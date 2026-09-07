# Fungies.io — Master Opportunity & Pre-Vet Brief

**Prospect:** Fungies Inc. / Fungies.io
**Opportunity:** Direct pay-in processing partner (Merchant of Record platform)
**Deal owner:** Giacomo Staffieri, Checkout.com
**Prospect contact:** Hoang Duc Vu ("Duke"), CEO & Co-founder
**Document date:** 7 September 2026
**Status:** Pre-vet / initial risk assessment — information gathering substantially complete, gaps listed in §11
**Classification:** Confidential — internal Checkout.com use only. Contains Fungies confidential information (received under NDA) and third-party personal data (UBOs, SAFE investors). Handle per internal data-handling rules.

---

## 1. Document purpose and provenance

This document consolidates everything currently known about Fungies.io into a single reference for the pre-vet form, the risk review, the solution design, and the commercial proposal.

**Sources:**

| # | Source | Date | Type |
|---|---|---|---|
| S1 | Discovery call with Duke Vu (CEO) | w/c 31 Aug 2026 | Call |
| S2 | Giacomo → Duke recap email + information request | Post-call | Email |
| S3 | Duke → Giacomo primary response (all 3 sections) | Post-call | Email |
| S4 | Duke → Giacomo follow-up (merchant counts, MCC, settlement banks, liability split, volume forecast) | Post-call | Email |
| S5 | Fungies Inc. Financial Statements FY2025 (P&L, Balance Sheet, Cash Flow) | FY2025, unaudited | PDF |
| S6 | Fungies Internal AML, Sanctions & Geographic Controls Policy v1.0 | Eff. 7 Aug 2026 | PDF |
| S7 | Fungies Internal KYB Procedure (Sumsub-supported) v1.0 | Eff. 6 Aug 2026 | PDF |
| S8 | Fungies Internal KYC Procedure (Didit-supported) v1.0 | Eff. 6 Aug 2026 | PDF |
| S9 | Fungies Internal Refund, Dispute, Reserve & Settlement Policy v1.0 | Eff. 7 Aug 2026 | PDF |
| S10 | Fungies Internal Transaction Monitoring & Merchant Risk Policy v1.0 | Eff. 7 Aug 2026 | PDF |
| S11 | Fungies.io MoR Fund Flow diagram (Stripe Connect — Direct Charge Model) | — | Image |
| S12 | Checkout.com Pre-vet Form for Direct Sellers (internal) | — | PDF |

**All Fungies-provided attachments have now been received.** The completed pre-vet form is a companion deliverable to this brief (`FUNGIES_IO_PREVET_FORM.md`).

Where a figure appears in more than one source with different values, both are shown and the discrepancy is flagged in §10.

---

## 2. Executive summary

Fungies.io is an early-stage (Delaware-incorporated, Warsaw-operated) Merchant of Record and monetisation platform for SaaS and digital-goods sellers. It provides hosted checkout, subscription billing, tax handling as MoR, and seller payouts, today entirely on Stripe Connect (direct charges, Express connected accounts). It monetises via a single blended fee of **5% + $0.50 per transaction**, all-inclusive.

**The ask:** add Checkout.com as a **second direct pay-in rail** alongside Stripe, paired with a separate payout provider, so that Fungies can offer its merchants PSP choice and diversify away from single-processor dependency.

**Commercial shape:**

| Parameter | Value |
|---|---|
| Target Checkout.com volume | ~**EUR 12m/year** at full run-rate (~EUR 1m/month) |
| Year 1 volume (Dec'26–Nov'27) | ~**EUR 9.3m** (6-month ramp) |
| Target launch | **December 2026** |
| Mix | 70% one-off / 30% subscription |
| ATV | **USD 60–63** (S3/S4); ~EUR 65 quoted on call (S2) |
| Implied Year-1 transaction count | ~150k–160k transactions |
| Current total platform volume (all rails) | **USD 4.8m/month** as of end July 2026 |
| Commercial construct discussed | Tiered pricing against a **monthly minimum commitment** |

**Headline assessment:** commercially attractive and strategically clean (MoR platform, PSP-diversification driver, digital-goods vertical we know well), but the risk profile is **materially front-loaded**. Four items dominate:

1. **No payment licence and no legal opinion** supporting the MoR construct — and Fungies' own AML policy says that determination is owed to counsel and has not been made.
2. A **balance sheet with effectively zero liquidity** (USD 225 cash at YE2025, USD 114k total assets, no audited accounts, and figures that do not internally reconcile) against MoR chargeback and refund liability that Fungies has confirmed sits **entirely with it**.
3. A **compliance framework that is one month old, version 1.0, and formally unapproved** — all five policies carry blank CEO/Board signature blocks, and each states it takes effect only on approval.
4. **No calibrated transaction monitoring in operation.** The Transaction Monitoring policy states that until its Monitoring Threshold Register is "approved and operational" everything is a **manual alert**, and warns expressly that the register and named data sources "must be attached **before external reliance is placed on live automated monitoring claims**." The register has not been provided.

See §10 and §12.

---

## 3. Corporate and legal structure

### 3.1 Contracting entity — Fungies Inc. (US)

| Field | Detail |
|---|---|
| Legal name | **Fungies Inc.** |
| Form | Delaware C-Corporation |
| Delaware File No. | 7099716 |
| EIN | 92-0927516 |
| Registered address | 2100 Geng Road, Suite 210, Palo Alto, CA 94303, USA |
| Role | **Contracting entity with Checkout.com**; holding entity |
| Banking | Mercury Bank and Brex (per S5 notes) |
| Settlement account | US bank account, USD |

**Ownership / UBO (as declared, S3):**

| Holder | Stake | Notes |
|---|---|---|
| Hoang Duc Vu ("Duke") | 55% | CEO, co-founder; also sole board member of the Polish entity |
| Wojciech Harzowski | 40% | Co-founder |
| Remainder | — | Held as **pre-conversion SAFE notes — no shares issued yet** |

> **Flag (UBO):** S5 states "Common Stock (0 shares issued) $0.00" and "No shares have been issued to date; all investor funding is held as pre-conversion SAFE instruments." The declared 55/40 split is therefore an **intended/unissued cap table**, not a registered shareholding. We need a definitive UBO position for onboarding — see §11.

**SAFE / seed investors identified in S5 notes:**

| Investor | Amount | Period |
|---|---|---|
| Christian Jaag | USD 250,000 | 2024 |
| Nguyen Trinh Diep | USD 100,000 | 2025 |
| Tomasz Wozniakowski | USD 25,000 | 2025 |
| UNIT (banking advance) | USD 20,000 | 2024 |
| Unattributed "seed wire" (cash-flow note) | USD 125,000 | 2025 |

Carrying value on the balance sheet is **USD 250,000** (2025) / USD 270,000 (2024), described as "net of conversions" — the gross of the named instruments exceeds this. See §10.

### 3.2 Operating entity — Fungies Europe P.S.A. (Poland)

| Field | Detail |
|---|---|
| Legal name | **Fungies Europe Prosta Spółka Akcyjna** (Simple Joint-Stock Company) |
| Ownership | 100% owned by Fungies Inc. |
| KRS | 0001137340 |
| NIP | 5214093272 |
| REGON | 540135615 |
| Incorporated | 8 November 2024 |
| Registered seat | Al. Jerozolimskie 109/70, 02-011 Warsaw, Poland |
| Share capital | PLN 10,000 (1,000,000 ordinary shares, no preference) |
| Sole management board member | Hoang Duc Vu (Prezes Zarządu / President of the Board) |
| Registered activity (PKD) | **62.01.Z — computer programming / software activities** |
| Role | Operating entity — "where our actual team sits and operates day to day" |
| Settlement account | Poland bank account, EUR/PLN |

> **Flag (settlement structure):** the **contracting entity is US** (Fungies Inc.) but EUR/PLN settlement is to a **Polish subsidiary's** account. Settling to an account not held by the contracting counterparty is a third-party-settlement issue. Either Fungies Europe P.S.A. is added as a contracting party / approved settlement entity with its own KYB, or EUR settles to a Fungies Inc. EUR account. Must be resolved before contracting — see §12 R4.

> **Flag (registered activity):** PKD 62.01.Z covers software development, not payment or payment-adjacent services. Worth confirming with counsel whether the Polish entity's registered scope covers the MoR/collection activity it performs.

### 3.3 Operational footprint (three countries)

- **United States** — holding/contracting entity, Palo Alto registered address (likely a virtual/registered-agent address given the team is in Warsaw).
- **Poland** — actual operating team, Warsaw.
- **Philippines** — S6 §2 references "The Philippines operations and customer-support team", with restricted access rights and no authority to approve high-risk merchants, change payout destinations, override screening or release compliance holds.

> **Flag:** the **Philippines operations/support team was not disclosed** in Duke's answers (S3/S4) and surfaced only inside the AML policy. Not a problem in itself — outsourced/offshore support is normal — but it is an undisclosed data-processing and control location that the risk file needs (headcount, entity or contractor arrangement, data access scope, personal-data transfer basis).

### 3.4 Named personnel

| Name | Role | Source |
|---|---|---|
| Hoang Duc Vu ("Duke") | CEO, co-founder, 55% declared, sole board member Fungies Europe | S3 |
| Wojciech Harzowski | Co-founder, 40% declared | S3 |
| Agata Pisarek | **Compliance Officer** — document owner of all four policies | S6–S9 |

