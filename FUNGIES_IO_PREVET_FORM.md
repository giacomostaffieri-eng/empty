# Pre-vet Form for Direct Sellers — Fungies Inc. (Fungies.io)

**Completed by:** Giacomo Staffieri, Commercial
**Date:** 7 September 2026
**Purpose:** Pre-qualification assessment ahead of MAF submission — to accompany the Deal Support Request (DSR)
**Companion document:** `FUNGIES_IO_MASTER_BRIEF.md` (full opportunity, compliance and risk analysis, with source references S1–S12)

> **Note to Underwriting.** All information below is as represented by the prospect (CEO Duke Vu) across a discovery call and two written responses, plus six supplied documents. Every field is answered. Where a representation is **unevidenced or contradicted by the prospect's own documents, it is marked and cross-referenced** — I have not smoothed those over, because two of them (the tax reconciliation and the monitoring register) are material to the underwriting decision. Four items requested at pre-vet stage have **not** been supplied and are flagged as gaps in the relevant fields: the 3-month processing screenshot, the Stripe cost breakdown, a financial-licence position supported by counsel, and the Monitoring Threshold Register.

---

## Information Requirements

### CKO Legal Entity Check

**Not yet performed** — to be run by Underwriting/Compliance against internal screening on the identifiers below.

| Entity | Role | Identifiers |
|---|---|---|
| **Fungies Inc.** | **Contracting entity** with Checkout.com; holding entity | Delaware C-Corp · File No. **7099716** · EIN **92-0927516** · 2100 Geng Road, Suite 210, Palo Alto, CA 94303, USA |
| **Fungies Europe Prosta Spółka Akcyjna** | 100%-owned Polish operating subsidiary — where the team actually sits; **holder of the EUR/PLN settlement account** | KRS **0001137340** · NIP **5214093272** · REGON **540135615** · Al. Jerozolimskie 109/70, 02-011 Warsaw, Poland · incorporated 8 Nov 2024 · share capital PLN 10,000 · PKD 62.01.Z (software) · sole board member: Hoang Duc Vu |

**Ownership / UBO as declared:** Hoang Duc Vu ("Duke", CEO) **55%**; Wojciech Harzowski (co-founder) **40%**; remainder held as pre-conversion SAFE notes.

> ⚠️ **UBO not formally established.** The FY2025 balance sheet states "Common Stock (**0 shares issued**)" and "**No shares have been issued to date**; all investor funding is held as pre-conversion SAFE instruments." The 55/40 split is therefore an **intended, unissued cap table**, not a registered shareholding. A definitive UBO position, cap table and SAFE agreements are needed for onboarding. *(Brief R11)*

> ⚠️ **Settlement to a non-contracting entity.** USD settles to Fungies Inc. (US); **EUR/PLN settles to the Polish subsidiary's account**. Settling to an account not held by the contracting counterparty is third-party settlement. Either the Polish entity is added as a contracting/approved settlement entity with its own KYB, or EUR settles to a Fungies Inc. account. **Resolve before contracting.** *(Brief R4)*

**Screening subjects for the entity check:**

| Name | Role |
|---|---|
| Hoang Duc Vu ("Duke") | CEO, co-founder, 55% declared, sole board member of the Polish entity |
| Wojciech Harzowski | Co-founder, 40% declared |
| Agata Pisarek | Compliance Officer (document owner of all five policies) |
| Christian Jaag | SAFE investor, USD 250,000 (2024) |
| Nguyen Trinh Diep | SAFE investor, USD 100,000 (2025) |
| Tomasz Woźniakowski | SAFE investor, USD 25,000 (2025) |

**Third operating location:** a **Philippines** operations and customer-support team is referenced in the prospect's AML policy (§2) but was **not disclosed** in any of their written answers. Entity/contractor basis, headcount, data-access scope and personal-data transfer basis all unknown. *(Brief R12)*

---

### Legal Entity Name

**Fungies Inc.** (Delaware C-Corporation) — trading as **Fungies.io**.

Contracting entity for Checkout.com. See the entity table above for the Polish operating subsidiary, which is relevant to settlement.

---

### Establishment Year

**Fungies Inc.: not explicitly confirmed by the prospect — to be verified from the certificate of incorporation.**

Best available inference: the FY2024 statement of cash flows shows **cash at beginning of period of USD 0.00**, indicating operations commenced in **2024**; the Delaware file number (7099716) is consistent with incorporation in **2023**. Treat as a **young entity — 2–3 years old at most**.

**Fungies Europe P.S.A.: 8 November 2024** (confirmed).

> Relevant to underwriting: this is an early-stage company on any reading, and the compliance framework (all policies dated Aug 2026) and the volume ramp are both very recent.

---

### Minimum Acceptance Criteria (MAC) details

> **I do not have the current internal MAC document to hand, so I have not asserted pass/fail against specific thresholds.** Set out below is the assessment against the criteria I would expect to apply, with the unmet items and a rationale for each. **Underwriting to confirm against the live MAC.**

**LOB:** Merchant of Record / payment facilitation platform for third-party digital-goods and SaaS sellers. **This is a payments-adjacent LOB, not a straightforward direct seller** — Fungies is the merchant of record for sales made by ~100 (→ ~1,000) underlying third-party sellers. It should be assessed under whichever MAC pathway covers MoR / PayFac / marketplace models, not the standard direct-seller path.

**Likely met:**

