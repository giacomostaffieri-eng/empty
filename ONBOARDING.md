# BDR Commission Audit — team guide

A small, dependency-free tool that checks whether the commissions Checkout.com
actually paid you (Workday) match what you earned according to **Salesforce**
(the source of truth), and flags anything missing or paid at the wrong
multiplier.

It reads three things and produces one Markdown report:

```
Salesforce opportunities  ─┐
Workday commission CSVs   ─┼──► commission_audit.py ──► audit.report.md
true-up breakdown (opt.)  ─┘
```

Nothing you feed it is stored in the repo — all personal data files are
git-ignored. Only the script and this guide are versioned.

---

## Quick start (5 minutes)

```bash
python3 commission_audit.py \
    --salesforce sf_opps.json \
    --paid-dir   workday/ \
    --period     2026-01:2026-06 \
    --trueup     trueups.json \    # optional
    --out        audit.report.md
```

Exit code is non-zero when anything is flagged — handy for scheduling.

### Step 1 — export your Salesforce opportunities → `sf_opps.json`

First get your own user id (run once, note the `userId`): in Salesforce open
the Developer Console → Query Editor, or ask an admin. Then run this SOQL and
export the result as JSON (`{"records":[ ... ]}`):

```sql
SELECT Name, StageName, Account_Incentive_Rating__c,
       Disco_Call_Date__c, Discovery_Call_Status__c,
       DateSettoP1__c, DateSettoT1__c, Finance_Go_Live__c,
       LeadSource, Commission_Hold__c, XCommission_Hold__c
FROM Opportunity
WHERE BDR_Name__c = '<your 18-char user id>'
  AND (Disco_Call_Date__c != null OR DateSettoP1__c != null OR DateSettoT1__c != null)
```

A CSV with the same columns also works.

### Step 2 — drop your Workday statements → `workday/`

Export the commission-statement tabs from Workday as CSV into a folder. Files
are auto-classified from their header row:

- `D4_Opportunities.csv`, `P1_Opportunities.csv`, `T1_Opportunities.csv`
  — per-opportunity payments (must include `Multiplier` and `Commission USD`).
- `Adjustments.csv` — true-ups. Both comment formats are parsed:
  `D4 True up - ACME - For March` (2026) and `April (D4):ACME - ...` (2025).

### Step 3 — (optional) record un-named true-ups → `trueups.json`

Some adjustment lines are generic (`D4 True up`, no merchant). When comp emails
you the breakdown, list the merchants so they aren't re-flagged:

```json
{ "D4": ["DIGITAIL", "SMEG SPA"], "P1": ["EMOTION MOBILITY"], "T1": ["SIVOLA"] }
```

---

## How the plan works (so you can sanity-check the rules)

You earn a commission each time an opportunity **you are credited on**
(`BDR_Name__c`) reaches a KPI milestone:

| KPI | Meaning | Salesforce field |
|-----|---------|------------------|
| **D4** | Explore / Discovery meeting held | `Disco_Call_Date__c` |
| **P1** | Opportunity set to **Propose** | `DateSettoP1__c` |
| **T1** | Opportunity set to **Trade** | `DateSettoT1__c` |
| Go-live | merchant goes live | `Finance_Go_Live__c` |

**Eligibility rules the tool applies:**

- A **D4 only counts if the discovery call actually happened**
  (`Discovery_Call_Status__c == "Completed"`); a `Scheduled` no-show is not paid.
- **Only Silver / Gold are payable**, and the rating that matters is the one *at
  the time of the event*. A deal downgraded to Bronze afterwards is still owed,
  so current-Bronze deals are parked as "verify rating at event date" rather than
  dropped.
- A **milestone already reached is still owed even if the deal later dies**
  (Disqualified / Merchant Lost).

**Two different things both called "multiplier":**

- **The 150% kicker** — the `Multiplier` column in Workday. `1` = base rate,
  `2` = kicker on (pays 1.5× base). It switches on once you pass your quarterly
  target *and* meet the gates (all three KPI targets, ≥11 outbound D4s, ≥80% ICP).
- **A merchant counted "2" in the tracker** — that account has **two distinct
  opportunity records**, so it pays **two separate commissions**. Easy for
  payroll to under-count.

**Plan differences by year:**

- **2025** — weights were D4 50% / P1 50% / **T1 0%** (T1 earned nothing at the
  time, but 2025 T1s were later trued up at ~$410 in the Feb-2026 statement), and
  there was **no kicker** (ignore the kicker review for 2025 periods).
- **2026** — T1 is weighted and the 150% kicker applies.

---

## Reading the report

- **Missing per KPI** (T1 → P1 → D4, highest value first): stage, rating,
  commission-hold flag, and an estimated value. Deals lost after a milestone are
  labelled so; current-Bronze deals are flagged for a rating-history check.
- **Kicker attainment review** per quarter: target vs achieved and whether the
  kicker was applied. It flags "all targets met but kicker off" for review, but
  cannot see the outbound/ICP gates, so it never asserts an error on its own.

## Before you dispute anything

- Names are matched **fuzzily** between Salesforce and Workday — confirm each
  flagged deal in Salesforce first.
- Current-month milestones may simply not be paid yet — that's *timing*, not a
  miss.
- Value figures are **estimates** from the base rates seen in your own paid data;
  the exact amount depends on the quarter and kicker state.
- Treat the output as a prompt to ask comp to double-check — not proof of error.

## Automating it

Re-run each pay cycle: refresh `sf_opps.json`, drop the new Workday CSVs into
`workday/`, run the command. The non-zero exit code makes it easy to wire into a
scheduled job that only alerts when something looks off. The logic lives in
`commission_audit.py` — standard library only, no install step.