> **Flag (internal inconsistency):** S7 and S8 both state the policy owner is "Compliance Officer / **CEO until a Compliance Officer is appointed**", and S8 §5.3 refers to reporting "to the CEO and, **once appointed**, the Compliance Officer" — yet Agata Pisarek is named as Compliance Officer and document owner on the cover of the same documents. Either the role was filled while the templates were being drafted, or the CO function is not actually staffed. Needs a direct answer: is there a full-time, independent Compliance Officer in post, and since when?

---

## 4. Merchant of Record legal setup and licensing position

**As declared (S3):**

- Fungies **contracts as legal seller of record**.
- This is enforced by a **hard contractual requirement that every merchant's own terms & conditions explicitly name Fungies as Merchant of Record**.
- **No independent payment licence is held.**
- Fungies operates **via its PSP's infrastructure** — currently Stripe, with Checkout.com to be added as a second pay-in rail under the same model.
- Tax collected as MoR is **held separately, is not Fungies revenue**, and is remitted to the relevant tax authority.

**Against my original question (S2):** I asked whether the operating basis was (i) a financial licence, (ii) a legal exemption, (iii) a collection-agent agreement, or (iv) the PSP's infrastructure. The answer is **(iv) only** — with no licence, no cited exemption, and no collection-agent structure.

**What the policies themselves say:** S6 §1 is explicit and unusually candid —

> "This policy is an operational control document. It does not itself determine whether Fungies.io is an MSB, money transmitter, financial institution, or reporting person in any jurisdiction. Regulatory status, SAR obligations, OFAC reporting obligations, and licensing requirements **must be determined by qualified counsel for the actual funds flow and jurisdictions involved**."

> **Flag (highest priority — R1 in §12):** Fungies' own compliance framework states the licensing/regulated-status question is unresolved and requires counsel. No legal opinion or memo has been provided. Fungies collects end-customer funds, deducts its own fee, withholds tax, and settles net to sellers — a flow that in several of its stated markets (EEA, UK, US state-level money transmission) can constitute regulated payment or money-transmission activity absent a licence, exemption, or a properly structured agency arrangement. Under the proposed model, Checkout.com would be the acquirer whose infrastructure carries that flow. **A counsel opinion covering the actual funds flow and each stated jurisdiction is required before this can be approved.**

**Geographic MoR footprint claimed on the call (S1/S2):** UAE, EEA, UK, US, Korea.

> **Flag:** the MoR jurisdiction list from the call (**UAE, Korea**) does not appear anywhere in S3/S4's entity, seller-geography, or buyer-geography data, and there is no UAE or Korean entity disclosed. Either the call list was aspirational or there are undisclosed arrangements. Clarify.

---

## 5. Merchant portfolio and risk profile

### 5.1 Scale

| Metric | Value | Source |
|---|---|---|
| Active merchants (current) | **~100** | S4 |
| Active merchants (24-month projection) | **~1,000** (10x) | S4 |
| Channel | **100% e-commerce, card-not-present** | S3 |

### 5.2 Verticals and MCC

- **Declared verticals:** SaaS, digital goods, e-books, music/video/software downloads.
- **MCC:** **100% of the merchant base classified under MCC 5734 "Computer Software Stores"** (S4).
- **Explicitly prohibited on the platform (per Duke, S3):** gambling, crypto, NFTs, loot boxes. No exposure declared.

> **Flag (MCC):** a single MCC for 100% of a ~100-merchant, soon-to-be ~1,000-merchant portfolio is a classification and monitoring blind spot. E-books, music/video downloads and digital-content subscriptions are not naturally 5734; digital-goods MCCs (5815/5816/5817/5818) and 5968 for continuity/subscription billing exist precisely to make this population visible to the networks. Blanket 5734 also masks the 30% subscription/recurring segment, which carries the negative-option and "unrecognised recurring charge" dispute profile. Expect this to be a required remediation: a mapped MCC taxonomy per merchant type before launch.

> **Flag (prohibited categories — policy vs. representation):** Duke states crypto is "explicitly prohibited." **S7 §2.2 does not prohibit it** — it places "Adult/NSFW, financial services, gambling, crypto, IP-sensitive goods" in the **"High / restricted"** tier, permissible with "specialist written processor approval." Only illegal activity, undisclosed processing, false information, sanctions, fraud, transaction laundering and prohibited card-network categories sit in the "Prohibited" tier. Likewise **S7 §1.1** treats "adult/NSFW content **without specialist written approval**" as prohibited — i.e. adult content is restricted-but-possible, and **adult was never addressed in Duke's answers at all**. The written policy is therefore more permissive than the verbal representation. We need (a) the actual country-control and prohibited-business list, and (b) a contractual commitment on which categories are hard-excluded from Checkout.com-processed volume.

### 5.3 Geography

**Seller (merchant) geography — S3:**

| Region | Share |
|---|---|
| EEA | 40% |
| UK | 20% |
| US | 10% |
| Hong Kong | 10% |
| Indonesia / Singapore / India | 10% |
| Canada / Australia | 10% |

**Buyer (shopper) geography — S3/S4:**

| Region | Share | Currency |
|---|---|---|
| US | 60% | USD |
| EEA | 30% | EUR |
| India / Canada / Australia | 10% | INR / CAD / AUD |

> **Flag (cross-border):** 30% of sellers sit in APAC (Hong Kong, Indonesia, Singapore, India) while 60% of buyers are US and 30% EEA. Under the MoR model Fungies is the merchant of record, so the card-acceptance geography follows Fungies' entity rather than the seller's — but the **underlying seller-country risk** (APAC sellers, US/EEA cardholders) is real and needs to be visible in our own risk model. Hong Kong and Indonesia seller exposure in particular warrants EDD. Note S6 §4 requires exactly this check ("a geographic mismatch between merchant registration, website targeting, customer countries, payout country, IP/access data, or expected activity requires enhanced review") — we should ask for evidence it is being run.

---

## 6. Compliance framework

Fungies has provided **five** internal policies (S6–S10). All five are **Version 1.0**, authored by Agata Pisarek (Compliance Officer), classified "Internal — Compliance Controlled Document", effective **6–7 August 2026** — i.e. approximately one month before our call.

> **Flag (cross-cutting — R3 in §12):** every policy carries an **unexecuted approval block**: "Approved by: **[CEO / Board approval to be inserted]**", with `[Insert]` in the Compliance Officer, CEO and Board signature and date fields. S6 §7 states expressly: "**This policy becomes effective only after the approving authority signs or digitally approves it**"; S10 §6 repeats it. By their own terms, **none of the five policies is in force**. Combined with the 6–7 August 2026 effective dates, the reasonable read is that this framework was **written for this diligence exercise** and has little or no operating history. Request countersigned versions plus evidence of operation (case files, QC samples, training records).

### 6.1 AML, Sanctions & Geographic Controls Policy (S6)

| Element | Content |
|---|---|
| Owner | Agata Pisarek, Compliance Officer |
| Effective | 7 August 2026 |
| Review cycle | Annually + on material change of processor, product, ownership, country footprint or law |
| Scope | All directors, officers, employees, contractors, merchants, connected accounts, payout beneficiaries, support and commercial personnel |

**Control ownership and independence (§2):** CO owns policy, case-management standards, escalation register and periodic testing. **Commercial personnel may collect information but may not override a compliance decline, payout hold, suspension or exit decision.** CO reports material matters directly to the CEO and may escalate to external counsel, board, processor, acquirer or bank. Philippines support team is limited to document collection, customer communication and case administration.

**Screening (§3):** **Didit** for individual identity verification, **Sumsub** for business verification, covering sanctions, PEP, adverse media, corporate registry, ownership and document verification. Fungies retains the final acceptance and payout-eligibility decision. Pre-activation screening must be recorded across four subjects: merchant legal entity; individual/UBO/control person; payout beneficiary (legal-name match, bank-country compatibility, **prohibition on unapproved third-party payout accounts**); product and jurisdiction (payment-partner restrictions, prohibited-business rules, country restrictions, IP/adult-content risk, transaction-laundering indicators, cross-border exposure).

Any sanctions/PEP/adverse-media/identity/registry/ownership/domain/funds-flow alert must be dispositioned in a case record. A possible or confirmed sanctions match, material identity mismatch, suspicious ownership change, unapproved country exposure or material adverse information requires **immediate escalation with no activation or payout release until resolved**.

**Geographic controls (§4):** a maintained **country-control list** identifying prohibited, restricted and EDD jurisdictions, approved by the CO with documented rationale and effective date. *(The list itself has not been provided — see §11.)*

**Investigation and escalation (§5):** available actions include declining activation, pausing processing, delaying payout, requesting evidence, suspending the workspace, preserving records, notifying the payment partner. **Legal advice is required before any independent filing, blocking action, regulatory report or law-enforcement response.** Where Stripe, a bank, acquirer or processor is the reporting institution, Fungies provides evidence and cooperates — i.e. **Fungies positions itself as non-reporting and relies on the regulated counterparty**. Directly relevant to what we would be expected to absorb.

**Records, QC, training (§6):** role-based audited access; **monthly QC sample** of onboarding and alert dispositions; **annual role-appropriate training**; non-retaliation for compliance escalations.

### 6.2 KYB Procedure — Sumsub (S7)

**Standard:** acceptance only after establishing legal entity, ownership and control structure, operating website/app, product and customer flow, payout destination, and risk profile. Re-run before live access and on any material business change. **"A registry match alone is never sufficient to approve a merchant."**