| Criterion | Position |
|---|---|
| Product category | SaaS, digital goods, e-books, music/video/software downloads — mainstream digital goods |
| Prohibited categories | Gambling, crypto, NFTs and loot boxes stated as **prohibited on the platform**, no exposure declared *(but see unmet item 5 — the written policy is more permissive than this)* |
| Channel | 100% e-commerce, CNP |
| Chargeback performance | **<0.05%** claimed historically — comfortably inside network programmes *(unevidenced — see unmet item 1)* |
| Target markets | US, EEA, UK + a small India/Canada/Australia tail — core supported markets |
| Volume | ~EUR 12m/year run-rate — commercially material |
| Liability clarity | Fungies confirms **all** chargeback/dispute liability sits with it, not the underlying sellers — our counterparty is unambiguous |

**Not met / unresolved — 8 items:**

**1. No 3-month processing evidence.** The form requires a screenshot of total sales, chargebacks and refunds for the last 3 months. **Not provided.** Duke: the 3–6 month transaction-level export is "still being pulled together — will follow up separately." All processing performance figures below are therefore **prospect assertion only**, including the <0.05% chargeback rate. No refund rate has been given at all — material for digital goods and subscriptions.
*Rationale to proceed:* the data is exportable from the Stripe dashboard in minutes and has been requested; recommend Underwriting treat pre-vet feedback as provisional pending it.

**2. No financial licence, and no legal opinion supporting the MoR construct.** Fungies holds no payment licence, cites no exemption, and operates "via our PSP's infrastructure." Its **own AML policy (§1)** states that whether Fungies is "an MSB, money transmitter, financial institution, or reporting person in any jurisdiction … **must be determined by qualified counsel for the actual funds flow and jurisdictions involved**." No such determination exists.
*Rationale:* Fungies collects end-customer funds, deducts its own fee, withholds tax and settles net to third-party sellers across EEA, UK and US. **This is the single biggest item in the file.** Recommend it be treated as blocking, with an external counsel opinion per jurisdiction required before MAF approval. Consider limiting Phase 1 to jurisdictions the opinion covers. *(Brief R1)*

**3. Financial standing well below any plausible threshold.** FY2025: revenue USD 119,876, net loss USD (232,657), **cash at 31 Dec 2025 of USD 225**, total assets USD 113,982 (99.8% of which is a Stripe receivable), total liabilities nil, no audited accounts. Against this: USD 4.8m/month currently processed, EUR 1m/month proposed, and full MoR chargeback liability.
*Rationale:* Fungies has **no meaningful loss-absorbing capacity** on the accounts provided. Not necessarily fatal — the 2026 ramp may have changed the picture entirely — but the 2026 picture is undocumented. Recommend conditional approval with a security package (rolling reserve + cap, stepped volume caps, re-test at each ramp step) rather than decline. *(Brief R2, §7.4)*

**4. Financial statements do not internally reconcile.** Six breaks, the largest being an accumulated deficit that fails to roll forward by ~USD 243k (opening deficit 146,699 + FY2025 loss 232,657 should give 379,356; reported closing deficit is 136,018), plus a USD 27,616 break between the FY2025 opening cash and the FY2024 closing balance sheet, and nil liabilities against USD 343k of opex.
*Rationale:* with no audited set to fall back on, the management accounts are the only evidence and they do not foot. Restated, internally consistent statements needed — ideally externally reviewed. *(Brief R6, §7.5)*

**5. Written policy is more permissive than the verbal representation on restricted categories.** Duke states crypto is "explicitly prohibited" and does not mention adult content. The KYB Procedure (§2.2) instead places **adult/NSFW, financial services, gambling, crypto and IP-sensitive goods in the "High/restricted" tier — permitted with "specialist written processor approval"**, not prohibited; §1.1 similarly treats adult content as prohibited only "without specialist written approval." The Transaction Monitoring policy (§2) lists adult content as an ongoing monitored category.
*Rationale:* the representation and the policy do not align. Need the actual country-control and prohibited-business lists, plus a **contractual hard exclusion** of specified categories from Checkout.com-processed volume. *(Brief R5)*

**6. No calibrated transaction monitoring in operation.** The Transaction Monitoring policy (§3) requires a **Monitoring Threshold Register**, and states that "**until the register is approved and operational**" a list of scenarios "must be treated as a **manual alert**." §6 goes further: the register and named data sources "**must be attached before external reliance is placed on live automated monitoring claims**." **The register has not been provided.**
*Rationale:* on the prospect's own terms, post-onboarding monitoring is currently **manual and uncalibrated**, across a portfolio going from ~100 to ~1,000 merchants — and we are expressly told not to rely on automated-monitoring claims. Recommend the register be a **launch condition**, and that Fungies' monitoring be given **zero credit** in our risk model until it is delivered. *(Brief R20)*

**7. Compliance framework unapproved and untested.** All five policies are Version 1.0, effective **6–7 August 2026** (one month before our call), and every one carries a **blank approval block** — "Approved by: [CEO / Board approval to be inserted]". Both the AML policy (§7) and the Transaction Monitoring policy (§6) state the policy takes effect **only on approval**. By their own terms, **none of the five is in force**. No case files, QC samples, MI packs or training records provided. Compliance Officer independence is also ambiguous: two policies still read "Compliance Officer / **CEO until a Compliance Officer is appointed**" while naming Agata Pisarek as CO on the cover.
*Rationale:* the design quality is genuinely good; the operating history is close to nil. Countersigned policies plus evidence of operation needed. *(Brief R3, §6)*

