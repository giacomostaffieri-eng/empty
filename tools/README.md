# html_to_a4_pdf.js

Renders standalone HTML documents to print-ready A4 PDFs with headless Chromium.

```bash
NODE_PATH=$(npm root -g) node tools/html_to_a4_pdf.js in1.html out1.pdf [in2.html out2.pdf ...]
```

Requires a global `playwright` install and a Chromium browser it can find.

## What it handles

Each `.page` element in the source is mapped onto exactly one A4 sheet
(210 x 297 mm, zero printer margin, backgrounds on):

- **Page fits** — printed as-is.
- **Page slightly too tall** — its content is scaled down (down to 0.85x) to
  fit one sheet. The scale is applied to an inner wrapper rather than the
  `.page` box itself, so full-bleed backgrounds and borders still reach all
  four edges.
- **Page much too tall** — allowed to flow onto a second sheet instead of
  being shrunk into illegibility. Cut-out elements (tokens, cards, slips) get
  `break-inside: avoid` so nothing is split across the fold.

It also works around two problems common to hand-authored HTML kits:

- A `@import` of Google Fonts placed *after* an `@page` rule is invalid and
  silently loads nothing. The stylesheet is fetched separately, with every
  woff2 inlined as a data URI, and injected properly.
- `<img>` icons on unreachable hosts render as broken alt text. Images whose
  `alt` matches the `GLYPHS` map are replaced with an equivalent emoji glyph.

The per-sheet scale/flow decisions are printed to stdout for each file.