**Prevents (§1.1):** undisclosed/misrepresented businesses, shell entities, false ownership, out-of-scope operation; **transaction laundering** (using one approved business to process for another company, website, product or seller); prohibited/restricted categories.

**Hard stop:** no business activated on the strength of a registration number, a revenue opportunity, or a completed provider check alone.

**Minimum evidence (§2.1):**

| Evidence | Requirement |
|---|---|
| Legal entity | Registry name, number, jurisdiction, address, formation date, legal status |
| Ownership & control | Directors, authorised representative, **each beneficial owner ≥25%** (lower where risk requires) |
| Operating presence | Verified website/app, domain control, products, price, delivery, policies, support contact, customer journey |
| Payout destination | Bank-account ownership evidence; explanation of any third-party beneficiary |
| Funds flow | Customer charge, Fungies fee, refund/dispute allocation, reserve, seller payout map |

**Risk tiers (§2.2)** — assigned by Fungies, not self-selected:

- **Standard** — transparent digital merchant, verified entity/owners, public storefront, low-risk product, clear refund/delivery terms.
- **Enhanced** — subscriptions, digital credits, AI tools, marketplaces, creator/seller payouts, cross-border sales, high-ticket goods, new entities.
- **High / restricted** — adult/NSFW, financial services, gambling, crypto, IP-sensitive goods, unclear fulfilment, country/ownership risk. Requires specialist written processor approval, or rejection.
- **Prohibited** — illegal activity, undisclosed merchant processing, false information, sanctions, fraud, transaction laundering, prohibited card-network category.

> Note: on Fungies' own taxonomy, **subscriptions and cross-border sales are "Enhanced"** — which means a large share of the Checkout.com-bound portfolio (30% subscriptions, heavy cross-border) should be in enhanced review by default. Worth testing how many of the ~100 merchants are actually tiered Enhanced or above.

**Pre-activation sequence (§3.1):** Sumsub business-verification case → registry reconciliation → director/UBO identification routed to KYC → questionnaire (business model, product category, target countries, delivery model, transaction profile, recurring-billing model, payment methods, expected volume, support process, complete funds flow) → corporate documents where registry data is unavailable/stale/contradictory → AML/sanctions/PEP/adverse-media review with documented false-positive reasoning → **comparison of Sumsub results against the actual public storefront, checkout URL, pricing, terms, refunds, social channels** → decision recorded in the Fungies Admin Panel with reason and reviewer.

**Enhanced review mandatory for:** complex corporate structure, non-local or opaque ownership chain, nominee arrangements, recently formed entity, seller marketplace, digital credits, subscriptions, AI-generation products, cross-border payouts, elevated disputes, regulated activity, high-risk country, or a business using a different domain/product than declared.

**Website research standard (§4.1):** reviewer independently inspects the declared domain/app and confirms legal entity or trading name, product/category, pricing and billing, delivery, refund/cancellation policy, support contact, policies and matching checkout. Search results, public complaints, IP-risk indicators, **hidden adult/NSFW content** and domain-history inconsistencies are treated as risk evidence.

**Outcomes (§5.1):** Accept (activate only the approved domain/product/country, set review date) / Accept with controls (**reserve, transaction cap, payout delay, or processor confirmation**) / Reject (ban, preserve case file) / Suspend–offboard (block payments/payouts, investigate, complete run-off).

**Ongoing monitoring (§5.2):** reopen KYB at least annually for enhanced/high-risk merchants, and immediately on any ownership, director, bank-account, legal-name, country, domain, product, billing, payout or risk-performance change. Mandatory triggers include elevated disputes/refunds, complaints, transaction-laundering indicators, adverse-media/sanctions alerts, new processor requirements, website changes, and **evidence that a merchant is processing for another business**.

### 6.3 KYC Procedure — Didit (S8)

**Standard:** "A Didit result is verification evidence, **not automatic approval**." No applicant may process, receive payout, or access live payment functionality before internal review and a recorded approval decision.

**Hard stop:** "No employee may waive KYC because of revenue potential, sales urgency, a referral, prior platform use, or an applicant's promise to provide documents later."

**Identity population (§2.1):** the workspace creator plus everyone who owns/controls **≥25%**, acts as director or authorised representative, **controls the payout account**, or otherwise exercises material control. Lower thresholds applied where risk indicators justify.

**Roles and approval authority (§2):**

| Role | May approve? |
|---|---|
| Applicant | No |
| Sales / Account team | **No** — collects context, escalates inconsistencies, may not approve, override or reopen a rejected case |
| Compliance analyst | Conditional — reviews and recommends |
| Compliance Officer / CEO delegate | **Yes** — approves elevated risk, rejects material risk, sets limits and review dates |
| Engineering / Operations | No — enforces status, blocks, holds, audit logs, access controls |

**Activation status model (§2.2):** Pending / Review required / Accepted (live access **only within approved domain, product, geography, limit and payout parameters**) / Rejected–suspended. **Hard stop:** status may not move to Accepted without a recorded KYC decision, an approved processing URL, and a completed business-risk review.

**Workflow (§3.1):** unique verification session tied to workspace, applicant name, email and country → **government-issued ID + selfie/liveness, completed personally** (third-party-supplied documents not accepted) → review of Didit decision, document authenticity, liveness/face-match, device/IP and duplicate-identity signals → sanctions/PEP/adverse-media screening of applicant and control persons → comparison of verified name, DOB, nationality/residence and control role against workspace, business application, bank record and KYB file → decision, reviewer, evidence references, approved purpose and next review date recorded.

**Step-up triggers (§3.2):** PEP or sanctions/adverse-media candidate; document–workspace mismatch; applicant linked to multiple workspaces; anomalous IP/device signals; high-risk country, product or payment flow; **payout-bank owner differs from the verified controller**; processor/network request. Enhanced evidence may include proof of address, business authorisation, ownership explanation, payout-bank ownership proof, source of funds, video verification, or a second ID. **Only the CO or authorised delegate may accept an exception.**

**Hard stop:** a failed, expired, tampered, duplicate or materially inconsistent KYC result stays blocked and cannot be substituted by a manual promise, a sales confirmation or a later payout request.

**Case note requirement (§4.1):** must state who was verified, which workspace and business were reviewed, which URL/app and product were approved, what evidence was considered, what risks were identified, what limits or follow-up apply, and who approved or rejected. **"A blank reason field is not acceptable."**

**QA (§5.3):** monthly sample testing of approved and rejected files; material control failures reported to the CEO and CO.

### 6.4 Refund, Dispute, Reserve & Settlement Policy (S9)

**Responsibility split (§2):** Fungies administers payment acceptance, billing communications, legally required refunds and chargeback administration in its customer-facing MoR role. **Sellers** remain responsible for accurate product descriptions, fulfilment, support cooperation, content/product compliance and timely dispute evidence. The **economic** allocation is governed by the seller/MoR agreement, which permits deduction or withholding of refunds, chargebacks, reversals, disputes, fees, penalties, taxes, reserve movements and FX amounts from seller settlement.

**Refund controls (§3):** every request logged with order reference, payment reference, reason, amount, currency, requester, decision and completion date. **Refunds to the original payment method** unless law or the processor permits otherwise. Ops may process routine refunds within authority limits; CO review required for suspected fraud, sanctions risk, a prohibited merchant, a legal complaint, an unusually high amount, or a request for a different destination. Merchants may not direct customer refunds to a third-party account or external wallet without provider and counsel approval.

**Disputes (§4):** on receipt, Fungies preserves customer, order, checkout, product, fulfilment, communications, refund and merchant data; requests seller evidence promptly; responds within processor/network time limits. CO must review material dispute trends, repeat reason codes, credible fraud/deception allegations, IP claims, prohibited-content claims, or dispute volume exceeding the approved risk profile — and may suspend the merchant, pause settlement, revise reserves, limit activity or require remediation.

**Settlement and reserves (§5):**

- Seller payout accounts must be **in the seller's legal name and verified before use**; any addition or change requires an authorised request, ownership verification and a **security hold** before activation. **Unapproved third-party payout accounts are prohibited.**
- Standard cycle: **automatic business-day payout after the prior seven days have settled and become eligible (T+7 example)**, subject to payment-method settlement timing, bank cut-offs, reserve requirements, lawful/contractual withholding and live processor restrictions.
- **Rolling reserve** may be established where contractually authorised and necessary for present or anticipated refunds, chargebacks, reversals, disputes, fees, penalties, taxes, fraud losses or related liabilities. **The sample MoR agreement permits a 10% rolling reserve** subject to a stated cap and release framework. Actual reserves documented by merchant, reason, calculation, owner, date and review schedule.

**Negative balances (§6):** recorded, notified to the seller, assessed by Finance and Compliance; recovery via future settlement, reserve amounts or contractual set-off. **No payout release may occur where it would create or worsen a known unpaid refund, chargeback, reserve shortfall, sanctions hold, prohibited-business investigation, or legal/processor restriction.**

**Reporting (§7):** reconciled settlement records showing gross settled amount, taxes, processing fees, Fungies fees, refunds, disputes, chargebacks, reserve movements, FX, seller net, payout reference and payout currency. Monthly CO exception reporting; quarterly QC sample.

> **Assessment:** this is the strongest of the four documents and it is directly useful to us — Fungies already has the contractual machinery (deduction, set-off, rolling reserve, payout hold, security hold on payout changes) that we would want it to exercise downstream of a Checkout.com reserve. The gap is not the policy design; it is that Fungies' **own balance sheet cannot absorb a loss that outruns seller recovery** (§7, §10).