**8. Blanket MCC 5734 across 100% of the portfolio.** All ~100 merchants (→ ~1,000) are classified under MCC 5734 "Computer Software Stores", including e-books, music/video downloads and the 30% subscription segment.
*Rationale:* a single MCC across the whole portfolio obscures the digital-content and recurring/continuity population from the networks. Recommend a mapped MCC taxonomy per merchant type as a launch condition. *(Brief R8)*

**Also relevant to MAC assessment:**

- **Second-rail arbitrage risk (Brief R21).** Checkout.com would sit alongside Stripe, creating a structural path for Stripe-declined or offboarded merchants to be routed to us as ordinary "PSP choice." Fungies' own policy (Transaction Monitoring §4) bars moving a merchant "to another payment provider for the same rejected activity" without written provider and CO approval — the right control, but unsigned and enforced by the party with the commercial incentive. Recommend mirroring it contractually with a warranty, notification obligation and audit right.
- **Merchant concentration unknown.** No top-5/top-10 data in any source. On this balance sheet a single large merchant failure could exceed Fungies' entire asset base. *(Brief R15)*
- **10x merchant growth on a one-month-old framework.** ~100 → ~1,000 merchants in 24 months. No compliance headcount or scaling plan provided. *(Brief R10)*
- **PCI DSS position not yet established** — not raised with the prospect. Fungies offers hosted, embedded/overlay and direct-API checkout, so card-data handling varies by mode. SAQ/AOC, level and scope required. *(Brief R18)*

---

### Website / URL

**https://fungies.io**

**Platform-layer products:** hosted checkout, subscription/billing management, API + webhook layer. Merchants integrate via hosted checkout, embedded/overlay checkout, or direct API.

> Note for Underwriting: fungies.io is the **platform's** own site. The actual points of sale are the **~100 underlying seller storefronts**, each with its own domain and checkout. A merchant-domain list has not been requested yet — recommend obtaining one, plus confirmation of which domains would carry Checkout.com volume, since the prospect's own KYB standard (§4.1) requires approval of specific domains and their monitoring policy escalates on "unapproved subdomain" and "undisclosed seller."

---

### Business Offerings (What will CKO be processing for?)

Checkout.com would act as a **direct pay-in processing rail** for Fungies' Merchant of Record flow, paired with a **separate payout provider** on the Fungies side.

**What we would be processing:** card, wallet and APM payments from end consumers buying **SaaS subscriptions and digital goods** (software, e-books, music/video/software downloads, digital content) from third-party sellers on the Fungies platform — with **Fungies Inc. as merchant of record**, i.e. the legal seller to the end customer.

**Commercial rationale:** Fungies is currently 100% on Stripe. It wants a second pay-in rail to (a) remove single-processor dependency and (b) offer its merchants PSP choice. Selected volume would be routed to Checkout.com.

**Mix:**

| Dimension | Split |
|---|---|
| One-off vs. subscription | **70% / 30%** |
| Cards (Visa/Mastercard/Amex) | ~70% |
| Digital wallets (Apple Pay/Google Pay) | ~20% |
| Local APMs (iDEAL, SEPA, etc. — EEA) | ~10% |
| Channel | 100% e-commerce, CNP |
| MCC | 5734 (100% of portfolio — see MAC item 8) |

**Explicitly excluded by the prospect:** gambling, crypto, NFTs, loot boxes *(see MAC item 5 — the written policy is looser than this)*.

**Architecture note.** Their current Stripe model uses **direct charges on Express connected sub-accounts**, where the charge lands on the seller's sub-account while Fungies nonetheless asserts full MoR liability. **There is no equivalent connected-account construct on Checkout.com** — Fungies would be the merchant on our platform under its own MID(s), with the payout leg handled by the separate payout provider. This is architecturally cleaner and matches their stated liability position, but it is a **redesign, not a port**, and should lead the Solutions Engineering session. *(Brief R17, §9.2)*

---

### Currently processing online

**Yes — 100% via Stripe** (Stripe Connect, Express connected accounts, direct charges, plus Stripe Billing and PaymentIntents).

| Metric | Value | As of |
|---|---|---|
| Total processing volume | **USD 4.8m/month** | End July 2026 |
| Prior data point | USD 2.4m/month | Mid-June 2026 |
| Growth | **2x in ~6 weeks** | — |
| Payout volume to sellers | USD 4.4m/month | — |
| Payout count | ~2,694/month | — |
| ATV | **USD 60–63** | — |
| Chargeback rate | **<0.05%** historically | — |
| Refund rate | **Not provided** | — |
| Active merchants | ~100 | — |

> ⚠️ **REQUIRED DOCUMENT NOT PROVIDED.** The form requires "a screenshot showing total sales, chargebacks & refunds for the last 3 months." **Not supplied.** Duke: the 3–6 month export (volume, counts, refunds, disputes, fraud, acceptance/auth rates with definitions) is "still being pulled together — will follow up separately." Requested; chasing.

> ⚠️ **Three data reconciliation issues Underwriting should be aware of** (full detail in Brief §10):
>
> **(a) FY2025 revenue vs. current volume.** FY2025 revenue of USD 119,876 implies average FY2025 volume of roughly USD 170–200k/month at their 5% + $0.50 take-rate. Current stated volume is USD 4.8m/month — **~24x growth in ~19 months**, essentially all in 2026, and **entirely undocumented**. The whole commercial and credit case rests on it. *(Brief R7)*
>
> **(b) Payout volume vs. tax withholding — ~USD 800k/month unexplained.** Payouts of USD 4.4m on USD 4.8m volume = sellers receive **91.7% of gross**. But the prospect's **own fund flow diagram** works an example ($12.00 charge = $10.00 net sale + $2.00 tax, less $0.50 + 5% fee) in which the seller nets **74–75% of gross** — implying payouts of ~USD 3.6m, not USD 4.4m. Either the volume/payout figures mean something other than stated, or **MoR tax is not being collected and remitted at the rates the model requires**. The latter would undercut the MoR tax representation the whole structure rests on. **Recommend this be put as a specific named question and resolved before MAF.** *(Brief R14, §10.2)*
>
> **(c) Payout count vs. merchant count.** ~2,694 payouts/month across ~100 merchants = **~27 payouts per merchant per month**, i.e. roughly daily — inconsistent with the stated T+7 weekly-eligibility cycle, which would produce ~400–430/month. Either the active-merchant count is materially higher than 100 (e.g. individual creators beneath merchant accounts), or payouts are far more granular than described. Affects how we size the population and the KYB burden. *(Brief §10.3)*

