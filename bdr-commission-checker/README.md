# BDR Commission Checker

A self-service tool that cross-checks a BDR's commissions. It compares, for the
period you choose:

- **Salesforce** — what you *earned* (opportunities where you're the BDR that hit
  a D4 / P1 / T1 milestone). This is the source of truth.
- **Workday** — what you were *actually paid* (your commission-statement CSVs).
- **Your BDR tracker** *(optional)* — what the company *expected* to pay you.

…and reports what's missing at each hop, plus a check on the 150% kicker
(“Multiplier”). Each BDR runs it against **their own** data — nothing is
hard-coded to any one person, org, or merchant.

```
YOUR Salesforce  ─┐
YOUR Workday CSVs ┼──►  commission_audit.py  ──►  audit.report.md
YOUR tracker (opt)┘
```

Your data never leaves your machine and is never committed — see *Data & privacy*.

---

## Install

Python **3.8+** is all you need for the offline mode. Check it:

```bash
python3 --version
```

Get the code and enter the folder:

```bash
git clone <this-repo-url>
cd bdr-commission-checker
```

To connect live to Salesforce (`--sf-fetch`), also install one dependency:

```bash
pip install -r requirements.txt
```

(If you only ever export your opportunities to a file and use `--salesforce`, you
can skip `pip install` entirely — the core is standard-library only.)

## Run it

**Connected to your own Salesforce** (recommended — see [SETUP.md](SETUP.md) to
authenticate once):

```bash
python3 commission_audit.py \
    --sf-fetch \
    --paid-dir ./workday \
    --tracker  ./tracker.csv \        # optional
    --period   2026-01:2026-06 \
    --out      audit.report.md
```

**Offline** (no Salesforce connection — feed a pre-exported file instead):

```bash
python3 commission_audit.py \
    --salesforce ./my_opps.json \
    --paid-dir   ./workday \
    --period     2026-01:2026-06 \
    --out        audit.report.md
```

The command exits non-zero when anything is flagged (handy for scheduling).

## The three inputs

1. **Salesforce** — `--sf-fetch` pulls your opportunities live (see
   [SETUP.md](SETUP.md)); or export them yourself and pass `--salesforce file`
   (JSON `{"records":[...]}` or CSV with the KPI date fields).
2. **Workday** — `--paid-dir FOLDER`: drop your commission-statement CSV exports
   in a folder. Files are auto-classified from their header
   (`D4_Opportunities.csv`, `P1_…`, `T1_…`, `Adjustments.csv`).
3. **Tracker** *(optional)* — `--tracker tracker.csv`: export the detailed
   per-opportunity tab of your BDR tracker. Adds an “in Salesforce but missing
   from the tracker” crediting-gap check.

### Optional helpers

- `--alias alias.json` — map a Salesforce opportunity name to the name(s) the
  same account is paid under in Workday. Accounts get renamed (e.g. the opp shown
  as “Electromaps” was paid as “Wall Box Chargers SL”), which otherwise makes a
  paid deal look missing. **This is the biggest source of false positives** — add
  an entry whenever comp confirms a deal was paid under a different name. See
  `alias.example.json`.
- `--trueup trueups.json` — record the breakdown of a generic, un-named “D4 True
  up” adjustment so those deals aren't re-flagged. See `trueups.example.json`.

## How the plan works (so you can sanity-check the rules)

| KPI | Meaning | Salesforce field |
|-----|---------|------------------|
| **D4** | Explore / Discovery meeting held | `Disco_Call_Date__c` |
| **P1** | Opportunity set to **Propose** | `DateSettoP1__c` |
| **T1** | Opportunity set to **Trade** | `DateSettoT1__c` |

**Eligibility rules applied:**

- A **D4** counts only if the discovery call is `Completed` (a `Scheduled`
  no-show is not paid).
- Only **Silver/Gold** are payable; current-Bronze deals are parked for a
  rating-at-event-date check rather than dropped (ratings change over time, and
  comp may read a different rating than the Salesforce field).
- A milestone already reached is still owed even if the deal is later lost.

**Two different things both called “multiplier”:** the `Multiplier` column in
Workday is the 150% kicker (`1` = base, `2` = 1.5× base). A merchant counted “2”
in the tracker instead means two *distinct* opportunities → two commissions.

## What the report shows

- **Missing per KPI** (T1 → P1 → D4, highest value first): stage, rating, hold
  flag, an estimated value, and a note (owed / lost-after-milestone / Bronze).
- **Kicker (150%) gate check** per quarter — evaluates all three L2 gates:
  100% of the D4/P1/T1 targets, outbound D4 ≥70% of target (from `LeadSource`),
  and ICP D4 ≥80% of target (from the account's `Sales_Ops_TP_Status__c` flag).
  It flags quarters where the gates are met but the kicker wasn't applied, and
  sums base-rate (1×) vs accelerated (1.5×) pay so you can query any base-rate
  milestones left in a qualifying quarter.
- **Tracker cross-check** (if `--tracker` given): Salesforce milestones absent
  from the tracker — usually a crediting gap upstream of payroll.

## Before you dispute anything

- Names are matched **fuzzily** — confirm each flagged deal in Salesforce first.
- Current-month milestones may simply not be paid yet — that's *timing*.
- Values are estimates from the base rates in your own paid data.
- Treat the output as a prompt to ask comp to double-check, not proof of error.

## Data & privacy

Your Salesforce/Workday data, the fetched `sf_opps.json`, tracker CSVs, generated
reports, and your real `alias.json` / `trueups.json` are all git-ignored — only
the code and the generic example files are versioned. The Salesforce connection
talks only to your own org (see SETUP.md); nothing is sent anywhere else.
