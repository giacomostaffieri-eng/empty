#!/usr/bin/env python3
"""Build both Fungies PDFs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import (HERE, PROJ, convert_blockquotes, cover, render,
                   strip_front_matter, tiles, to_pdf)

CONF = ("<strong>CONFIDENTIAL — internal Checkout.com use only.</strong> "
        "Contains Fungies Inc. confidential information received under NDA and "
        "third-party personal data (UBOs, SAFE investors). Handle in line with "
        "internal data-handling rules. Do not forward externally.")

# ==================================================================== BRIEF

brief_md = (PROJ / "FUNGIES_IO_MASTER_BRIEF.md").read_text()
brief_md = strip_front_matter(brief_md, "## 1. Document purpose")

brief_cover = cover(
    eyebrow="Merchant of Record · Pre-vet &amp; risk assessment",
    title="Fungies.io",
    sub="Master opportunity, compliance and risk brief — direct pay-in "
        "processing partnership",
    meta=[
        ("Prospect", "Fungies Inc. (Delaware) / Fungies.io"),
        ("Contact", "Hoang Duc Vu (“Duke”) — CEO &amp; co-founder"),
        ("Deal owner", "Giacomo Staffieri, Checkout.com"),
        ("Opportunity", "~EUR 12m/yr run-rate · launch Dec 2026"),
        ("Document date", "7 September 2026"),
        ("Status", "Information gathering complete · 2 blocking items"),
    ],
    foot=CONF + "<br><br>Companion document: <em>Pre-vet Form for Direct "
                "Sellers — Fungies Inc.</em> (completed, for the DSR).",
)

brief_tiles = tiles("The opportunity at a glance", [
    dict(label="Run-rate target", value="€12m", note="per year (~€1m/month); "
         "Year 1 ~€9.3m on a 6-month ramp"),
    dict(label="Launch target", value="Dec 2026", note="Full run-rate from "
         "month 6 (May 2027)"),
    dict(label="Current platform volume", value="$4.8m", note="per month "
         "(all rails, Stripe) as at end July 2026"),
    dict(label="Average ticket", value="$60–63", note="~150–160k transactions "
         "in Year 1"),
]) + tiles("The counterparty at a glance", [
    dict(label="Cash at 31 Dec 2025", value="$225", note="Against FY2025 net "
         "cash burn of ~$346k", k="alarm"),
    dict(label="Total assets", value="$113,982", note="99.8% of it a "
         "receivable from Stripe", k="alarm"),
    dict(label="Payment licence", value="None", note="No exemption cited; no "
         "counsel opinion on the MoR construct", k="alarm"),
    dict(label="Chargeback liability", value="100% Fungies", note="Confirmed "
         "in writing — not the underlying sellers", k="good"),
]) + tiles("Risk register — 21 items", [
    dict(label="Critical / blocking", value="2", note="R1 licensing · R2 "
         "balance sheet", k="alarm"),
    dict(label="High", value="8", note="Incl. R14 tax reconciliation, R20 "
         "monitoring, R21 PSP arbitrage"),
    dict(label="Medium-High", value="4", note="MCC coding, subscription "
         "disputes, 10x merchant growth"),
    dict(label="Medium &amp; below", value="7", note="UBO, footprint, "
         "concentration, PCI, migration"),
])

brief_html = render(convert_blockquotes(brief_md), {
    "title": "Fungies.io — Master Opportunity & Risk Brief",
    "cover": brief_cover,
    "tiles": brief_tiles,
})

to_pdf(brief_html, PROJ / "Fungies_io_Master_Brief.pdf", "brief")
print("built brief")

# ================================================================= PRE-VET

pv_md = (PROJ / "FUNGIES_IO_PREVET_FORM.md").read_text()
pv_md = strip_front_matter(pv_md, "> **Note to Underwriting.**")

pv_cover = cover(
    eyebrow="Internal · Pre-qualification assessment",
    title="Pre-vet Form for Direct Sellers",
    sub="Fungies Inc. (Fungies.io) — completed for submission with the Deal "
        "Support Request",
    meta=[
        ("Completed by", "Giacomo Staffieri, Commercial"),
        ("Date", "7 September 2026"),
        ("Legal entity", "Fungies Inc., Delaware C-Corp"),
        ("Line of business", "Merchant of Record / payment platform"),
        ("Volume via CKO", "~EUR 12m/yr run-rate · ~EUR 9.3m Year 1"),
        ("Recommendation", "Conditional — 2 items blocking for MAF"),
    ],
    foot=CONF + "<br><br>Full analysis, source references (S1–S12) and the "
                "21-item risk register: <em>Fungies.io — Master Opportunity, "
                "Compliance and Risk Brief</em>.",
)

pv_tiles = tiles("Pre-vet outcome", [
    dict(label="Fields completed", value="15 of 15", note="Every requirement "
         "answered; gaps marked in-field", k="good"),
    dict(label="Blocking for MAF", value="2", note="MoR legal basis · "
         "financial standing", k="alarm"),
    dict(label="Launch conditions", value="6", note="Tax reconciliation, "
         "monitoring register, MCC, categories, policies, settlement entity"),
    dict(label="Items outstanding", value="23", note="2 deferred by prospect · "
         "6 unanswered · 15 newly identified"),
], cols=4) + tiles("Required documents — supply status", [
    dict(label="Financial statements", value="Provided", note="FY2025 "
         "unaudited management accounts; 6 internal inconsistencies",
         k="alarm"),
    dict(label="Funds flow diagram", value="Provided", note="Stripe Connect "
         "direct-charge model; economics contradict payout data", k="alarm"),
    dict(label="Policies", value="5 provided", note="All v1.0, dated Aug 2026, "
         "all approval blocks blank", k="alarm"),
    dict(label="3-month processing data", value="Not provided", note="Required "
         "by the form; deferred by the prospect", k="alarm"),
], cols=4)

pv_html = render(convert_blockquotes(pv_md), {
    "title": "Pre-vet Form — Fungies Inc.",
    "cover": pv_cover,
    "tiles": pv_tiles,
})

to_pdf(pv_html, PROJ / "Fungies_io_Prevet_Form.pdf", "prevet")
print("built prevet")