---

### Volume ($): Annual volume to be processed via CKO

**Run-rate target: EUR 12m/year (~EUR 1m/month).**
**Year 1 (Dec 2026 – Nov 2027): ~EUR 9.3m** — full run-rate reached from month 6.

| Month | Volume (EUR) | % of run-rate |
|---|---|---|
| Dec 2026 (launch) | 150,000 | 15% |
| Jan 2027 | 300,000 | 30% |
| Feb 2027 | 450,000 | 45% |
| Mar 2027 | 600,000 | 60% |
| Apr 2027 | 800,000 | 80% |
| May 2027 onward | 1,000,000/month | 100% |
| **Year 1 total** | **~9,300,000** | — |

*Ramp arithmetic verified: 150 + 300 + 450 + 600 + 800 + (7 × 1,000) = EUR 9,300k.*

**Derived transaction volume** at USD 60–63 ATV: ~**150k–160k transactions** in Year 1; ~**16k/month** at full run-rate.

**Context:** the EUR 12m is a **slice** of Fungies' total platform volume (USD 4.8m/month ≈ USD 57.6m/year), not the whole book. Fungies remains on Stripe for the balance.

> **Note for commercial sizing:** the monthly minimum commitment should be **stepped against the ramp**, not set against the EUR 12m endpoint — Year 1 is ~EUR 9.3m and the first four months are at 15–60% of run-rate.

---

### Target markets

**Buyer / shopper geography (where the cardholders are — what we would be acquiring):**

| Region | Share | Currency |
|---|---|---|
| **US** | **60%** | USD |
| **EEA** | **30%** | EUR |
| India / Canada / Australia | 10% | INR / CAD / AUD |

**Seller / merchant geography (where the underlying sellers are):**

| Region | Share |
|---|---|
| EEA | 40% |
| UK | 20% |
| US | 10% |
| **Hong Kong** | **10%** |
| **Indonesia / Singapore / India** | **10%** |
| Canada / Australia | 10% |

> ⚠️ **Cross-border seller/buyer mismatch.** 30% of sellers sit in APAC (Hong Kong, Indonesia, Singapore, India) while 90% of buyers are US/EEA. Under MoR the acceptance geography follows Fungies' entity, but the underlying **seller-country risk is real** and should be visible in our risk model — Hong Kong and Indonesia seller exposure in particular warrants EDD. The prospect's own AML policy (§4) requires exactly this check ("a geographic mismatch between merchant registration, website targeting, customer countries, payout country, IP/access data, or expected activity requires enhanced review"); we should ask for evidence it operates. *(Brief R13)*

> ⚠️ **MoR jurisdictions claimed on the call do not match the written data.** On the discovery call Fungies described operating as MoR across **UAE, EEA, UK, US and Korea**. Neither **UAE nor Korea** appears anywhere in the written entity, seller or buyer data, and there is no entity in either. Clarify whether this reflects tax-registration footprint, planned expansion, or an undisclosed arrangement. *(Brief R19)*

**Country-control list:** referenced in the prospect's AML policy (§4) as maintained and CO-approved, identifying prohibited, restricted and EDD jurisdictions. **Not provided** — requested.

---

### Financial Details (fundraising, government / investor backing)

**Stage:** seed / pre-priced-round. **No government backing. No institutional VC.** All funding to date is founder-led angel money held as **pre-conversion SAFE instruments** — **no shares have been issued**.

| Investor | Amount | Period |
|---|---|---|
| Christian Jaag | USD 250,000 | 2024 |
| Nguyen Trinh Diep | USD 100,000 | 2025 |
| Tomasz Woźniakowski | USD 25,000 | 2025 |
| UNIT (banking advance) | USD 20,000 | 2024 |
| Unattributed "seed wire" (per cash-flow note) | USD 125,000 | 2025 |

**Carried on the balance sheet at USD 250,000** (2024: USD 270,000), described as "net of conversions."

> ⚠️ **SAFE reconciliation unexplained.** The named instruments total **USD 395,000**, plus a separately referenced **USD 125,000** seed wire — against **USD 250,000** carried. "Net of conversions" is asserted, but the same balance sheet states **no shares have been issued**, so there is nothing for the SAFEs to have converted into.

**Capital raised:** USD 250,000 in FY2025; USD 270,000 in FY2024. **No evidence of any post-31-December-2025 funding round has been provided** — material, given cash of USD 225 at that date.

**Banking:** Mercury Bank and Brex (US).

---

### Financial licence

**No.** Fungies holds **no payment or financial licence in any jurisdiction.**

Duke, verbatim: *"No independent payment license held; we operate via our PSP's infrastructure (currently Stripe, with Checkout.com to be added as a second pay-in rail under the same model)."*