### 6.5 Transaction Monitoring & Merchant Risk Policy (S10)

*Received after the initial response; this is the post-onboarding control layer and, from our perspective, the most consequential document in the pack.*

| Element | Content |
|---|---|
| Owner | Agata Pisarek, Compliance Officer |
| Effective | 7 August 2026 |
| Review cycle | **Quarterly** for thresholds, **annually** for the policy |
| Positioning | "It **supplements** processor and acquirer monitoring; **it does not replace it**." |

**Objective (§1):** detect activity that differs from the approved merchant profile *before* it causes customer harm, chargebacks, card-network exposure, processor violations or transaction laundering.

**System of record (§2):** the Fungies Admin Panel holds workspace activation, status, reviewer decision, reason code, approved website/domain, processor status and enforcement action, with role-based access and an audit trail of material status changes. Every active merchant must have an approved file containing legal entity, contact and control persons, website/domain, product description, intended use, expected transaction profile, customer terms, refund policy, payout destination and risk rating. **Material changes require re-review before continued processing.**

**Six monitoring areas and escalation triggers (§2):**

| Area | Control | Escalation trigger |
|---|---|---|
| Website & domain | Approved URL, checkout domain, descriptor, products and marketing remain consistent with onboarding | New/changed domain, unapproved subdomain, misleading descriptor, undisclosed seller, prohibited product |
| Merchant activity | Actual volume, countries, payment patterns, refund/dispute behaviour vs. approved expected profile | Material unexplained deviation, **rapid volume growth**, new high-risk country, unusual payment method |
| Disputes & refunds | Spikes, unusual reasons, repeat buyer complaints, refund practices | Threshold breach per processor/acquirer rules or internal risk review |
| Payout risk | New/amended payout destination, negative balance, reserve depletion, failed payout, rapid withdrawal pattern | Third-party account, legal-name mismatch, unusual payout country, **request to bypass standard hold** |
| Linked-account / laundering | Common owners, devices, domains, support contacts, fulfilment sources, traffic sources, commercial relationships | **Undisclosed processing for another business**, owner mismatch, activity inconsistent with declared URL |
| Content & restricted business | Reassess digital goods, AI, subscriptions, IP, **adult content**, regulated products, jurisdictional restrictions | Prohibited product, credible complaint, rights-holder allegation, processor request |

**Investigation and enforcement (§4):** reviewer documents alert source, factual observations, evidence requested, merchant explanation, decision maker and outcome. CO may require EDD, revise limits, suspend activation, pause processing, delay or withhold payout, establish a reserve, require remediation, or exit the merchant. **"Commercial targets must not influence a compliance decision."**

**Management information (§5):** monthly MI covering active merchant count, new approvals, declines, review queue, alerts opened/closed, average response time, suspensions, payout holds, material disputes/refunds, complaints, high-risk-country exposure and remediation status. Monthly QC sample tests evidence standard, recorded reasons, status controls and escalation.

#### 6.5.1 Two findings from this document that change the risk picture

**(a) There is no calibrated monitoring in operation — everything is manual (R20).**

§3 requires a **separate Monitoring Threshold Register**, CO-approved, specifying thresholds, owners, effective dates, data source, alert severity, response timeline and closure requirements, "**calibrated to the actual processor, merchant category, portfolio, and card-network programme rather than copied from a generic policy**." Then:

> "**Until the register is approved and operational**, any of the following must be treated as a **manual alert**: a material dispute/refund increase; a transaction or volume level that materially exceeds the approved profile; a change in business/domain/payout beneficiary; a complaint alleging non-delivery, deception, IP infringement, or prohibited content; a sanctions or adverse-media hit; a processor/card-network inquiry; or a suspected transaction-laundering indicator."

And §6 goes further, in what is effectively a self-imposed warning to counterparties like us:

> "The Monitoring Threshold Register, named data sources, and named dashboard reports **must be attached before external reliance is placed on live automated monitoring claims**."

**The register has not been provided.** On the plain reading of Fungies' own document, post-onboarding monitoring today is **manual, uncalibrated, and not something we may rely on**. This is a credit to their drafting honesty and a significant finding for our file: it means monitoring of a portfolio heading from ~100 to ~1,000 merchants currently rests on human review with no defined thresholds — and the policy itself tells us not to treat any automated-monitoring claim as substantiated. **Request the register (or confirmation it does not yet exist) as a launch condition.**

**(b) Anti-PSP-arbitrage control — directly relevant to us as the second rail (R21).**

§4: "A merchant may not be reactivated **or moved to another payment provider for the same rejected activity** without written approval from the relevant provider and the Compliance Officer."

This is the right control, and it is precisely the risk created by the proposed architecture. Once Checkout.com sits alongside Stripe as a second pay-in rail, the structural temptation is for merchants that Stripe has declined, limited or offboarded to be routed to us — and for that routing to look, operationally, like ordinary PSP choice. Fungies has anticipated this in policy. We should **mirror it contractually**: an express warranty and ongoing notification obligation that no merchant declined, suspended, offboarded or limited by Stripe (or any other provider) for risk or compliance reasons is routed to Checkout.com volume without our prior written approval, plus an audit right to test it.

### 6.6 Compliance framework — summary scorecard

| Dimension | Assessment |
|---|---|
| Policy design and coverage | **Strong** — well-drafted, specific, right hard stops, correct treatment of transaction laundering, sales/compliance separation, payout-beneficiary control, anti-PSP-arbitrage clause |
| Vendor stack | **Adequate** — Didit (KYC/liveness/AML), Sumsub (KYB/registry/UBO/screening); both credible, both used as evidence rather than decision |
| Formal status | **Weak** — all five v1.0, effective 6–7 Aug 2026, **approval blocks unsigned**; by their own terms not in force |
| Operating history | **Unknown / likely minimal** — ~1 month old at best; no case files, QC samples or training records provided |
| Independence | **Unclear** — CO named on covers but two policies still say "CEO until a Compliance Officer is appointed" |
| Regulatory position | **Unresolved** — policy explicitly defers MSB/money-transmitter/licensing determination to counsel; no opinion provided |
| Transaction monitoring | **Weak in practice** — policy design is sound, but the **Monitoring Threshold Register does not exist / was not provided**, so monitoring is manual and uncalibrated, and S10 §6 expressly disclaims external reliance on automated-monitoring claims (§6.5.1a) |
| Scalability to ~1,000 merchants | **Unevidenced** — no compliance headcount, no SLAs, no MI packs, no QC output provided |

---

## 7. Financial position and credit assessment

### 7.1 Profit & Loss (S5, USD, FY2025 vs FY2024 — **unaudited management accounts**)

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

Revenue represents **net platform fees**, not gross MoR volume — Duke flagged this himself: "we only keep the 5% + $0.50 fee, not the full transaction amount." Costs are categorised from Mercury Bank and Brex account activity. FY2024 figures are described as sourced from "audited management accounts"; FY2025 is explicitly unaudited.

### 7.2 Balance Sheet (S5, USD)

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

### 7.3 Cash Flow (S5, USD)

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

### 7.4 Credit assessment

| Factor | Reading |
|---|---|
| **Liquidity** | **USD 225** in cash at 31 Dec 2025 against a FY2025 net burn of ~USD 346k. Effectively **zero runway** at year-end, absent post-YE funding or the 2026 revenue ramp. |
| **Total assets** | **USD 113,982**, of which **99.8% is a Stripe receivable** — a claim on the incumbent processor, not free cash. |
| **Liabilities** | Nil reported. No debt. Nil accrued expenses and nil accounts payable for a company with USD 343k of annual opex is itself implausible and suggests incomplete accrual accounting. |
| **Funding** | USD 250k carried as pre-conversion SAFEs; USD 250k raised in FY2025, USD 270k in FY2024. Seed-stage, no priced round, no shares issued. |
| **Profitability** | Loss-making both years, with losses widening (−55.9%). Opex is 2.9x revenue. |
| **Audit status** | **No independently audited financials exist** (confirmed by Duke). FY2025 is management-prepared. |
| **Capacity vs. exposure** | This is the core issue. Total assets of **USD ~114k** and cash of **USD 225** stand against: current processing of **USD 4.8m/month**, a proposed Checkout.com run-rate of **EUR 1m/month**, and Fungies' own confirmation (S4) that **all chargeback and dispute liability sits with Fungies** to the processor, networks and end customer. Fungies can pass the economic cost to sellers contractually, but it cannot absorb a loss that outruns seller recovery — a merchant failure, a mass-fraud event, a portfolio-level dispute spike, or an insolvent seller with a negative balance. |

> **Flag (R2 in §12):** on the FY2025 balance sheet, Fungies has **no meaningful loss-absorbing capacity**. Any approval should be conditioned on some combination of: an up-to-date 2026 balance sheet and bank statements (the 2026 growth is the whole argument and it is entirely undocumented), a **security package** (rolling reserve, cap, and/or a parent or founder guarantee), volume caps stepped against the ramp, and evidence of post-YE2025 funding. The 2026 trading position needs to be substantiated before the FY2025 accounts are treated as stale rather than as the operative picture.

### 7.5 Internal inconsistencies in the financial statements

These matter because there are no audited accounts to fall back on — the management accounts are the only evidence, and they do not tie.

