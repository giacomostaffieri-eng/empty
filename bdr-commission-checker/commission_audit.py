#!/usr/bin/env python3
"""
Commission audit for Checkout.com BDR compensation.

Reconciles the *source of truth* (Salesforce opportunities credited to a BDR,
via BDR_Name__c) against what was *actually paid* (Workday commission statement
CSVs), and flags anything missing, plus checks the 150% kicker ("Multiplier").

KPI -> Salesforce field mapping (validated against the H1-2026 tracker pivot):
    D4  =  Disco_Call_Date__c   (First Explore Meeting Date)
    P1  =  DateSettoP1__c       (Date Set to Propose)
    T1  =  DateSettoT1__c       (Date Set to Trade)
    go-live bonus = Finance_Go_Live__c

Two multiplier concepts, kept distinct:
  * "Multiplier" column in Workday = the 150% kicker. It is a *flag* (1 or 2);
    when 2 the opportunity is paid at 1.5x the base value. It switches on once
    quarter-to-date attainment passes target (and the kicker gates are met).
  * A merchant showing a count of "2" in the tracker = two *distinct*
    opportunity records on the same account -> two separate commissions.

This is a self-service tool: each BDR connects it to *their own* Salesforce,
drops in *their own* Workday CSV exports (and optionally *their own* tracker
export), and gets a cross-check of what they earned vs what they were paid. No
IDs or merchant names are hard-coded.

Usage (connect to your own Salesforce):
    python commission_audit.py \
        --sf-fetch \
        --paid-dir ./workday \
        --tracker tracker.csv \
        --period 2026-01:2026-06 \
        [--trueup trueups.json] [--alias alias.json] [--out audit.report.md]

Offline alternative (use a pre-exported opportunities file instead of --sf-fetch):
    python commission_audit.py --salesforce sf_opps.json --paid-dir ./workday ...

Inputs
------
--sf-fetch : connect to your Salesforce (see salesforce_client.py / SETUP.md) and
    pull the opportunities where you are the BDR. Auto-detects your own user id.

--salesforce : offline alternative — a JSON ({"records":[{...}]}) or CSV export of
    the same opportunities. Must expose the KPI date fields above, Name, StageName,
    LeadSource, Commission_Hold__c. Query used:
        SELECT Name, StageName, Disco_Call_Date__c, DateSettoP1__c,
               DateSettoT1__c, Finance_Go_Live__c, LeadSource,
               Commission_Hold__c, XCommission_Hold__c
        FROM Opportunity WHERE BDR_Name__c = '<your user id>'
        AND (Disco_Call_Date__c != null OR DateSettoP1__c != null
             OR DateSettoT1__c != null)

--tracker : optional CSV export of your BDR tracker (the detailed per-opportunity
    tab). Adds a "in Salesforce but missing from the tracker" crediting-gap check.

--paid-dir : folder with the Workday exports. Files are auto-classified by the
    KPI column in their header (D4/P1/T1) or by "Adjustment" content. The
    per-opportunity files carry columns: Opportunity, Rating, <KPI> date,
    Target, QTD achieved, Target incentive, Multiplier, Commission USD/LCY.

--trueup : optional JSON of manually-decoded adjustments (e.g. the breakdown a
    comp analyst emails for a generic "D4 True up" line with no merchant name):
        {"D4": ["DIGITAIL", "SMEG", ...], "P1": [...], "T1": [...]}
    Names here are treated as already paid so they are not re-flagged.

--alias : optional JSON mapping the Salesforce opportunity name to the name(s)
    the same account is paid under in Workday. Accounts get renamed (e.g. the opp
    that is "Electromaps" in Salesforce was paid as "Wall Box Chargers SL"), which
    otherwise makes a paid deal look missing. Map them so the match still works:
        {"Electromaps": "Wall Box Chargers SL", "Arcaplanet": ["Agrifarma SPA"]}
    A value may be a single name or a list. This is the single biggest source of
    false "missing" flags, so add an entry whenever comp tells you a deal was paid
    under a different name.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

DEAD_STAGES = {"Disqualified", "Merchant Lost", "Closed/Lost", "Closed Lost", "Closed Won Lost"}

# 150% kicker gates (L2 BDR). All must hold for a quarter to accelerate:
#   1. 100% of quarterly target on all three KPIs (D4, P1, T1);
#   2. outbound D4 >= 70% of the D4 target;
#   3. ICP-compliant D4 >= 80% of the D4 target.
# Gate 3 needs an ICP flag that the standard export does not carry, so it is
# reported as "unverifiable" rather than assumed. Adjust the outbound sources to
# match how your org labels LeadSource.
KICKER_OUTBOUND_FRACTION = 0.70
KICKER_ICP_FRACTION = 0.80
OUTBOUND_SOURCES = {"outbound"}

# Words dropped when reducing an opportunity/merchant name to a comparison key.
_STOP = {
    "SPA", "SRL", "SL", "SA", "SAU", "SLU", "LTD", "LIMITED", "INC", "GROUP",
    "S", "P", "A", "R", "L", "SGPS", "LDA", "AS", "BV", "BENEFIT", "SOCIETA",
    "NEW", "BUSINESS", "THE", "DE", "DEL", "SOCIEDAD", "LIMITADA", "ANONIMA",
    "MERCANTIL", "ESTATAL", "COMPANY", "OPERATORS", "HOLDINGS", "HOLDING",
    "RETAIL", "ITALIA", "ITALY", "SPAIN", "ESPANA", "SERVICOS", "SOCIETE",
    "ANONYME", "TRADING", "TOURIST", "AND", "URBAN", "MOBILITY", "DIGITAL",
    "EF", "FC", "EDE", "ELECTRONIC", "ISSUER", "ALTERNATIVE",
}


def norm(name: str) -> str:
    """Reduce a name to its first two significant tokens for fuzzy matching."""
    if not name:
        return ""
    s = name.split(" - ")[0]                      # merchant part before first " - "
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.upper()
    s = re.sub(r"\(.*?\)", " ", s)                # drop parentheticals
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    toks = [t for t in s.split() if t and t not in _STOP]
    return " ".join(toks[:2])


def _matches(sf_name: str, paid_keys: set[str]) -> bool:
    n = norm(sf_name)
    if not n:
        return False
    if n in paid_keys:
        return True
    first = n.split(" ")[0]
    nd = n.replace(" ", "")                       # de-spaced, e.g. "Stanley Bet" ~ "Stanleybet"
    for p in paid_keys:
        if not p:
            continue
        if p == n:
            return True
        if len(first) >= 4 and p.split(" ")[0] == first:
            return True
        if len(n) >= 5 and (n in p or p in n):
            return True
        pd = p.replace(" ", "")
        if len(nd) >= 6 and len(pd) >= 6 and (nd.startswith(pd) or pd.startswith(nd)):
            return True
    return False


def _month(s: str | None) -> str:
    return s[:7] if s else ""


def _to_iso(d: str) -> str:
    """Accept dd/mm/yyyy or yyyy-mm-dd, return yyyy-mm-dd (or '')."""
    d = (d or "").strip()
    if re.match(r"\d{4}-\d{2}-\d{2}", d):
        return d[:10]
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", d)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


_MONTHS = ("january|february|march|april|may|june|july|august|september|october|november|december")


def _adjust_name(comment: str) -> str:
    """Extract the merchant from an adjustment comment.

    Handles both statement formats seen in the exports:
      2026: 'D4 True up - ALTEX ROMANIA SRL - For March', 'D4 - Adevinta True up',
            'D4 True up - Everli - Issuing', bare 'D4 True up' (-> '').
      2025: 'April (D4):GOLDEN GOOSE SPA - New Business - ...',
            'July (P1):Percassi Retail - New Business - -'.
    """
    if not re.search(r"\b(D4|P1|T1)\b", comment):
        return ""
    if ":" in comment:                                  # 2025 'Month (KPI):Name'
        rest = comment.split(":", 1)[1]
    else:                                               # 2026 'KPI True up - Name'
        rest = re.sub(r"\b(D4|P1|T1)\b", " ", comment, count=1)
        rest = re.sub(r"true\s*up", " ", rest, flags=re.I)
    rest = re.sub(rf"(?i)^\s*({_MONTHS})\b", " ", rest)  # strip a leading month name
    junk = re.compile(rf"(?i)^(for\b|issuing$|q[1-4]$|\d{{4}}$|for the|({_MONTHS})$)")
    parts = [p.strip(" -") for p in rest.split(" - ")]
    parts = [p for p in parts if p and not junk.match(p)]
    return parts[0] if parts else ""


def _num(x: str) -> float:
    x = (x or "").replace('"', "").replace(",", "").strip()
    try:
        return float(x)
    except ValueError:
        return 0.0


@dataclass
class KpiEvent:
    name: str
    date: str
    stage: str
    lead_source: str
    hold: bool
    rating: str


@dataclass
class PaidRow:
    kpi: str
    statement: str
    opportunity: str
    target: float
    qtd: float
    multiplier: float
    usd: float


# --------------------------------------------------------------------------- #
# Loading                                                                      #
# --------------------------------------------------------------------------- #
def load_salesforce(path: Path) -> dict[str, list[KpiEvent]]:
    """Load Salesforce records from a JSON/CSV file and return KpiEvents."""
    text = path.read_text()
    if text.lstrip().startswith("{"):
        records = json.loads(text).get("records", [])
    else:  # CSV fallback
        records = list(csv.DictReader(text.splitlines()))
    return events_from_records(records)


def events_from_records(records: list[dict]) -> dict[str, list[KpiEvent]]:
    """Return {'D4':[...], 'P1':[...], 'T1':[...]} of KpiEvent from raw SF records.

    Shared by the file loader and the live Salesforce fetch, so both paths apply
    the same eligibility rules.
    """
    fields = {"D4": "Disco_Call_Date__c", "P1": "DateSettoP1__c", "T1": "DateSettoT1__c"}
    out: dict[str, list[KpiEvent]] = {"D4": [], "P1": [], "T1": []}
    for r in records:
        hold = bool(r.get("Commission_Hold__c")) or bool(r.get("XCommission_Hold__c"))
        for kpi, f in fields.items():
            d = _to_iso(r.get(f))
            # A D4 only earns commission if the discovery/explore call was actually
            # held: Discovery_Call_Status__c == "Completed" (a "Scheduled" no-show
            # never happened and is not paid). P1/T1 are stage transitions and count
            # whenever the date is set.
            if kpi == "D4" and (r.get("Discovery_Call_Status__c") or "").strip().lower() != "completed":
                continue
            if d:
                out[kpi].append(
                    KpiEvent(
                        name=r.get("Name", ""),
                        date=d,
                        stage=r.get("StageName", ""),
                        lead_source=r.get("LeadSource", ""),
                        hold=hold,
                        rating=(r.get("Account_Incentive_Rating__c") or "").strip(),
                    )
                )
    return out


def _classify(header_rows: list[list[str]]) -> str | None:
    flat = " ".join(c for row in header_rows for c in row).upper()
    if "ADJUSTMENT" in flat or "TRUE UP" in flat or "COMMENT" in flat:
        return "ADJ"
    for kpi in ("D4", "P1", "T1"):
        if kpi in flat:
            return kpi
    return None


def load_paid(paid_dir: Path) -> tuple[list[PaidRow], dict[str, set[str]]]:
    """Return (per-opportunity paid rows, {kpi: set(adjustment names)})."""
    rows: list[PaidRow] = []
    adj: dict[str, set[str]] = {"D4": set(), "P1": set(), "T1": set()}
    for path in sorted(paid_dir.glob("*.csv")):
        data = list(csv.reader(path.read_text().splitlines()))
        if not data:
            continue
        kind = _classify(data[:3])
        body = data[3:]
        if kind == "ADJ":
            for row in body:
                if not row or row[0].startswith("Totals"):
                    continue
                comment = row[2] if len(row) > 2 else ""
                m = re.search(r"\b(D4|P1|T1)\b", comment)
                if not m:
                    continue
                kpi = m.group(1)
                name = _adjust_name(comment)     # handles both "D4 True up - X" and "D4 - X True up"
                if name:
                    adj[kpi].add(norm(name))
        elif kind in ("D4", "P1", "T1"):
            last_stmt = ""
            for row in body:
                if not row or row[0].startswith("Totals") or len(row) < 11:
                    continue
                opp = (row[2] or "").strip()
                if not opp:
                    continue
                last_stmt = _to_iso(row[1]) or last_stmt   # statement only on group's first row
                rows.append(
                    PaidRow(
                        kpi=kind,
                        statement=last_stmt,
                        opportunity=opp,
                        target=_num(row[5]),
                        qtd=_num(row[6]),
                        multiplier=_num(row[9]),
                        usd=_num(row[10]),
                    )
                )
    return rows, adj


def load_alias(path: Path | None) -> dict[str, list[str]]:
    """{normalized SF name -> [alternate names used in Workday]}.

    Lets a renamed account still match its payment (see --alias in the module
    docstring). Values may be a single string or a list.
    """
    if not path:
        return {}
    raw = json.loads(path.read_text())
    out: dict[str, list[str]] = {}
    for sf_name, alts in raw.items():
        if isinstance(alts, str):
            alts = [alts]
        out.setdefault(norm(sf_name), []).extend(alts)
    return out


def load_tracker(path: Path | None) -> dict[str, set[str]] | None:
    """Parse a BDR tracker export (CSV) into {kpi: set(normalized names)}.

    Looks for the detailed per-opportunity tab: a header row that has an
    "Opp name"/"Opportunity" column and a "Rule" column whose values are
    D4/P1/T1. Returns None if the file doesn't look like that layout (e.g. the
    pivot tab), so the caller can skip the tracker cross-check gracefully.
    """
    if not path:
        return None
    rows = list(csv.reader(path.read_text().splitlines()))
    name_col = rule_col = header_idx = None
    for i, row in enumerate(rows[:20]):
        low = [c.strip().lower() for c in row]
        nc = next((j for j, c in enumerate(low) if "opp" in c and "name" in c or c == "opportunity"), None)
        rc = next((j for j, c in enumerate(low) if c == "rule" or c.endswith(" rule")), None)
        if nc is not None and rc is not None:
            name_col, rule_col, header_idx = nc, rc, i
            break
    if header_idx is None:
        return None
    out: dict[str, set[str]] = {"D4": set(), "P1": set(), "T1": set()}
    for row in rows[header_idx + 1:]:
        if len(row) <= max(name_col, rule_col):
            continue
        kpi = row[rule_col].strip().upper()
        if kpi in out:
            key = norm(row[name_col])
            if key:
                out[kpi].add(key)
    return out


# --------------------------------------------------------------------------- #
# Reconciliation                                                               #
# --------------------------------------------------------------------------- #
def base_values(paid: list[PaidRow]) -> dict[str, float]:
    """Empirical base (multiplier==1) commission per KPI, for value estimates."""
    out = {}
    for kpi in ("D4", "P1", "T1"):
        vals = [p.usd for p in paid if p.kpi == kpi and p.multiplier <= 1 and p.usd]
        out[kpi] = round(sum(vals) / len(vals), 2) if vals else 0.0
    return out


def reconcile(sf, paid, adj, period, trueup, alias=None):
    lo, hi = period
    alias = alias or {}
    paid_keys = {kpi: {norm(p.opportunity) for p in paid if p.kpi == kpi} for kpi in ("D4", "P1", "T1")}
    for kpi in ("D4", "P1", "T1"):
        paid_keys[kpi] |= adj.get(kpi, set())
        paid_keys[kpi] |= {norm(n) for n in trueup.get(kpi, [])}

    est = base_values(paid)
    findings: dict[str, list[dict]] = {"D4": [], "P1": [], "T1": []}
    for kpi in ("D4", "P1", "T1"):
        for ev in sf[kpi]:
            if not (lo <= _month(ev.date) <= hi):
                continue
            # Match by the SF name, or by any alias name the account is paid under
            # in Workday (renames are the main cause of false "missing" flags).
            alt_names = alias.get(norm(ev.name), [])
            if _matches(ev.name, paid_keys[kpi]) or any(_matches(a, paid_keys[kpi]) for a in alt_names):
                continue
            findings[kpi].append(
                {
                    "name": ev.name.split(" - ")[0],
                    "full_name": ev.name,
                    "date": ev.date,
                    "stage": ev.stage,
                    "dead": ev.stage in DEAD_STAGES,
                    "hold": ev.hold,
                    "rating": ev.rating,
                    "bronze": ev.rating.lower() == "bronze",
                    "est_usd": est[kpi],
                }
            )
    return findings, est


def _quarter(stmt: str) -> str:
    if len(stmt) < 7:
        return "?"
    y, m = stmt[:4], int(stmt[5:7])
    return f"{y}-Q{(m - 1) // 3 + 1}"


def kicker_check(sf, paid: list[PaidRow]) -> list[dict]:
    """Per-quarter 150% kicker verdict against the real gates.

    Evaluates gate 1 (all three targets) from Workday QTD, gate 2 (outbound D4
    share) from Salesforce LeadSource, and reports gate 3 (ICP) as unverifiable
    since the export carries no ICP flag. Also sums base-rate (1x) vs accelerated
    (1.5x) USD per quarter: when a quarter clears the gates but still has base-rate
    milestones, that 0.5x delta is a *potential* underpayment worth querying —
    depending on whether your plan accelerates the whole quarter or only the units
    above target.
    """
    q: dict[str, dict] = {}
    for p in paid:
        quarter = _quarter(p.statement)
        if quarter == "?":
            continue
        e = q.setdefault(quarter, {"kpi": {}, "base_usd": 0.0, "accel_usd": 0.0})
        d = e["kpi"].setdefault(p.kpi, {"target": 0.0, "qtd": 0.0, "kicker": False})
        d["target"] = p.target or d["target"]
        d["qtd"] = max(d["qtd"], p.qtd)
        if p.multiplier >= 2:
            d["kicker"] = True
            e["accel_usd"] += p.usd
        else:
            e["base_usd"] += p.usd

    outbound_d4: dict[str, int] = {}
    for ev in sf.get("D4", []):
        if ev.lead_source.strip().lower() in OUTBOUND_SOURCES:
            qq = _quarter(ev.date)
            outbound_d4[qq] = outbound_d4.get(qq, 0) + 1

    rows = []
    for quarter in sorted(q):
        kp = q[quarter]["kpi"]
        have_all = all(k in kp for k in ("D4", "P1", "T1"))
        targets_met = (
            all(kp[k]["qtd"] >= kp[k]["target"] > 0 for k in ("D4", "P1", "T1"))
            if have_all else None
        )
        d4_target = kp.get("D4", {}).get("target", 0)
        outb = outbound_d4.get(quarter, 0)
        outbound_ok = outb >= KICKER_OUTBOUND_FRACTION * d4_target if d4_target else None
        applied = any(v.get("kicker") for v in kp.values())
        rows.append({
            "quarter": quarter,
            "kpi": kp,
            "targets_met": targets_met,
            "outbound_d4": outb,
            "outbound_need": round(KICKER_OUTBOUND_FRACTION * d4_target, 1) if d4_target else None,
            "icp_need": round(KICKER_ICP_FRACTION * d4_target, 1) if d4_target else None,
            "outbound_ok": outbound_ok,
            "kicker_applied": applied,
            "base_usd": q[quarter]["base_usd"],
            "accel_usd": q[quarter]["accel_usd"],
        })
    return rows


# --------------------------------------------------------------------------- #
# Reporting                                                                    #
# --------------------------------------------------------------------------- #
def tracker_gaps(sf, tracker, period):
    """SF milestones in-period that the tracker does not list (crediting gaps).

    Returns {kpi: [names]}. Only meaningful when a tracker was supplied.
    """
    lo, hi = period
    gaps: dict[str, list[str]] = {"D4": [], "P1": [], "T1": []}
    for kpi in ("D4", "P1", "T1"):
        seen = tracker.get(kpi, set())
        for ev in sf[kpi]:
            if lo <= _month(ev.date) <= hi and norm(ev.name) not in seen:
                gaps[kpi].append(ev.name.split(" - ")[0])
    return gaps


def build_report(findings, est, kicker_rows, period, trk_gaps=None) -> str:
    lo, hi = period
    L = [f"# Commission audit — {lo} … {hi}", ""]
    grand = 0.0
    for kpi in ("T1", "P1", "D4"):  # highest value first
        items = sorted(findings[kpi], key=lambda x: x["date"])
        if not items:
            continue
        # "Owed" = Silver/Gold, not on hold. Dead-but-milestone-reached still counts
        # (a completed discovery / a set-to-Propose is earned even if the deal later
        # dies). Bronze is parked for review: rating may have been higher at the time.
        owed = [i for i in items if not i["bronze"] and not i["hold"]]
        subtotal = sum(i["est_usd"] for i in owed)
        grand += subtotal
        L.append(f"## {kpi} — {len(items)} not found in paid  (~${subtotal:,.0f} owed, Silver/Gold)")
        L.append("")
        L.append("| Merchant | KPI date | Stage | Rating | Hold | ~USD | Note |")
        L.append("|---|---|---|---|---|---|---|")
        for i in items:
            if i["bronze"]:
                note = "BRONZE — verify rating at event date"
            elif i["hold"]:
                note = "ON HOLD"
            elif i["dead"]:
                note = "lost after milestone — still owed"
            else:
                note = "owed"
            L.append(
                f"| {i['name']} | {i['date']} | {i['stage']} | {i['rating'] or '?'} | "
                f"{'yes' if i['hold'] else 'no'} | {i['est_usd']:.0f} | {note} |"
            )
        L.append("")
    L.append(f"**Estimated unpaid on Silver/Gold, non-held opportunities: ~${grand:,.0f}**")
    L.append(f"(base values used — D4 ${est['D4']:.0f} · P1 ${est['P1']:.0f} · T1 ${est['T1']:.0f}; "
             f"kicker months pay 1.5x)")
    L.append("")
    if kicker_rows:
        def yn(v):
            return "?" if v is None else ("yes" if v else "no")
        L.append("## Kicker (150%) — gate check per quarter")
        L.append("")
        L.append("| Quarter | Gate 1: all targets | Gate 2: outbound ≥70% | Gate 3: ICP ≥80% | Kicker applied? | Base-rate (1x) $ | Accelerated (1.5x) $ |")
        L.append("|---|---|---|---|---|---|---|")
        gap_total = 0.0
        for f in kicker_rows:
            kp = f["kpi"]
            g1 = " ".join(f"{k} {kp[k]['qtd']:.0f}/{kp[k]['target']:.0f}" for k in ("D4", "P1", "T1") if k in kp)
            g2 = (f"{f['outbound_d4']}/{f['outbound_need']:.0f}"
                  if f["outbound_need"] is not None else "?")
            icp = f"need ≥{f['icp_need']:.0f}" if f["icp_need"] is not None else "?"
            qualifies = f["targets_met"] and f["outbound_ok"]
            gap = 0.5 * f["base_usd"] if (qualifies and f["base_usd"]) else 0.0
            gap_total += gap
            flag = ""
            if qualifies and not f["kicker_applied"]:
                flag = " ⚠️ gates met, kicker OFF"
            elif f["kicker_applied"] and f["targets_met"] is False:
                flag = " ⚠️ kicker ON but targets missed"
            L.append(
                f"| {f['quarter']} | {yn(f['targets_met'])} ({g1}) | {yn(f['outbound_ok'])} ({g2}) | "
                f"{yn(None)} ({icp}) | {yn(f['kicker_applied'])}{flag} | "
                f"${f['base_usd']:,.0f} | ${f['accel_usd']:,.0f} |"
            )
        L.append("")
        L.append("_Gate 3 (ICP) can't be verified — the export has no ICP flag; confirm with Comp._")
        if gap_total:
            L.append("")
            L.append(f"**Potential kicker gap: ~${gap_total:,.0f}.** In quarters that clear "
                     "gates 1 & 2, this is 0.5× of the milestones still paid at base (1x). "
                     "It is only owed if the plan accelerates the *whole* quarter once gates "
                     "are met; if instead only units above target accelerate, the base-rate "
                     "rows are correct. Worth confirming the mechanic with Comp.")
        L.append("")
    if trk_gaps is not None:
        total = sum(len(v) for v in trk_gaps.values())
        L.append("## Tracker cross-check — in Salesforce but missing from your tracker")
        L.append("")
        if total == 0:
            L.append("_Every in-period Salesforce milestone is present in the tracker._")
        else:
            L.append("These milestones exist in Salesforce for the period but were not found "
                     "in the tracker export — a likely crediting gap upstream of payroll:")
            L.append("")
            L.append("| KPI | Merchant |")
            L.append("|---|---|")
            for kpi in ("T1", "P1", "D4"):
                for name in sorted(trk_gaps.get(kpi, [])):
                    L.append(f"| {kpi} | {name} |")
        L.append("")
    L.append("_Names matched fuzzily; confirm each against Salesforce before disputing. "
             "If a deal was paid under a renamed account, add it to --alias so it stops "
             "being flagged._")
    L.append("_D4 counts only when the discovery call is Completed (not Scheduled). "
             "Only Silver/Gold are payable; a Bronze here may still be owed if it was "
             "Silver/Gold at the time of the KPI event — check the rating history._")
    return "\n".join(L)


def parse_period(s: str) -> tuple[str, str]:
    lo, hi = s.split(":")
    return lo.strip(), hi.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Cross-check your BDR commissions: Salesforce (earned) vs Workday (paid).")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sf-fetch", action="store_true",
                     help="connect to YOUR Salesforce and pull your opportunities (see SETUP.md)")
    src.add_argument("--salesforce", type=Path,
                     help="use a pre-exported opportunities file (JSON or CSV) instead of --sf-fetch")
    ap.add_argument("--paid-dir", required=True, type=Path,
                    help="folder with your Workday commission CSV exports")
    ap.add_argument("--tracker", type=Path,
                    help="your BDR tracker export (CSV) — adds a crediting-gap cross-check")
    ap.add_argument("--period", default="2026-01:2026-06", type=parse_period,
                    help="YYYY-MM:YYYY-MM inclusive (default 2026-01:2026-06)")
    ap.add_argument("--trueup", type=Path, help="JSON of manually decoded true-up names")
    ap.add_argument("--alias", type=Path,
                    help="JSON mapping SF opp name -> Workday name(s) for renamed accounts")
    ap.add_argument("--sf-cache", type=Path, default=Path("sf_opps.json"),
                    help="where --sf-fetch writes the pulled opportunities (default sf_opps.json)")
    ap.add_argument("--out", type=Path, help="write the markdown report here")
    args = ap.parse_args(argv)

    if args.sf_fetch:
        import salesforce_client
        n = salesforce_client.fetch_to_file(args.sf_cache)
        print(f"Fetched {n} opportunities from Salesforce → {args.sf_cache}")
        sf = load_salesforce(args.sf_cache)
    else:
        sf = load_salesforce(args.salesforce)

    paid, adj = load_paid(args.paid_dir)
    trueup = json.loads(args.trueup.read_text()) if args.trueup else {}
    alias = load_alias(args.alias)

    findings, est = reconcile(sf, paid, adj, args.period, trueup, alias)
    kicker_rows = kicker_check(sf, paid)

    trk = load_tracker(args.tracker)
    trk_gaps = tracker_gaps(sf, trk, args.period) if trk is not None else None
    if args.tracker and trk is None:
        print("Note: could not read the tracker export as the detailed per-opportunity "
              "layout — skipping the tracker cross-check.", file=sys.stderr)

    report = build_report(findings, est, kicker_rows, args.period, trk_gaps)

    if args.out:
        args.out.write_text(report)
        print(f"Report written to {args.out}")
    print(report)
    total_missing = sum(len(v) for v in findings.values())
    return 1 if total_missing else 0


if __name__ == "__main__":
    sys.exit(main())