I specifically asked whether the operating basis was (i) a financial licence, (ii) a legal exemption, (iii) a collection-agent agreement, or (iv) the PSP's infrastructure. The answer was **(iv) only** — no licence, no cited exemption, no collection-agent structure.

**MoR construct as described:** Fungies contracts as legal seller of record, enforced by a hard requirement that **every merchant's own terms & conditions explicitly name Fungies as Merchant of Record**. Tax collected as MoR is held separately, is not Fungies revenue, and is remitted to the end customer's jurisdiction.

> ⚠️ **The prospect's own AML policy says this question is unresolved.** Section 1: *"This policy is an operational control document. It does not itself determine whether Fungies.io is an MSB, money transmitter, financial institution, or reporting person in any jurisdiction. Regulatory status, SAR obligations, OFAC reporting obligations, and licensing requirements **must be determined by qualified counsel for the actual funds flow and jurisdictions involved**."*
>
> **No counsel opinion has been provided or, as far as I can establish, obtained.** Fungies collects end-customer funds, deducts its own fee, withholds tax and settles net to third-party sellers across the EEA, UK and US — a flow which, absent a licence, exemption or properly structured agency arrangement, can constitute regulated payment or money-transmission activity in several of those markets. Under the proposed model Checkout.com would be the acquirer whose infrastructure carries it.
>
> **Recommend treating as blocking:** external counsel opinion covering the actual funds flow per jurisdiction, reviewed by our Legal/Compliance, before MAF approval. *(Brief R1)*

Also note: the AML policy positions Fungies as **non-reporting**, relying on the regulated counterparty — *"Where Stripe, a bank, acquirer, payment processor, or another regulated counterparty is the reporting institution, Fungies.io will provide complete and timely evidence and cooperate."* Directly relevant to what we would be expected to absorb.

---

### Type of financial licence held

**N/A — none held.** See above.

---

### Policies in place

**Six documents supplied. Five are internal compliance policies; the sixth is the fund flow diagram (next field).** All five policies are authored by Agata Pisarek (Compliance Officer), classified "Internal — Compliance Controlled Document", **Version 1.0**.

| # | Policy | Effective | Review cycle |
|---|---|---|---|
| 1 | **AML, Sanctions & Geographic Controls Policy** | 7 Aug 2026 | Annual + on material change |
| 2 | **KYB Procedure** (Sumsub-supported business & beneficial-owner verification) | 6 Aug 2026 | Quarterly |
| 3 | **KYC Procedure** (Didit-supported individual identity verification) | 6 Aug 2026 | Quarterly |
| 4 | **Refund, Dispute, Reserve & Settlement Policy** | 7 Aug 2026 | Quarterly |
| 5 | **Transaction Monitoring & Merchant Risk Policy** | 7 Aug 2026 | Quarterly (thresholds) / annual (policy) |

**Vendor stack:** **Didit** for individual KYC (ID document, liveness/face-match, device/IP signals, configurable AML screening); **Sumsub** for KYB (corporate registry, ownership/control, UBO/director verification, questionnaires, document review, AML screening). Both are used as **evidence, not decision** — Fungies retains final acceptance in its internal Admin Panel.

