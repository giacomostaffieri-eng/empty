# BDR Commission Audit

Checks that the commissions Checkout.com actually paid you (Workday) match what
you earned according to the **source of truth — Salesforce** — and flags anything
missing or mis-multiplied.

It was built to answer three questions:

1. **Is anything missing?** — deals that reached a paid milestone but were never paid.
2. **How do the multipliers work?** — see below.
3. **Can this be automated?** — yes: `commission_audit.py` reruns the whole check.

## How commissions work (L2 BDR)

You earn a commission each time an opportunity **you are credited on**
(`BDR_Name__c` = you) reaches a KPI milestone:

| KPI | Meaning | Salesforce field |
|-----|---------|------------------|
| **D4** | Explore / Discovery meeting held | `Disco_Call_Date__c` |
| **P1** | Opportunity set to **Propose** | `DateSettoP1__c` |
| **T1** | Opportunity set to **Trade** | `DateSettoT1__c` |
| Go-live bonus | merchant goes live (Silver/Gold) | `Finance_Go_Live__c` |

### Eligibility rules (applied by the tool)

- **A D4 only counts if the discovery call actually happened** —
  `Discovery_Call_Status__c == "Completed"`. A `Scheduled` no-show is not paid.
- **Only Silver / Gold ratings are payable** (`Account_Incentive_Rating__c`);
  Bronze is not. The rating that matters is the one *at the time of the KPI
  event* — if a deal was downgraded to Bronze afterwards it is still owed, so the
  tool parks current-Bronze deals in a "verify rating at event date" note rather
  than dropping them.
- **A milestone already reached is still owed even if the deal later dies**
  (Disqualified / Merchant Lost). Those rows are labelled "lost after milestone".

### Plan differences by year

- **2025 plan**: weights were D4 50% / P1 50% / **T1 0%** — T1s earned nothing at
  the time, but 2025 T1s were later paid retroactively at ~$410 via a true-up in
  the Feb-2026 statement. There was **no 150% kicker** in 2025, so ignore the
  kicker review for 2025 periods.
- **2026 plan**: T1 is weighted and the 150% kicker applies.

Two things that both get called "multiplier" but are different:

- **The 150% kicker** — the `Multiplier` column in the Workday export. It is a
  flag: `1` = base rate, `2` = **kicker on**, paying **1.5× the base value**
  (e.g. a D4 goes from $88 to $132). It switches on once you pass your quarterly
  target *and* meet the gates: all three KPI targets, ≥11 outbound D4s, ≥80% ICP.
- **A merchant counted "2" in the tracker** — that account simply has **two
  distinct opportunity records**, so it pays **two separate commissions**. This
  is the easiest thing for payroll to under-count.

## Usage

```bash
python3 commission_audit.py \
    --salesforce sf_opps.json \
    --paid-dir   workday/ \
    --period     2026-01:2026-06 \
    --trueup     trueups.json \
    --out        audit.report.md
```

Exit code is non-zero when anything is flagged (handy for CI / scheduling).

### 1. `--salesforce` — the source of truth

A JSON dump of your opportunities. Generate it from the Salesforce query below
(the repo does **not** store your data — it is git-ignored):

```sql
SELECT Name, StageName, Disco_Call_Date__c, DateSettoP1__c, DateSettoT1__c,
       Finance_Go_Live__c, LeadSource, Commission_Hold__c, XCommission_Hold__c
FROM Opportunity
WHERE BDR_Name__c = '<your user id>'
  AND (Disco_Call_Date__c != null OR DateSettoP1__c != null OR DateSettoT1__c != null)
```

Save the result as `{"records":[ ... ]}`. A CSV with the same columns also works.

### 2. `--paid-dir` — what Workday actually paid

Drop the Workday commission-statement exports into a folder. Files are
auto-classified from their header:

- `D4_Opportunities.csv`, `P1_Opportunities.csv`, `T1_Opportunities.csv`
  — per-opportunity payments (with `Multiplier` and `Commission USD`).
- `Adjustments.csv` — true-ups. Named lines (`D4 True up - ACME - For March`)
  are parsed automatically.

### 3. `--trueup` — true-ups with no merchant name (optional)

Some adjustment lines are generic (`D4 True up`, no name). When a comp analyst
emails you the breakdown, record it here so those deals aren't re-flagged:

```json
{
  "D4": ["DIGITAIL", "SMEG SPA"],
  "P1": ["EMOTION MOBILITY"],
  "T1": ["SIVOLA", "GUCCI"]
}
```

## What the report shows

- **Missing per KPI** (T1 → P1 → D4, highest value first) with each deal's
  current stage, whether it is on commission hold, and an estimated value.
  Rows on dead opportunities (Disqualified / Merchant Lost) are marked
  `DEAD — check policy`: whether a milestone already reached is still owed after
  the deal later dies is a comp-plan question to confirm.
- **Kicker attainment review** per quarter: target vs achieved, and whether the
  150% kicker was applied. It flags "all targets met but kicker off" for review
  — but cannot see the outbound/ICP gates, so it never asserts an error alone.

## Caveats

- Merchant names are matched fuzzily between Salesforce and Workday — **confirm
  each flagged deal in Salesforce before disputing it**.
- Recent (current-month) milestones may simply not be paid yet — treat them as
  *timing*, not missing.
- Value figures are estimates derived from the base rates seen in your own paid
  data; the exact owed amount depends on the quarter and kicker state.

## Automating it

- Re-run each pay cycle: refresh `sf_opps.json`, drop the new Workday CSVs into
  `workday/`, run the command. The non-zero exit code makes it easy to wire into
  a scheduled job that only alerts when something is off.
- The reconciliation logic lives in `commission_audit.py` and has no third-party
  dependencies (standard library only).