1. **Accumulated deficit does not roll forward.** Opening deficit (146,698.86) + FY2025 loss (232,657.00) = **(379,355.86)**. Reported closing deficit is **(136,018.00)** — a ~USD 243k unexplained difference. The reported deficit is also *smaller* than the prior year's despite a full-year loss.
2. **Cash flow opening balance does not match the prior balance sheet.** FY2025 "cash at beginning of period" is **96,639.00**; FY2024 "cash at end of period" and the 31 Dec 2024 balance sheet both show **124,254.78** — a **USD 27,616 break**.
3. **FY2024 cash flow does not foot.** Opening 0.00 + net change 120,729.28 = 120,729.28, against a reported closing balance of **124,254.78** — a **USD 3,525 break**.
4. **SAFE note reconciliation.** The named instruments (Jaag 250k + Diep 100k + Woźniakowski 25k + UNIT 20k = **395k**, plus a separately referenced **125k** "seed wire" in the cash-flow note) exceed the **250k** carried on the balance sheet. "Net of conversions" is asserted but the balance sheet simultaneously states **no shares have been issued** — so there is nothing for the SAFEs to have converted into.
5. **Equity composition vs. share issuance.** Equity of 113,982 = 250,000 SAFEs − 136,018 deficit, so the total foots — but it foots to a deficit figure that is itself unsupported (item 1), and rests on SAFE instruments recorded within equity while described as pre-conversion.
6. **Nil liabilities.** No accounts payable, accrued expenses or deferred revenue in either year, despite USD 343k opex and a subscription-billing business (which would normally generate deferred revenue).

> These are the kind of breaks a review would expect an accountant to resolve in an afternoon — but they need resolving. Ask for a restated, internally consistent set, ideally reviewed by an external accountant, plus 2026 YTD.

---

## 8. Commercial: volumes, pricing, settlement

### 8.1 Current platform scale (all rails, Stripe today)

| Metric | Value | As of |
|---|---|---|
| Total processing volume | **USD 4.8m/month** | End July 2026 |
| Prior data point | USD 2.4m/month | Mid-June 2026 |
| Growth | **2x in ~6 weeks** | — |
| Payout volume to sellers | **USD 4.4m/month** | — |
| Payout count | **~2,694 payouts/month** | — |
| ATV | **USD 60–63** | — |
| Chargeback rate | **<0.05% historically** (asserted, unevidenced) | — |
| Settlement currencies | **USD and EUR — 99% of volume** | — |

### 8.2 Checkout.com-bound volume forecast (S4)

Launch December 2026, full run-rate by month 6:

| Month | Volume (EUR) | % of run-rate |
|---|---|---|
| Dec 2026 | 150,000 | 15% |
| Jan 2027 | 300,000 | 30% |
| Feb 2027 | 450,000 | 45% |
| Mar 2027 | 600,000 | 60% |
| Apr 2027 | 800,000 | 80% |
| May 2027 onward | 1,000,000/month | 100% |
| **Year 1 total (Dec'26–Nov'27)** | **~9,300,000** | — |
| **Run-rate from month 6** | **12,000,000/year** | — |

*Ramp arithmetic checks out: 150 + 300 + 450 + 600 + 800 + (7 × 1,000) = EUR 9,300k.*

**By shopper country / currency:** US 60% (USD) · EEA 30% (EUR) · India/Canada/Australia 10% (INR/CAD/AUD).

**By payment method (Fungies estimate, open to refinement):**

| Method | Share |
|---|---|
| Cards (Visa / Mastercard / Amex) | ~70% |
| Digital wallets (Apple Pay / Google Pay) | ~20% |
| Local APMs (iDEAL, SEPA, etc. — EEA) | ~10% |

**One-off vs. subscription:** **70% / 30%** (consistent across S1, S3, S4).

**Derived (at USD 60–63 ATV):** ~150k–160k transactions in Year 1; ~16k/month at full run-rate.

### 8.3 Settlement

| Parameter | Detail |
|---|---|
| Settlement currencies | USD, EUR (99% of volume) |
| **USD** | US bank account, **Fungies Inc.** (Delaware) |
| **EUR / PLN** | Poland bank account, **Fungies Europe P.S.A.** |
| FX requirement | Not definitively answered — S2 asked whether processing-currency settlement or FX conversion is required (EUR, PLN). S3/S4 confirm the currencies and accounts but not the requirement. **Open — see §11.** |
| INR / CAD / AUD (10% of volume) | No settlement arrangement stated for these currencies. **Open.** |

> See §3.2 flag: EUR settlement to a non-contracting entity's account must be structured properly.

### 8.4 Pricing

**Fungies → its merchants:** blended **5% + USD 0.50 per transaction**, all-inclusive — bundling payouts, FX, PSP processing and tax compliance.

**Fungies' current Stripe cost:** **not provided.** S2 asked for effective Stripe pricing broken down by processing, Connect, payout, fixed and FX fees; S3 answered with Fungies' *sell-side* price instead. **We do not know their cost base, and therefore not their margin or their price sensitivity.** This is the single most important missing commercial input for the proposal — see §11.

**Derived take-rate context:** at USD 60 ATV, 5% + $0.50 = USD 3.50 per transaction ≈ **5.83% effective**. On USD 4.8m/month that implies gross platform fee revenue of roughly **USD 280k/month (~USD 3.4m annualised)** — which sits against FY2025 reported revenue of USD 119,876. The gap is explained only by the 2026 ramp; it needs to be evidenced (see §10.1).

**Commercial construct:** tiered pricing against a **monthly minimum commitment** (discussed on call, to be finalised).

---

## 9. Technical, integration and money flow

### 9.1 Current architecture — Stripe Connect

| Element | Detail |
|---|---|
| Connected account type | **Stripe Express** |
| Charge type | **Direct charges** — charge created directly on the seller's Express connected sub-account |
| Fungies monetisation | **Stripe application fees** (platform fee) |
| Tax as MoR | Held separately, **not Fungies revenue**, remitted to the relevant tax authority |
| Seller net settlement | Gross sale − Fungies fee − tax collected, wired to the seller's Stripe Express sub-account |
| Payout rails | **99% SEPA / Wire / ACH**; remainder **push-to-card (Visa Direct, Mastercard Send)** |
| Payout cycle | Automatic business-day cycle after the prior 7 days settle (**T+7** example, per S9) |

### 9.2 Liability split (S4 — explicit clarification)

> "Fungies is responsible for **all** chargebacks, disputes, and related liability as Merchant of Record — this sits with us directly, not the underlying merchant, from a network/processor-facing perspective. Internally, our merchant agreement allows us to recover the economic cost of a chargeback or dispute from the responsible merchant's settlement (via a per-transaction chargeback fee and net-settlement deduction), but the liability itself — to Checkout.com, to the card networks, to the end customer — is **ours alone**."

This is the correct and expected MoR answer, and it is clean from a contracting standpoint: **our counterparty is Fungies, full stop.** It also means our credit exposure is to Fungies' balance sheet (§7.4), with seller recovery as a second-order mitigant only.

> **Note (architecture divergence):** direct charges on Express connected accounts is a *Stripe-specific* construct where the charge lands on the seller's sub-account, yet Fungies asserts full MoR liability. Under a Checkout.com integration there is no equivalent connected-account layer — **Fungies would be the merchant on our platform**, processing under its own MID(s), with the payout leg handled by the separate payout provider. This is architecturally cleaner and matches the stated liability position, but it is a **different model from what they run today**, not a port of it. This should be the opening item in the Solutions Engineering session.

### 9.3 Platform layer

Fungies provides:
- **Hosted checkout**
- **Subscription / billing management**
- **API and webhook layer**

Merchant integration options: **hosted checkout**, **embedded/overlay checkout**, or **direct API**.

### 9.4 Money flow

**S11 — "Fungies.io — Merchant of Record Fund Flow · Stripe Connect — Direct Charge Model"** has now been received. Duke has offered to adapt it once the payout provider on our side is confirmed.

**Current-state flow as diagrammed, with the worked example Fungies uses:**

```
End customer (card / wallet / APM)
        │
        │  $12.00 customer charge
        │  = $10.00 net sale + $2.00 VAT / GST / Sales Tax
        ▼
Charge created DIRECTLY on Seller's Stripe Express Sub-Account (Direct Charge)
        │
        ▼
$0.50 + 5% Fungies platform fee  (deducted as Stripe Application Fee)
        │
        ├──────────────────────────────┬─────────────────────────────────┐
        ▼                              ▼                                 │
Net Seller Balance            $2.00 Tax Collected & Held                 │
(gross − Fungies fee − tax)   ("Not Fungies revenue")                    │
        │                              │                                 │
        ▼                              ▼                                 │
Seller's Stripe Express        Tax Remittance to Tax Authority           │
Sub-Account Balance            (End Customer's country / jurisdiction)   │
        │                                                                │
        ▼                                                                │
Payout to Seller's Bank                                    Fungies fee ──┘
(SEPA / Wire / ACH — 99%;                                  → Fungies Inc.
 remainder push-to-card)                                     (Mercury / Brex)
```

**Three observations from the diagram:**

**(a) Tax treatment is correct in principle.** Tax is added *on top* of the seller's $10 list price rather than carved out of it, is explicitly labelled "Not Fungies revenue", is held separately, and is remitted to the **end customer's** jurisdiction. That is the right MoR construct and it matches what Duke said in S3.

**(b) The diagram's own economics contradict the reported payout ratio — decisively.** On the worked example, the seller receives roughly **$8.90–$9.00 of a $12.00 gross charge (74–75%)**, depending on whether the 5% is struck on gross or on net sale. Fungies reports payouts of **USD 4.4m on USD 4.8m of volume — 91.7%**. Those two numbers cannot both describe the same business: at the diagram's economics, payouts on USD 4.8m gross would be roughly **USD 3.6m**, not USD 4.4m. See §10.2 — the diagram converts that item from a rounding query into a **material reconciliation failure requiring an explanation**.