**Substantive strengths (genuinely better than the company's stage would suggest):**

- **Right hard stops.** No activation on a registry match, revenue opportunity or completed provider check alone. No KYC waiver "because of revenue potential, sales urgency, a referral, prior platform use, or an applicant's promise to provide documents later."
- **Sales/compliance separation.** Commercial personnel may collect information but **may not override a compliance decline, payout hold, suspension or exit decision**. "Commercial targets must not influence a compliance decision."
- **Transaction-laundering awareness** throughout — explicit controls against one approved business processing for another company, website, product or seller, with linked-account review across common owners, devices, domains, support contacts, fulfilment and traffic sources.
- **Payout-beneficiary controls.** Accounts must be in the seller's legal name and verified before use; changes require authorised request, ownership verification and a **security hold**; unapproved third-party payout accounts prohibited.
- **Real reserve and set-off machinery.** 10% rolling reserve permitted under the sample MoR agreement; deduction, withholding and set-off against seller settlement for refunds, chargebacks, disputes, fees, penalties, taxes, FX; **no payout release that would create or worsen a known unpaid refund, chargeback, reserve shortfall, sanctions hold or processor restriction**.
- **Anti-PSP-arbitrage clause** (Transaction Monitoring §4) — a merchant may not be "moved to another payment provider for the same rejected activity" without written provider and CO approval. This pre-empts the main structural risk of the deal.
- **Unusual drafting candour.** Twice the policies constrain what Fungies may claim to us (the counsel deferral on money transmission; the bar on relying on automated-monitoring claims). Documents written purely to pass diligence do not usually include the sentences that undercut them.

**Weaknesses — all four are about substantiation, not design:**

> ⚠️ **1. None of the five policies is formally in force.** Every one carries a blank approval block — "Approved by: **[CEO / Board approval to be inserted]**" — with `[Insert]` in the CO, CEO and Board signature and date fields. AML §7: *"This policy becomes effective only after the approving authority signs or digitally approves it."* Transaction Monitoring §6 repeats it. **Request countersigned versions.**

> ⚠️ **2. Effective dates are 6–7 August 2026 — one month before our call.** Combined with Version 1.0 across the board and no case files, QC samples, MI packs or training records, the reasonable read is that this framework was **written for this diligence exercise** and has little or no operating history. Request evidence of operation.

> ⚠️ **3. No calibrated monitoring in operation.** Transaction Monitoring §3 requires a **Monitoring Threshold Register** (thresholds, owners, effective dates, data sources, alert severity, response timelines, closure requirements, "calibrated to the actual processor, merchant category, portfolio, and card-network programme rather than copied from a generic policy"), and states that **until it is "approved and operational" a list of scenarios must be treated as a manual alert**. §6: the register and named data sources "**must be attached before external reliance is placed on live automated monitoring claims**." **The register has not been provided.** *(Brief R20 — recommend launch condition + zero monitoring credit until delivered.)*

> ⚠️ **4. Compliance Officer independence ambiguous.** The KYB and KYC procedures both state the policy owner is "Compliance Officer / **CEO until a Compliance Officer is appointed**", and the KYC procedure refers to reporting "to the CEO and, **once appointed**, the Compliance Officer" — while naming Agata Pisarek as CO on the same documents' covers. Needs a direct answer: is the role independently staffed, and since when?

**Also not provided, though referenced inside the policies:** the country-control list (AML §4), the prohibited-business list, the Monitoring Threshold Register (TM §3), the sample MoR/seller agreement and customer terms (relied on repeatedly in the Refund/Dispute/Reserve policy, including for the 10% rolling reserve), and the monthly compliance MI packs and QC samples (TM §5).

---

### Funds flow diagram

**Provided** — *"Fungies.io — Merchant of Record Fund Flow · Stripe Connect — Direct Charge Model."* Given the MoR LOB, a funds flow is required, and the prospect's own KYB standard also requires a funds-flow map per merchant.

**Flow as diagrammed, with the prospect's worked example:**

```
End customer (card / wallet / APM)
        │  $12.00 customer charge
        │  = $10.00 net sale + $2.00 VAT / GST / Sales Tax
        ▼
Charge created DIRECTLY on Seller's Stripe Express Sub-Account (Direct Charge)
        │
        ▼
$0.50 + 5% Fungies platform fee  (deducted as Stripe Application Fee)  ──► Fungies Inc.
        │                                                                  (Mercury / Brex)
        ├──────────────────────────────┬──────────────────────────────────┐
        ▼                              ▼
Net Seller Balance            $2.00 Tax Collected & Held
(gross − Fungies fee − tax)   ("Not Fungies revenue")
        │                              │
        ▼                              ▼
Seller's Stripe Express        Tax Remittance to Tax Authority
Sub-Account Balance            (End Customer's country / jurisdiction)
        │
        ▼
Payout to Seller's Bank
(SEPA / Wire / ACH — 99%; remainder push-to-card: Visa Direct, Mastercard Send)
```

**Payout cycle:** automatic business-day cycle after the prior seven days have settled and become eligible (**T+7**), subject to payment-method settlement timing, bank cut-offs, reserve requirements and contractual withholding.

**Liability split — confirmed unambiguously by the prospect (verbatim):**

> *"Fungies is responsible for **all** chargebacks, disputes, and related liability as Merchant of Record — this sits with us directly, not the underlying merchant, from a network/processor-facing perspective. Internally, our merchant agreement allows us to recover the economic cost of a chargeback or dispute from the responsible merchant's settlement (via a per-transaction chargeback fee and net-settlement deduction), but the liability itself — to Checkout.com, to the card networks, to the end customer — is **ours alone**."*

This is the correct MoR answer and clean from a contracting standpoint: **our counterparty is Fungies, full stop.** It also means our credit exposure is to Fungies' balance sheet — with seller recovery as a second-order mitigant only, which is exactly why MAC item 3 matters.

**Three observations:**

**(a) Tax treatment is correct in principle.** Tax is added *on top* of the seller's list price rather than carved out of it, labelled "Not Fungies revenue", held separately, and remitted to the **end customer's** jurisdiction.

**(b) ⚠️ The diagram's own economics contradict the reported payout ratio.** On the worked example the seller nets **$8.90–$9.00 of a $12.00 gross charge (74–75%)**. Fungies reports paying out **91.7%** (USD 4.4m of 4.8m). At the diagram's economics, payouts on USD 4.8m would be ~**USD 3.6m** — a gap of roughly **USD 800k/month**. See the "Currently processing online" field, note (b). **This is the item I would most want Underwriting to press on**, because one of the candidate explanations is that MoR tax is not being collected and remitted as represented. *(Brief R14)*

**(c) Fee base ambiguous.** The diagram does not state whether the 5% is struck on the **gross charge including tax** ($12.00 → $1.10 total fee) or on the **net sale** ($10.00 → $1.00). The fixed $0.50 makes the effective rate highly ticket-sensitive: ~**10–11% at a $10 ticket** vs. ~**5.83% at the stated $60 ATV**. Note also that the example ticket ($10–12) sits far below the stated ATV. Confirm before we benchmark pricing.

**Target-state flow (Checkout.com + separate payout provider): to be designed.** Duke has offered to adapt the diagram once our payout provider is confirmed. Open design points for the Solutions Engineering session: MID structure (and whether split by geography, currency or vertical); where the fee and tax split occurs given there is no application-fee equivalent; handoff and reconciliation with the payout provider; interaction between a Checkout.com-held reserve and Fungies' own 10% rolling reserve on sellers; negative-balance and run-off handling; dispute flow within network time limits; and multi-currency handling including the 10% INR/CAD/AUD tail.

---

### Financial Statements

**Provided: Fungies Inc. FY2025 financial statements (P&L, Balance Sheet, Statement of Cash Flows), FY2025 vs FY2024 comparative, USD, Delaware entity.**

**Status: unaudited management accounts.** Duke was upfront: *"These are unaudited management accounts (we don't have independently audited financials, so this satisfies the 'or balance sheet/P&L' alternative from your ask)."* The statements themselves carry the note *"This statement has not been independently audited. Prepared for internal management and investor reporting purposes only."* FY2024 figures are described as sourced from "audited management accounts" — an ambiguous phrase worth clarifying.

**Profit & Loss (USD)**

| Line item | FY 2025 | FY 2024 | YoY |
|---|---|---|---|
| Platform revenue (Stripe / SaaS) | 119,876.00 | 87,375.70 | +37.2% |
| **Total revenue** | **119,876.00** | **87,375.70** | **+37.2%** |
| Cloud hosting & infrastructure (AWS) | (9,756.08) | (379.97) | +2,467.6% |
| **Gross profit** | **110,119.92** | **86,995.73** | **+26.6%** |
| Personnel & contractors | (240,524.04) | (163,717.30) | +46.9% |
| SaaS & software subscriptions | (40,558.57) | (31,945.81) | +27.0% |
| Advertising & marketing | (17,951.00) | (25,766.51) | −30.3% |
| Travel & entertainment | (16,271.75) | (9,518.08) | +71.0% |
| Banking & wire transfer fees | (974.41) | (449.56) | +116.7% |
| Other G&A | (26,497.16) | (4,869.19) | +444.2% |
| **Total operating expenses** | **(342,776.92)** | **(236,266.45)** | **+45.1%** |
| **Net income / (loss)** | **(232,657.00)** | **(149,270.72)** | **−55.9%** |

**Important:** revenue is **net platform fee revenue**, not gross MoR volume. Duke flagged this himself — *"we only keep the 5% + $0.50 fee, not the full transaction amount."* Correct, and worth noting he volunteered it.

**Balance Sheet (USD)**

| Line item | 31 Dec 2025 | 31 Dec 2024 |
|---|---|---|
| Cash & cash equivalents | **225.00** | 124,254.78 |
| Stripe account (receivable) | 113,757.00 | 0.00 |
| Accounts receivable / prepaid | 0.00 | 0.00 |
| **Total assets** | **113,982.00** | **124,254.78** |
| **Total liabilities** | **0.00** | **0.00** |
| Common stock (0 shares issued) | 0.00 | 0.00 |
| SAFE notes & seed (pre-conversion) | 250,000.00 | 270,000.00 |
| Retained earnings / (accumulated deficit) | (136,018.00) | (146,698.86) |
| **Total stockholders' equity** | **113,982.00** | **123,301.14** |

**Statement of Cash Flows (USD)**

| Line item | FY 2025 | FY 2024 |
|---|---|---|
| Net income / (loss) | (232,657.00) | (149,270.72) |
| Increase in Stripe receivable | (113,757.00) | 0.00 |
| **Net cash from operating** | **(346,414.00)** | **(149,270.72)** |
| Net cash from investing | 0.00 | 0.00 |
| Proceeds from SAFE notes & seed | 250,000.00 | 270,000.00 |
| **Net change in cash** | **(96,414.00)** | **120,729.28** |
| Cash at beginning of period | 96,639.00 | 0.00 |
| **Cash at end of period** | **225.00** | **124,254.78** |

**Credit summary**

| Factor | Reading |
|---|---|
| **Liquidity** | **USD 225** at 31 Dec 2025 against FY2025 net cash burn of USD 346k — effectively **zero runway** at year-end absent post-YE funding or the 2026 ramp |
| **Total assets** | **USD 113,982**, of which **99.8% is a receivable from Stripe** — a claim on the incumbent processor, not free cash |
| **Liabilities** | Nil reported. Nil AP and nil accrued expenses against USD 343k of annual opex is implausible and suggests incomplete accrual accounting |
| **Funding** | USD 250k carried as pre-conversion SAFEs; seed-stage, no priced round, no shares issued, no evidence of post-YE2025 raise |
| **Profitability** | Loss-making both years, widening (−55.9%); opex is 2.9x revenue |
| **Audit** | **No independently audited financials exist** |
| **Capacity vs. exposure** | **The core issue.** Total assets of ~USD 114k and cash of USD 225 against USD 4.8m/month currently processed, EUR 1m/month proposed, and **full MoR chargeback liability confirmed as Fungies' alone**. Fungies can pass economic cost to sellers contractually, but cannot absorb a loss that outruns seller recovery — a merchant failure, a mass-fraud event, a portfolio dispute spike, or an insolvent seller with a negative balance |

> ⚠️ **Six internal inconsistencies** (full detail in Brief §7.5). These matter because there are no audited accounts to fall back on — the management accounts are the only evidence, and they do not tie:
>
> 1. **Accumulated deficit does not roll forward.** Opening (146,698.86) + FY2025 loss (232,657.00) = **(379,355.86)**; reported closing deficit is **(136,018.00)** — ~USD 243k unexplained, and the closing deficit is *smaller* than the prior year's despite a full-year loss.
> 2. **Cash flow opening balance breaks against the prior balance sheet.** FY2025 opening cash 96,639.00 vs. FY2024 closing 124,254.78 — a **USD 27,616** break.
> 3. **FY2024 cash flow does not foot.** 0.00 + 120,729.28 = 120,729.28 vs. reported closing 124,254.78 — a **USD 3,525** break.
> 4. **SAFE reconciliation.** Named instruments total USD 395k (+ a USD 125k seed wire) against USD 250k carried; "net of conversions" asserted while the same statement says no shares have been issued.
> 5. **Equity composition.** Foots arithmetically (250,000 − 136,018 = 113,982) but to a deficit figure that is itself unsupported per item 1.
> 6. **Nil liabilities** in both years despite USD 343k opex and a subscription-billing business that would normally generate deferred revenue.
>
> **Request:** restated, internally consistent statements — ideally externally reviewed — plus **2026 YTD management accounts and bank/Stripe statements**. The 2026 position is the entire credit case and is currently supported only by figures in an email. *(Brief R6, R7)*

---

## Recommendation to Underwriting

**Recommend proceeding to a conditional assessment rather than either a straight decline or a standard MAF path.**

The commercial case is real (EUR 12m run-rate, PSP-diversification driver, a vertical we know), the liability position is clean and unambiguous (Fungies alone, confirmed in writing), and the compliance framework is well designed. The prospect has also been responsive and candid — volunteering the revenue-vs-volume distinction, sending an unprompted follow-up to close the gaps he had left thin, and not overstating the audit status of the financials.

The problem is uniformly one of **substantiation**: almost every control is well conceived and **none is yet evidenced as operating**.

**Blocking for MAF:**

1. **R1 — Legal basis for the MoR construct.** No licence, no exemption, no counsel opinion — and the prospect's own AML policy says the money-transmission determination is owed to counsel and has not been made. Requires an external opinion per jurisdiction, reviewed by our Legal/Compliance.
2. **R2 / R6 — Financial standing.** USD 225 cash, USD 114k assets (99.8% a Stripe receivable), no audited accounts, and the accounts that exist do not internally reconcile. Requires restated statements plus 2026 YTD with bank/Stripe corroboration.

**Launch conditions:**

3. **R14 — Tax reconciliation.** ~USD 800k/month unexplained between the reported payout ratio and the prospect's own fund flow economics. Needs a named answer plus tax registrations and remittance evidence.
4. **R20 — Monitoring Threshold Register.** Until delivered, Fungies' post-onboarding monitoring should be given **zero credit** in our risk model, on the authority of their own policy.
5. **R8 — MCC taxonomy** mapped per merchant type, replacing blanket 5734.
6. **R5 — Contractual hard exclusion** of adult/NSFW, gambling, crypto and other restricted categories from Checkout.com volume, reconciling the policy-vs-representation gap.
7. **R3 — Countersigned policies** plus evidence of operation (case files, monthly QC samples, MI packs, training records).
8. **R4 — Settlement-entity structure** resolved (EUR settling to a non-contracting entity).

**Contractual must-have specific to this architecture:**

9. **R21 — Anti-PSP-arbitrage protection.** Warranty and ongoing notification that no merchant declined, suspended, offboarded or limited by Stripe (or any other provider) for risk or compliance reasons is routed to Checkout.com volume without our prior written approval; audit right; breach as a termination trigger. This is the defining structural risk of being the second rail, and the prospect has already conceded the principle in their own policy.

**Security package to be designed into the first proposal, not retrofitted:** rolling reserve with a defined cap, volume caps stepped by ramp month with re-test at each step, and concentration limits (top-merchant data still outstanding). Consider a founder or parent guarantee, or a deposit, given the balance sheet.

**Commercial note:** size the proposal against **~EUR 9.3m Year 1**, not the EUR 12m endpoint, and step the monthly minimum commitment with the ramp.

**Parallel track:** the Solutions Engineering session should proceed now regardless of the risk timeline — it de-risks the December 2026 launch date and the two items on the critical path (the architecture redesign, and whether stored payment credentials need migrating from Stripe, which would require network token/PAN migration involving both processors).

---

## Outstanding items requested from the prospect

**Requested and explicitly deferred by Fungies:**

1. 3–6 month Stripe processing export — volume, counts, refunds, disputes, fraud, acceptance/auth rates with definitions *(the pre-vet form's required 3-month screenshot)*
2. Stripe scope & migration — exact products in use; whether the 30% subscription volume is new-subscriptions-only or includes stored-credential migration

**Asked but not answered:**

3. **Effective Stripe pricing** broken out by processing, Connect, payout, fixed and FX — they answered with their own sell-side price instead. **We do not know their cost base, margin or price sensitivity. Top commercial priority.**
4. Legal opinion on the MoR construct *(R1)*
5. Country-control list and prohibited-business list
6. FX requirement — processing-currency settlement vs. conversion
7. INR / CAD / AUD settlement treatment (10% of volume)
8. Definitive UBO position, cap table, SAFE agreements

**Not yet raised — recommend adding to the next request:**

9. Monitoring Threshold Register, named data sources and dashboard reports *(R20)*
10. Tax registrations (US states, EU OSS/IOSS, UK VAT) + gross→tax→fees→payouts reconciliation for one recent month *(R14)*
11. Confirmation of the 5% fee base (gross incl. tax vs. net sale) and the ATV distribution
12. Corporate documents — Delaware certificate of incorporation and good standing, KRS extract
13. Sample MoR/seller agreement and customer terms
14. 2026 YTD financials, bank and Stripe statements, evidence of post-YE2025 funding
15. Countersigned policies + evidence of operation (case files, QC samples, MI packs, training records)
16. Compliance Officer status — independently staffed, and since when?
17. Philippines operations — entity/contractor basis, headcount, access scope, data-transfer basis
18. PCI DSS — SAQ/AOC, level, scope; which integration modes carry Checkout.com volume
19. Merchant concentration — top 5 / top 10 as % of volume
20. Refund rate (distinct from chargeback rate)
21. Insurance — E&O / cyber / crime cover
22. Merchant domain list, and which domains would carry Checkout.com volume
23. NDA execution status (sent via DocuSign — confirm before further exchange)
