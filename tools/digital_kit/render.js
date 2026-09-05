// Render phone-shaped HTML screens to PDFs (one .page per PDF page) or PNGs.
//
//   render.js pdf  out.pdf  in.html [in2.html ...]     concatenates all screens
//   render.js png  outDir   in.html [in2.html ...]     one PNG per screen
//
// Screens that overflow their page get their content scaled down to fit, so a
// packet always has exactly as many pages as it has .page elements.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { buildFontCss } = require('../fonts');

const PAGE_W = 420;      // css px, 9:19.5 -- fills a phone screen edge to edge
const PAGE_H = 910;
const SCALE = 2.5;       // PNG oversampling

const FONT_CSS = buildFontCss();

const PRINT_CSS = `
@page { size: ${PAGE_W}px ${PAGE_H}px; margin: 0 !important; }
html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; }
.page {
  break-after: page;
  page-break-after: always;
  break-inside: avoid;
  height: ${PAGE_H}px !important;
  min-height: ${PAGE_H}px !important;
  overflow: hidden !important;
}
.page:last-of-type { break-after: auto; page-break-after: auto; }
.fit-inner { transform-origin: top center; }
`;

async function prepare(page, src) {
  await page.goto('file://' + path.resolve(src), { waitUntil: 'load' });
  await page.addStyleTag({ content: FONT_CSS });
  await page.addStyleTag({ content: PRINT_CSS });
  await page.emulateMedia({ media: 'print' });
  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await page.waitForTimeout(400);

  // Shrink any screen whose content is taller than the page. Only the .sheet
  // is scaled, so the parchment and its frame still reach every edge.
  return page.evaluate(({ PAGE_H }) => {
    const scaled = [];
    document.querySelectorAll('.page').forEach((el, i) => {
      const sheet = el.querySelector('.sheet');
      if (!sheet) return;
      const cs = getComputedStyle(sheet);
      const pad = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
      const avail = PAGE_H - pad;
      if (sheet.scrollHeight - pad > avail + 0.5) {
        // A centred sheet overflows both ways; anchor it to the top first so
        // scaling from `top center` can't clip the head of the content.
        sheet.style.justifyContent = 'flex-start';
        const s = avail / (sheet.scrollHeight - pad);
        sheet.style.transform = `scale(${s})`;
        scaled.push(`${i + 1}:${s.toFixed(3)}`);
      }
    });
    return scaled;
  }, { PAGE_H });
}

async function main() {
  const [mode, dest, ...sources] = process.argv.slice(2);
  if (!['pdf', 'png'].includes(mode) || !dest || !sources.length) {
    console.error('usage: render.js <pdf|png> <out.pdf|outDir> <in.html...>');
    process.exit(2);
  }

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewportSize: { width: PAGE_W, height: PAGE_H },
    deviceScaleFactor: mode === 'png' ? SCALE : 1,
  });

  if (mode === 'pdf') {
    // One document at a time keeps page numbering per-source; callers pass a
    // single source when they care about that.
    if (sources.length > 1) throw new Error('pdf mode takes one source');
    const scaled = await prepare(page, sources[0]);
    await page.pdf({
      path: dest,
      width: `${PAGE_W}px`,
      height: `${PAGE_H}px`,
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
    });
    console.log(`${path.basename(dest)}${scaled.length ? '  scaled ' + scaled.join(' ') : ''}`);
  } else {
    fs.mkdirSync(dest, { recursive: true });
    for (const src of sources) {
      const scaled = await prepare(page, src);
      const els = await page.$$('.page');
      const stem = path.basename(src, '.html');
      for (const [i, el] of els.entries()) {
        const name = els.length > 1 ? `${stem}-${i + 1}.png` : `${stem}.png`;
        await el.screenshot({ path: path.join(dest, name) });
      }
      console.log(`${stem}: ${els.length} png${scaled.length ? '  scaled ' + scaled.join(' ') : ''}`);
    }
  }

  await browser.close();
}

main();