**(c) The fee base is ambiguous, and it matters commercially.** The diagram does not state whether the 5% is struck on the **gross charge including tax** ($12.00 → $0.60 + $0.50 = $1.10) or on the **net sale** ($10.00 → $0.50 + $0.50 = $1.00). Note also that the example ticket ($10–12) sits far below the stated ATV of USD 60–63, and the fixed $0.50 makes the effective rate highly ticket-sensitive: ~**10–11% at a $10 ticket** versus ~**5.83% at a $60 ticket**. Confirm the fee base and the true ATV distribution before we benchmark our pricing against theirs.

**Target-state flow (Checkout.com + separate payout provider)** — to be designed in the technical session. Key open design points:

1. Fungies as merchant on Checkout.com under its own MID(s) — MID structure, and whether split by seller geography, currency or vertical.
2. Where the fee and tax split occurs (no application-fee equivalent — likely in the Fungies ledger post-settlement).
3. Handoff mechanics to the payout provider, and reconciliation between our settlement file and their payout file.
4. Reserve mechanics — Checkout.com-held reserve vs. Fungies' own 10% rolling reserve on sellers, and how the two interact.
5. Negative-balance and run-off handling if a seller fails mid-cycle.
6. Dispute flow: our dispute notification → Fungies case management → seller evidence, within network time limits.
7. Multi-currency: USD/EUR settlement plus the 10% INR/CAD/AUD tail.

### 9.5 Stripe scope and migration — open

S2 asked which Stripe products are in use (Billing, PaymentIntents, etc.) and whether the ~30% subscription volume is **new subscriptions only** or includes **migration of stored payment credentials**. Duke has deferred to engineering (S3).

> **Why this matters:** if stored credentials are to be migrated, a Stripe→Checkout.com **network token / PAN migration** is required, which involves both processors, network approvals and lead time. It is on the critical path for a December 2026 launch and cannot be left until scoping. This should be resolved in the technical session, not after.

---

## 10. Data reconciliation issues

Beyond the financial-statement breaks in §7.5, four operational figures do not reconcile. None is necessarily a problem; all four need an answer.

### 10.1 FY2025 revenue vs. current volume

FY2025 revenue of **USD 119,876** implies, at a 5% + $0.50 take-rate (~5.83% at USD 60 ATV), an average FY2025 processing volume of roughly **USD 170–200k/month**. Current stated volume is **USD 4.8m/month** — implying **~24x growth in roughly 19 months**, most of it in 2026. Achievable for an early-stage platform with a good quarter, but the entire commercial and credit case now rests on 2026 performance for which **no documentation has been provided**. → Request 2026 YTD management accounts, monthly volume by month, and Stripe/bank statements.

### 10.2 Payout volume vs. tax withholding — **material, now confirmed by their own diagram**

Volume processed **USD 4.8m/month** vs. payouts to sellers **USD 4.4m/month** = sellers receive **91.7% of gross**. But per §9.1 and S11, seller net = gross − Fungies fee − **tax collected as MoR**. The fee alone (~5.83% at a USD 60 ATV) accounts for essentially the whole 8.3% gap, leaving **nothing for tax**.

The fund flow diagram (S11) settles this. Fungies' own worked example is a **$12.00 charge on a $10.00 net sale with $2.00 of tax** — tax at **16.7% of gross** — from which the seller nets **$8.90–$9.00, i.e. 74–75% of gross**. Applied to USD 4.8m/month, that implies payouts of roughly **USD 3.6m**, against the **USD 4.4m** reported. The discrepancy is on the order of **USD 800k/month**.

There are only a few possible explanations, and we need to know which:

1. The USD 4.8m "volume" figure is **net of tax** (i.e. gross charges are materially higher);
2. The USD 4.4m payout figure **includes tax remittances** and/or non-seller transfers;
3. The blended effective tax rate across the portfolio is far below the 16.7% in the example (plausible in part — much US digital-goods sales tax is lower or not due, though the 30% EEA buyer base attracts VAT at 17–27%); or
4. **Tax is not being collected and remitted at the rates the MoR representation implies.**

Explanation 4 would be a significant issue: it would undercut the MoR tax representation on which the whole model rests, and create an exposure that ultimately sits in front of the acquirer. **This should be a direct, named question, and it is worth resolving before the risk file closes.** Request tax registration numbers and remittance evidence for the principal jurisdictions (US states, EU OSS/IOSS, UK VAT), plus a reconciliation of gross charges → tax → fees → payouts for one recent month.

### 10.3 Payout count vs. merchant count

**~2,694 payouts/month** across **~100 active merchants** = **~27 payouts per merchant per month**, i.e. roughly daily. That is inconsistent with the stated **T+7 automatic weekly-eligibility cycle** (which would produce ~400–430 payouts/month for 100 merchants). → Either the active-merchant count is materially higher than 100 (e.g. counting individual creators/sellers beneath merchant accounts), or payouts are far more granular than described. Affects how we size the population and the KYB burden.

### 10.4 ATV

**USD 60–63** (S3/S4) vs. **~EUR 65** noted on the call (S2). At current rates these are similar figures in different currencies; likely just USD/EUR loose usage. Low materiality — confirm the currency for the pricing model.

### 10.5 MoR jurisdictions

Call (S1/S2): **UAE, EEA, UK, US, Korea**. Written answers (S3/S4): no UAE or Korea entity, and neither appears in seller or buyer geography. → Clarify whether the UAE/Korea claim reflects tax-registration footprint, planned expansion, or something undisclosed.

---

## 11. Outstanding information requests

### 11.1 Received in full

All Fungies attachments listed in S3 have now been received: the five compliance policies (S6–S10), the FY2025 financial statements (S5), and the MoR fund flow diagram (S11). Nothing from the original attachment list is outstanding.

### 11.2 Explicitly deferred by Fungies

| Item | Status per Duke |
|---|---|
| **3–6 month Stripe processing export** — volume, counts, refunds, disputes, fraud, acceptance/auth rates with definitions | "Still being pulled together — will follow up separately" |
| **Stripe scope & migration** — exact products in use; whether the 30% subscription volume is new-only or includes stored-credential migration | "Will confirm with our engineering team and follow up" |

### 11.3 Asked but not answered

| # | Item | Why it matters |
|---|---|---|
| 1 | **Effective Stripe pricing** — processing, Connect, payout, fixed, FX, broken out | Requested in S2; S3 gave the sell-side price instead. Without their cost base we cannot price competitively or judge sensitivity. **Top commercial priority.** |
| 2 | **Legal opinion on the MoR construct** | Their own AML policy defers this to counsel. **Top risk priority.** |
| 3 | **Country-control list** (prohibited / restricted / EDD) | Referenced in S6 §4; never provided |
| 3a | **Monitoring Threshold Register** + named data sources and dashboard reports | Required by S10 §3; **not provided**. Without it, monitoring is manual by their own terms and S10 §6 bars external reliance on automated-monitoring claims. **Launch condition.** |
| 3b | **Tax registrations and remittance evidence** (US states, EU OSS/IOSS, UK VAT) + gross→tax→fees→payouts reconciliation for one recent month | Resolves the USD ~800k/month payout-vs-tax break in §10.2 |
| 3c | **Confirmation of the 5% fee base** (gross incl. tax vs. net sale) and the ATV distribution | Fee base is ambiguous in S11; effective rate is highly ticket-sensitive (§9.4c) |
| 3d | **Warranty + notification obligation on merchants declined/offboarded by Stripe** | Mirrors their own S10 §4 anti-arbitrage clause; the core structural risk of a second-rail setup (R21) |
| 3e | **Compliance MI packs and monthly QC samples** as specified in S10 §5 | Evidence the framework operates at all |
| 4 | **Prohibited-business list** | Needed to reconcile the policy-vs-representation gap on adult and crypto (§5.2) |
| 5 | **FX requirement** — processing-currency settlement vs. conversion | Asked in S2; currencies confirmed but requirement not stated |
| 6 | **INR / CAD / AUD settlement treatment** (10% of volume) | No arrangement stated |
| 7 | **Definitive UBO position** given zero shares issued | Onboarding blocker |
| 8 | **Corporate documents** — Delaware certificate of incorporation and good standing; KRS extract for the Polish entity; SAFE agreements; cap table | Standard KYB |
| 9 | **Sample MoR / seller agreement** and **customer terms** | S9 repeatedly relies on "the standard agreement" and "the sample MoR agreement" (incl. the 10% rolling reserve); we have not seen either. Also needed to verify the "merchant T&Cs must name Fungies as MoR" control. |
| 10 | **2026 YTD financials + bank/Stripe statements**; restated internally consistent FY2025 (§7.5); evidence of post-YE2025 funding | The whole credit case is 2026 performance |
| 11 | **Countersigned policies** + evidence of operation (case files, monthly QC samples, training records) | Policies are unsigned and one month old |
| 12 | **Compliance Officer status** — is the role independently staffed, and since when? | §3.4 inconsistency |
| 13 | **Philippines operations** — entity/contractor basis, headcount, access scope, data-transfer basis | Undisclosed footprint (§3.3) |
| 14 | **PCI DSS status** — SAQ/AOC, level, scope; whether card data touches Fungies systems | Not raised yet; needed for integration design |
| 15 | **MCC taxonomy** per merchant type | Blanket 5734 is not sustainable (§5.2) |
| 16 | **Merchant concentration** — top 5 / top 10 merchants as % of volume | Absent from all sources; material to loss modelling given the balance sheet |
| 17 | **Refund rate** (distinct from chargeback rate) | Never given; digital goods/subscriptions typically run high |
| 18 | **Insurance** — E&O / cyber / crime cover | Standard for a thin-balance-sheet counterparty |
| 19 | **NDA execution status** (sent via DocuSign) | Confirm before further exchange |

