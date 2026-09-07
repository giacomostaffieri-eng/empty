#!/usr/bin/env python3
"""Render the Fungies deal documents as designed PDFs."""

import re
import subprocess
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).parent
PROJ = Path("/home/user/empty")
CSS = (HERE / "style.css").read_text()

CHROME = "/opt/pw-browsers/chromium"


# ----------------------------------------------------------------- callouts

def classify(text):
    """Pick a callout style from the blockquote's leading label."""
    t = text.lstrip("> ").lstrip()
    low = t.lower()

    if "required document not provided" in low or "not provided.**" in low[:200]:
        return "gap"
    if "gap —" in low[:80] or "not provided" in low[:120]:
        return "gap"
    if low.startswith("⚠️"):
        # distinguish blocking items from ordinary flags
        if any(k in low for k in ("blocking", "highest priority", "the single biggest",
                                  "critical", "cannot support")):
            return "crit"
        return "warn"
    if low.startswith("**flag (highest priority") or "blocking." in low[:200]:
        return "crit"
    if low.startswith("**flag"):
        return "warn"
    if low.startswith("**assessment"):
        return "good"
    if low.startswith("**note") or low.startswith("**why this matters") \
       or low.startswith("**relevant") or low.startswith("*received"):
        return "note"
    if low.startswith("*"):
        return "note"
    if t.startswith('"') or low.startswith("*\"") or low.startswith('*"'):
        return "quote"
    if "verbatim" in low[:60]:
        return "quote"
    return "note"


LABELS = {
    "crit": "Critical — blocking",
    "warn": "Flag",
    "gap": "Gap — not provided",
    "note": "Note",
    "good": "Assessment",
    "quote": "Verbatim — prospect",
}


ACRONYMS = {"ubo", "mor", "mcc", "psp", "cko", "pci", "kyb", "kyc", "aml",
            "ceo", "co", "fx", "us", "uk", "eea", "uae", "safe", "nda", "mi",
            "qc", "dsr", "maf", "mac", "atv", "sla", "edd", "pep"}


def titlecase(label):
    """Preserve acronym casing when a callout label becomes a sentence lead."""
    words = label.strip().split()
    out = []
    for i, w in enumerate(words):
        core = w.strip("()/,.")
        if core.lower() in ACRONYMS:
            out.append(w.replace(core, core.upper()))
        elif i == 0:
            out.append(w[:1].upper() + w[1:])
        else:
            out.append(w)
    return " ".join(out)


def strip_label(body, kind):
    """Remove the redundant inline label now that the callout has a chrome label."""
    if kind == "warn":
        body = re.sub(r"^\*\*Flag(?:\s*\(([^)]*)\))?:?\*\*\s*",
                      lambda m: f"**{titlecase(m.group(1))}.** " if m.group(1) else "",
                      body, count=1)
    elif kind == "crit":
        body = re.sub(r"^\*\*Flag\s*\(([^)]*)\):?\*\*\s*",
                      lambda m: f"**{titlecase(m.group(1))}.** ", body, count=1)
    elif kind == "note":
        body = re.sub(r"^\*\*Note(?:\s*\(([^)]*)\))?:?\*\*\s*",
                      lambda m: f"**{titlecase(m.group(1))}.** " if m.group(1) else "",
                      body, count=1)
    elif kind == "good":
        body = re.sub(r"^\*\*Assessment:?\*\*\s*", "", body, count=1)
    body = body.replace("⚠️ ", "").replace("⚠️", "")
    return body


def convert_blockquotes(md):
    """Turn '>' blocks into styled callout divs (md_in_html keeps markdown inside)."""
    lines = md.split("\n")
    out, buf = [], []

    def flush():
        if not buf:
            return
        raw = "\n".join(buf)
        kind = classify(raw)
        body = "\n".join(re.sub(r"^>\s?", "", l) for l in buf).strip()
        body = strip_label(body, kind)
        out.append(f'<div class="callout {kind}" markdown="1">\n\n{body}\n\n</div>\n')
        buf.clear()

    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith(">"):
            buf.append(line)
        elif not in_fence and buf and line.strip() == "":
            flush()
            out.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out)


# ----------------------------------------------------------------- badges

SEV = {
    "Critical": "sev-critical",
    "High": "sev-high",
    "Medium-High": "sev-medhigh",
    "Medium": "sev-medium",
    "Low-Medium": "sev-low",
    "Low": "sev-low",
}


def badge_severities(html):
    """Colour-code the severity column and risk IDs in the risk register."""
    def sev_repl(m):
        cell, label, tail = m.group(1), m.group(2), m.group(3)
        cls = SEV.get(label)
        if not cls:
            return m.group(0)
        return f'{cell}<span class="badge {cls}">{label}</span>{tail}'

    html = re.sub(
        r"(<td>)<strong>(Critical|High|Medium-High|Medium|Low-Medium|Low)</strong>(\s|<|$)",
        sev_repl, html)

    # risk IDs: <td><strong>R1</strong>
    html = re.sub(r"(<td>)<strong>(R\d{1,2})</strong>",
                  r'\1<span class="rid">\2</span>', html)
    return html


def style_financial_tables(html):
    """Right-align numeric tables."""
    def repl(m):
        tbl = m.group(0)
        head = tbl[:tbl.find("</thead>")] if "</thead>" in tbl else tbl[:400]
        if re.search(r"FY 20\d\d|DEC 31|31 Dec 20\d\d|Dec 31", head):
            return tbl.replace("<table>", '<table class="fin">', 1)
        return tbl
    return re.sub(r"<table>.*?</table>", repl, html, flags=re.S)


# ----------------------------------------------------------------- assembly

def render(md_body, extras):
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "md_in_html", "attr_list", "toc", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "1-2", "anchorlink": False}},
    )
    html = md.convert(md_body)
    html = badge_severities(html)
    html = style_financial_tables(html)
    toc = md.toc

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{extras['title']}</title>
<style>{CSS}</style>
</head><body>

{extras['cover']}

<div class="toc-wrap">
<div class="toc-title">Contents</div>
<div class="toc">{toc}</div>
</div>

{extras.get('tiles','')}

{html}
</body></html>"""


def cover(eyebrow, title, sub, meta, foot):
    rows = "".join(
        f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta
    )
    return f"""<div class="cover">
<div class="cover-rule"></div>
<div class="cover-eyebrow">{eyebrow}</div>
<h1>{title}</h1>
<div class="sub">{sub}</div>
<dl class="cover-meta">{rows}</dl>
<div class="cover-spacer"></div>
<div class="cover-foot">{foot}</div>
</div>"""


def tiles(label, items, cols=4):
    cls = "tiles" + (" tiles-3" if cols == 3 else "")
    cells = "".join(
        f'<div class="tile {t.get("k","")}"><div class="tile-k">{t["label"]}</div>'
        f'<div class="tile-v">{t["value"]}</div>'
        f'<div class="tile-n">{t["note"]}</div></div>'
        for t in items)
    return f'<div class="tiles-label">{label}</div><div class="{cls}">{cells}</div>'


def strip_front_matter(md_text, drop_until):
    """Remove the markdown title block; the cover page replaces it."""
    idx = md_text.find(drop_until)
    return md_text[idx:] if idx > -1 else md_text


def to_pdf(html, out_pdf, tag):
    html_path = HERE / f"{tag}.html"
    html_path.write_text(html)
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=12000",
        f"--print-to-pdf={out_pdf}",
        f"file://{html_path}",
    ], check=True, capture_output=True, timeout=240)
    return out_pdf
