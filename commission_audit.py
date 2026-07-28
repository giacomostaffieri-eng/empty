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

Usage:
    python commission_audit.py \
        --salesforce sf_opps.json \
        --paid-dir ./workday \
        --period 2026-01:2026-06 \
        [--trueup trueups.json] \
        [--out audit.report.md]

Inputs
------
--salesforce : JSON produced by the Salesforce MCP soqlQuery
    (shape: {"records":[{...}]}) OR a CSV. Must expose the KPI date fields above,
    Name, StageName, LeadSource, Commission_Hold__c and BDR_Name__c.
    Query used to generate it:
        SELECT Name, StageName, Disco_Call_Date__c, DateSettoP1__c,
               DateSettoT1__c, Finance_Go_Live__c, LeadSource,
               Commission_Hold__c, XCommission_Hold__c
        FROM Opportunity WHERE BDR_Name__c = '<your user id>'
        AND (Disco_Call_Date__c != null OR DateSettoP1__c != null
             OR DateSettoT1__c != null)

--paid-dir : folder with the Workday exports. Files are auto-classified by the
    KPI column in their header (D4/P1/T1) or by "Adjustment" content. The
    per-opportunity files carry columns: Opportunity, Rating, <KPI> date,
    Target, QTD achieved, Target incentive, Multiplier, Commission USD/LCY.

--trueup : optional JSON of manually-decoded adjustments (e.g. the breakdown a
    comp analyst emails for a generic "D4 True up" line with no merchant name):
        {"D4": ["DIGITAIL", "SMEG", ...], "P1": [...], "T1": [...]}
    Names here are treated as already paid so they are not re-flagged.
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
    """Return {'D4':[...], 'P1':[...], 'T1':[...]} of KpiEvent."""
    text = path.read_text()
    if text.lstrip().startswith("{"):
        records = json.loads(text).get("records", [])
    else:  # CSV fallback
        records = list(csv.DictReader(text.splitlines()))

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


def reconcile(sf, paid, adj, period, trueup):
    lo, hi = period
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
            if _matches(ev.name, paid_keys[kpi]):
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


def kicker_summary(paid: list[PaidRow]) -> list[dict]:
    """Per quarter/KPI attainment, and whether the 150% kicker was applied.

    The kicker requires ALL of: D4, P1 and T1 targets hit, >=11 outbound D4s, and
    >=80% ICP D4s. Outbound/ICP cannot be judged from these files, so this is a
    review aid — it does not assert an error on its own.
    """
    q: dict[tuple[str, str], dict] = {}
    for p in paid:
        k = (_quarter(p.statement), p.kpi)
        d = q.setdefault(k, {"target": p.target, "max_qtd": 0.0, "kicker": False})
        d["target"] = p.target or d["target"]
        d["max_qtd"] = max(d["max_qtd"], p.qtd)
        d["kicker"] = d["kicker"] or p.multiplier >= 2
    rows = []
    quarters = sorted({qk for qk, _ in q})
    for quarter in quarters:
        all_targets = all(
            q.get((quarter, kpi), {}).get("max_qtd", 0) >= q.get((quarter, kpi), {}).get("target", 1)
            for kpi in ("D4", "P1", "T1")
            if (quarter, kpi) in q
        )
        for kpi in ("D4", "P1", "T1"):
            d = q.get((quarter, kpi))
            if not d:
                continue
            rows.append(
                {
                    "quarter": quarter,
                    "kpi": kpi,
                    "target": d["target"],
                    "max_qtd": d["max_qtd"],
                    "kicker_applied": d["kicker"],
                    "all_targets_met": all_targets,
                }
            )
    return rows


# --------------------------------------------------------------------------- #
# Reporting                                                                    #
# --------------------------------------------------------------------------- #
def build_report(findings, est, kicker_rows, period) -> str:
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
        L.append("## Kicker (150% multiplier) — attainment review")
        L.append("")
        L.append("| Quarter | KPI | Target | Max QTD | Kicker paid? | All 3 targets met? |")
        L.append("|---|---|---|---|---|---|")
        for f in kicker_rows:
            review = ""
            if f["all_targets_met"] and not f["kicker_applied"]:
                review = " ⚠️"
            L.append(
                f"| {f['quarter']} | {f['kpi']} | {f['target']:.0f} | {f['max_qtd']:.0f} | "
                f"{'yes' if f['kicker_applied'] else 'no'} | "
                f"{'yes' if f['all_targets_met'] else 'no'}{review} |"
            )
        L.append("")
        L.append("_⚠️ = all three KPI targets met but kicker not applied — worth checking, "
                 "but confirm the outbound (>=11 D4) and 80% ICP gates, which these files do not show._")
        L.append("")
    L.append("_Names matched fuzzily; confirm each against Salesforce before disputing._")
    L.append("_D4 counts only when the discovery call is Completed (not Scheduled). "
             "Only Silver/Gold are payable; a Bronze here may still be owed if it was "
             "Silver/Gold at the time of the KPI event — check the rating history._")
    return "\n".join(L)


def parse_period(s: str) -> tuple[str, str]:
    lo, hi = s.split(":")
    return lo.strip(), hi.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit BDR commissions: Salesforce vs Workday paid.")
    ap.add_argument("--salesforce", required=True, type=Path)
    ap.add_argument("--paid-dir", required=True, type=Path)
    ap.add_argument("--period", default="2026-01:2026-06", type=parse_period,
                    help="YYYY-MM:YYYY-MM inclusive (default 2026-01:2026-06)")
    ap.add_argument("--trueup", type=Path, help="JSON of manually decoded true-up names")
    ap.add_argument("--out", type=Path, help="write the markdown report here")
    args = ap.parse_args(argv)

    sf = load_salesforce(args.salesforce)
    paid, adj = load_paid(args.paid_dir)
    trueup = json.loads(args.trueup.read_text()) if args.trueup else {}

    findings, est = reconcile(sf, paid, adj, args.period, trueup)
    kicker_rows = kicker_summary(paid)
    report = build_report(findings, est, kicker_rows, args.period)

    if args.out:
        args.out.write_text(report)
        print(f"Report written to {args.out}")
    print(report)
    total_missing = sum(len(v) for v in findings.values())
    return 1 if total_missing else 0


if __name__ == "__main__":
    sys.exit(main())