---

## 12. Risk register

| ID | Risk | Severity | Detail | Proposed mitigation / condition |
|---|---|---|---|---|
| **R1** | **No payment licence and no legal opinion on the MoR construct** | **Critical** | Fungies holds no licence, cites no exemption, and operates "via our PSP's infrastructure." Its own AML policy states MSB / money-transmitter / licensing status "must be determined by qualified counsel for the actual funds flow and jurisdictions involved" — and no such determination exists. Fungies collects customer funds, deducts its fee, withholds tax and settles net to third-party sellers across EEA, UK and US. | **Blocking.** External counsel opinion covering the actual funds flow per jurisdiction, before contracting. Our own Legal/Compliance to review. Consider limiting Phase 1 to jurisdictions covered by the opinion. |
| **R2** | **No loss-absorbing capacity** | **Critical** | USD 225 cash, USD 113,982 total assets (99.8% a Stripe receivable), loss-making and widening, no audited accounts — against USD 4.8m/month current volume, EUR 1m/month proposed, and **full MoR chargeback liability confirmed as Fungies' alone**. | Security package: rolling reserve sized to the ramp + a cap, volume caps stepped by month, 2026 financials and bank statements, evidence of post-YE funding. Consider a founder or parent guarantee, or a deposit. Re-test at each ramp step. |
| **R3** | **Compliance framework unapproved and effectively untested** | **High** | **Five** policies, all v1.0, effective 6–7 Aug 2026 (one month pre-call), all with **blank CEO/Board approval blocks**; S6 §7 and S10 §6 both state they take effect only on approval. No case files, QC samples or training records. CO independence ambiguous (§3.4). | Countersigned policies; evidence of operation (dated case files, monthly QC samples, training completion); confirmation the CO role is independently staffed. |
| **R4** | **Settlement to a non-contracting entity** | **High** | Contracting entity Fungies Inc. (US); EUR/PLN settlement to Fungies Europe P.S.A. (Poland). Third-party settlement. | Add Fungies Europe P.S.A. as a contracting/approved settlement entity with its own KYB, **or** settle EUR to a Fungies Inc. account. Resolve before contracting. |
| **R5** | **Policy is more permissive than the verbal representation** | **High** | Duke: crypto "explicitly prohibited," no gambling/NFT/loot-box exposure, adult not mentioned. S7 §2.2 places adult/NSFW, financial services, gambling, crypto and IP-sensitive goods in **"High/restricted" — permitted with written processor approval**, not prohibited. | Obtain the country-control and prohibited-business lists. Contractual hard exclusion of specified categories from Checkout.com-processed volume, with a notification obligation and audit right. |
| **R6** | **Financial statements do not internally reconcile** | **High** | Accumulated deficit fails to roll forward (~USD 243k break); cash-flow opening balance breaks against the prior balance sheet (USD 27.6k); FY2024 cash flow does not foot (USD 3.5k); SAFE reconciliation unexplained; nil liabilities implausible against USD 343k opex. No audited set exists to fall back on. (§7.5) | Restated, internally consistent statements, ideally externally reviewed, plus 2026 YTD. |
| **R7** | **2026 growth entirely undocumented** | **High** | The whole commercial and credit case rests on USD 200k/month (FY2025 implied) → USD 4.8m/month (July 2026), ~24x. Only source is an email figure. | 2026 monthly volume, Stripe dashboard exports, bank statements. Independent verification before final sizing. |
| **R8** | **Blanket MCC 5734 across the whole portfolio** | **Medium-High** | 100% of ~100 merchants (→ ~1,000) under one software MCC, obscuring digital content, e-books, media downloads, and the 30% subscription/continuity segment. | Mapped MCC taxonomy per merchant type before launch; correct coding for recurring/continuity billing. |
| **R9** | **Subscription / recurring-billing dispute profile** | **Medium-High** | 30% subscriptions; S7 flags "deceptive subscriptions" as a category it must prevent; policies list subscriptions as **Enhanced** risk. Claimed CB rate <0.05% is unevidenced and no refund rate has been given. | Obtain the 3–6 month dispute/refund export with definitions. Enforce SCA/3DS and recurring-transaction flagging; monitor at merchant level from launch. |
| **R10** | **Ten-fold merchant growth on a one-month-old framework** | **Medium-High** | ~100 → ~1,000 merchants in 24 months, onboarded by a compliance function whose policies are unsigned and whose staffing is unclear. Onboarding quality is what stands between us and the portfolio. | Compliance headcount and scaling plan; agreed onboarding SLAs and quality metrics; our audit right; periodic file sampling; portfolio-level and per-merchant volume caps. |
| **R11** | **Ownership / UBO not formally established** | **Medium** | Declared 55/40 split, but **zero shares issued**; remainder in pre-conversion SAFEs; SAFE amounts do not reconcile. | Definitive UBO documentation; cap table; SAFE agreements; Delaware corporate documents. |
| **R12** | **Undisclosed Philippines operational footprint** | **Medium** | Support/ops team in the Philippines surfaced only inside S6, not in the responses. Access is policy-restricted but this is an undisclosed data-processing and control location. | Entity/contractor basis, headcount, access scope, personal-data transfer basis, control attestation. |
| **R13** | **Cross-border seller/buyer mismatch** | **Medium** | 30% of sellers in APAC (HK, Indonesia, Singapore, India) against 60% US / 30% EEA buyers. Their own §4 requires enhanced review of exactly this mismatch. | Evidence the geographic-mismatch control operates; seller-country breakdown of Checkout.com-bound volume; EDD for HK/Indonesia sellers. |
| **R14** | **MoR tax withholding does not reconcile — ~USD 800k/month unexplained** | **High** *(raised from Medium on receipt of S11)* | USD 4.4m payouts on USD 4.8m volume = 91.7% to sellers. Fungies' **own fund flow diagram** works an example in which the seller nets 74–75% of gross after fee and tax — implying payouts of ~USD 3.6m, not USD 4.4m. Either the volume/payout figures mean something other than stated, or tax is not being collected and remitted at the rates the MoR model requires. (§9.4b, §10.2) | Direct named question. Tax registrations (US states, EU OSS/IOSS, UK VAT) and remittance records; full gross→tax→fees→payouts reconciliation for one recent month. Resolve before the risk file closes. |
| **R15** | **Merchant concentration unknown** | **Medium** | No top-5/top-10 concentration data in any source. On this balance sheet, a single large merchant failure could exceed Fungies' entire asset base. | Concentration data; per-merchant caps; concentration covenant. |
| **R16** | **Stored-credential migration on the critical path** | **Medium** | If the 30% subscription volume includes migrating stored credentials from Stripe, a network-token/PAN migration is needed — both processors, network approval, lead time — against a December 2026 launch. (§9.5) | Resolve in the technical session. If migration is in scope, start the process immediately or launch new-subscriptions-only in Phase 1. |
| **R17** | **Single-MID / architecture change, not a port** | **Low-Medium** | Their Stripe model (direct charges on Express sub-accounts) has no Checkout.com equivalent; Fungies becomes the merchant on our platform. Cleaner, but a genuine redesign. (§9.2) | Lead item for Solutions Engineering. Agree MID structure, fee/tax split location, payout handoff and reconciliation. |
| **R18** | **PCI DSS position unknown** | **Low-Medium** | Not yet raised. Fungies operates hosted, embedded and direct-API checkout — so card data handling varies by integration mode. | Request SAQ/AOC, level and scope; confirm which integration modes are in scope for Checkout.com volume. |
| **R19** | **UAE / Korea claim unsubstantiated** | **Low** | Named as MoR jurisdictions on the call; absent from all written data, with no entity in either. (§10.5) | Clarify: tax registration, planned expansion, or undisclosed arrangement. |
| **R20** | **No calibrated transaction monitoring in operation** | **High** | S10 §3 requires a **Monitoring Threshold Register**; until it is "approved and operational" everything is a **manual alert**. The register was not provided. S10 §6 states expressly that the register and named data sources "must be attached **before external reliance is placed on live automated monitoring claims**." So by Fungies' own terms, post-onboarding monitoring is manual, uncalibrated, and not something we may rely on — across a portfolio going from ~100 to ~1,000 merchants. (§6.5.1a) | **Launch condition:** deliver the approved register with thresholds, owners, data sources, alert severities and response timelines, calibrated to Checkout.com and the relevant card-network programmes. Until then, treat Fungies' monitoring as zero-credit in our own risk model and size our monitoring accordingly. Agreed MI reporting to us. |
| **R21** | **PSP arbitrage — Checkout.com as the landing spot for Stripe-declined merchants** | **High** | The structural risk of a second pay-in rail: merchants Stripe has declined, limited or offboarded get routed to us, and it looks like ordinary "PSP choice." Fungies has anticipated exactly this — S10 §4 bars moving a merchant "to another payment provider for the same rejected activity" without written provider and CO approval — but the control is unsigned, untested, and enforced by the party with the commercial incentive. (§6.5.1b) | Mirror it **contractually**: express warranty + ongoing notification that no merchant declined, suspended, offboarded or limited by any provider for risk/compliance reasons is routed to Checkout.com volume without our prior written approval; audit right to test it; breach as a termination trigger. |

**Severity summary:** 2 Critical · 8 High · 4 Medium-High · 5 Medium · 3 Low/Low-Medium.

**The five to lead with:** R1 (licensing), R2 (balance sheet), R14 (tax reconciliation), R20 (no operative monitoring), R21 (PSP arbitrage). R1 and R2 are blocking; R14 and R20 are launch conditions; R21 is a contractual must-have specific to the second-rail architecture.

---

## 13. Assessment and recommended posture

**What is genuinely good here:**

- A **clean liability answer** — Fungies has confirmed unambiguously that it, not the underlying merchant, carries all chargeback and dispute liability to us, to the networks and to the end customer. Our counterparty is singular and unambiguous.
- **Well-designed policies.** The five documents are better than the stage of the company would suggest: correct hard stops, sales/compliance separation, transaction-laundering awareness, payout-beneficiary controls, a real reserve and set-off framework, and an anti-PSP-arbitrage clause that pre-empts the main structural risk of the deal.
- **Unusual drafting candour.** Twice the policies constrain what Fungies may claim to us — deferring the money-transmission question to counsel (S6 §1) and barring external reliance on automated-monitoring claims until the threshold register exists (S10 §6). Documents written purely to pass diligence do not usually include the sentences that undercut them.
- **A correct MoR tax construct on paper** — tax added on top of the seller's price, held separately, not treated as revenue, remitted to the end customer's jurisdiction (S11).
- **Credible vendor stack** — Didit for KYC/liveness, Sumsub for KYB/registry/UBO/screening, both used as evidence rather than as a decision.
- A **coherent commercial rationale**: PSP diversification off single-processor Stripe dependency, with real merchant demand for choice.
- **Responsiveness and candour.** Duke answered nearly everything, volunteered the revenue-vs-volume distinction himself, sent an unprompted follow-up to close the gaps he had left thin, and did not oversell the audit status of the financials. That matters in diligence.
- A **vertical we know** — SaaS and digital goods, CNP, mid-single-digit ATV, with declared exclusion of the categories we would refuse anyway.

**What has to be resolved:**

The gap is not the intent or the policy design — it is **substantiation**. Almost every control in the pack is well conceived and **none of it is yet evidenced as operating**. Two items are blocking:

1. **R1 — the licensing question.** Fungies' own compliance framework says the MSB/money-transmitter determination is unresolved and belongs to counsel. Until an opinion exists for the actual funds flow in each jurisdiction, we would be providing the acquiring infrastructure for a flow whose regulatory characterisation nobody has established.
2. **R2 — the balance sheet.** USD 225 of cash and USD 114k of assets, 99.8% of it a receivable from the incumbent processor, cannot support the MoR liability Fungies has correctly acknowledged as its own. The 2026 ramp may have changed this picture entirely — but the 2026 picture is currently an email figure, and the FY2025 accounts that do exist **do not internally reconcile** (R6).

And two are launch conditions that the later attachments surfaced:

3. **R14 — the tax reconciliation.** Fungies' own fund flow diagram implies sellers net 74–75% of gross; Fungies reports paying out 91.7%. That is roughly USD 800k/month unaccounted for, and one of the candidate explanations is that MoR tax is not being collected and remitted as represented. This needs a named answer, not a range.
4. **R20 — monitoring.** The Transaction Monitoring policy tells us in terms that its threshold register must exist "before external reliance is placed on live automated monitoring claims," and the register was not provided. We should therefore assume, for now, that Fungies contributes **no** reliable post-onboarding monitoring layer and size our own controls on that basis.

**Recommended posture:** proceed, in parallel, on the basis that this is a **conditional approval with a security package**, not a standard onboarding.

1. **Advance the technical track now** — the Solutions Engineering session does not depend on the risk outcome and de-risks the December timeline. Lead with the architecture change (R17) and the stored-credential migration question (R16), since the latter is on the critical path.
2. **Send a single consolidated follow-up list** (§11) rather than drip-feeding requests, and mark R1, R2, R6, R7 and the Stripe pricing breakdown as blocking for the proposal.
3. **Size the commercial proposal against the ramp, not the run-rate.** Year 1 is ~EUR 9.3m, not EUR 12m; the monthly minimum commitment should step with the ramp rather than assume the endpoint.
4. **Design the security package into the first proposal** — rolling reserve with a cap, stepped volume caps by ramp month, re-test at each step. Introducing it later reads as a downgrade; introducing it now reads as the structure of the deal.
5. **Do not treat the FY2025 accounts as stale until 2026 is documented.** They are the only audited-adjacent evidence we have, and they are the operative picture until replaced.

---

## 14. Next steps

| # | Action | Owner | Timing |
|---|---|---|---|
| 1 | Confirm NDA execution (DocuSign) | Giacomo | Immediate |
| 2 | Send consolidated follow-up request (§11), flagging R1/R2/R6/R7/R14/R20 + Stripe pricing as blocking | Giacomo | This week |
| 3 | **Raise the DSR with the completed pre-vet form** (`FUNGIES_IO_PREVET_FORM.md`) to Underwriting | Giacomo | This week |
| 4 | Put the tax reconciliation (R14) to Duke as a specific named question | Giacomo | This week |
| 5 | Schedule the technical session with Solutions Engineering — agenda per §9.4 and §9.5 | Giacomo / Duke | Next week (availability requested) |
| 6 | Route R1 (licensing / MoR legal basis) to Legal & Compliance for position | Giacomo → Legal | On receipt of counsel opinion |
| 7 | Route financials to Credit Risk with §7.5 breaks flagged; agree the security package | Giacomo → Credit | On receipt of 2026 financials |
| 8 | Build the commercial proposal against the ramped Year-1 volume with a stepped monthly minimum | Giacomo | After pricing data received |
| 9 | Agree MCC taxonomy and prohibited-category exclusions as launch conditions | Giacomo / Risk | Pre-contract |
| 10 | Confirm settlement-entity structure (R4) with Legal | Giacomo → Legal | Pre-contract |
| 11 | Request the Monitoring Threshold Register (R20); if it does not exist, set it as a launch condition and assume no monitoring credit | Giacomo / Risk | This week |
| 12 | Instruct Legal to draft the anti-PSP-arbitrage warranty, notification obligation and audit right (R21) | Giacomo → Legal | Pre-contract |

---

## Appendix A — Key identifiers quick reference

| Field | Value |
|---|---|
| Contracting entity | Fungies Inc., Delaware C-Corp |
| Delaware File No. | 7099716 |
| EIN | 92-0927516 |
| US address | 2100 Geng Road, Suite 210, Palo Alto, CA 94303 |
| EU operating entity | Fungies Europe Prosta Spółka Akcyjna |
| KRS | 0001137340 |
| NIP | 5214093272 |
| REGON | 540135615 |
| PL address | Al. Jerozolimskie 109/70, 02-011 Warsaw, Poland |
| PL incorporation | 8 November 2024 |
| PL share capital | PLN 10,000 (1,000,000 ordinary shares) |
| PL PKD | 62.01.Z |
| CEO / UBO | Hoang Duc Vu ("Duke") — 55% declared |
| Co-founder | Wojciech Harzowski — 40% declared |
| Compliance Officer | Agata Pisarek |
| Banking (US) | Mercury Bank, Brex |
| Incumbent PSP | Stripe (Connect, Express, direct charges) |
| KYC vendor | Didit |
| KYB vendor | Sumsub |
| MCC | 5734 (100% of portfolio) |
| Website | fungies.io |

## Appendix B — Figures quick reference

| Metric | Value |
|---|---|
| Current total volume | USD 4.8m/month (end July 2026) |
| Prior data point | USD 2.4m/month (mid-June 2026) |
| Payouts to sellers | USD 4.4m/month, ~2,694 payouts/month |
| Active merchants | ~100 (→ ~1,000 in 24 months) |
| ATV | USD 60–63 |
| Chargeback rate | <0.05% (asserted, unevidenced) |
| Fungies sell-side pricing | 5% + USD 0.50, all-inclusive |
| Checkout.com run-rate target | EUR 12m/year (EUR 1m/month) |
| Checkout.com Year 1 (Dec'26–Nov'27) | ~EUR 9.3m |
| Launch target | December 2026 |
| Mix | 70% one-off / 30% subscription |
| Payment methods | ~70% cards / ~20% wallets / ~10% APM |
| Buyer geography | US 60% / EEA 30% / IN-CA-AU 10% |
| Seller geography | EEA 40% / UK 20% / US 10% / HK 10% / ID-SG-IN 10% / CA-AU 10% |
| FY2025 revenue | USD 119,876 |
| FY2025 net loss | USD (232,657) |
| Cash at 31 Dec 2025 | **USD 225** |
| Total assets at 31 Dec 2025 | USD 113,982 |
| Total liabilities | USD 0 |
| SAFE notes (carried) | USD 250,000 |
| Payout cycle | T+7 automatic business-day |
| Rolling reserve (their sellers) | 10% per sample MoR agreement |
| Fund flow worked example (S11) | $12.00 charge = $10.00 net sale + $2.00 tax; fee $0.50 + 5%; seller nets ~$8.90–9.00 (**74–75% of gross**) |
| Reported payout ratio | **91.7%** (USD 4.4m / 4.8m) — irreconcilable with the above; see R14 |
