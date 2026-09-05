const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const SHEET_MM = 296.5;          // usable height on a 297mm A4 sheet
const MIN_SCALE = 0.85;          // below this, let the page flow onto extra sheets

const FONTS_HREF = 'https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900'
  + '&family=Cinzel:wght@700;900&family=Special+Elite'
  + '&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Pirata+One&family=Nosifer&display=swap';

const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
  + 'Chrome/131.0.0.0 Safari/537.36';

const GLYPHS = {
  'dagger': '\u{1F5E1}\u{FE0F}',
  'poison vial': '\u{1F9EA}',
  'revolver': '\u{1F52B}',
  'candlestick': '\u{1F56F}\u{FE0F}',
  'noose rope': '\u{1FA9A}',
};

const PRINT_CSS = `
@page { size: A4 portrait; margin: 0 !important; }
html { background: #fff !important; }
body { margin: 0 !important; padding: 0 !important; background: #fff !important; }

.a4-sheet {
  width: 210mm;
  height: ${SHEET_MM}mm;
  overflow: hidden;
  position: relative;
  margin: 0;
  break-after: page;
  page-break-after: always;
}
.a4-sheet.is-flow { height: auto; overflow: visible; }
.a4-sheet:last-of-type { break-after: auto; page-break-after: auto; }

.page {
  margin: 0 !important;
  width: 210mm !important;
  min-height: ${SHEET_MM}mm !important;
  outline: none !important;
  box-shadow: inset 0 0 60px rgba(50,25,10,0.45), inset 0 0 12px rgba(0,0,0,0.35) !important;
  break-after: auto !important;
  page-break-after: auto !important;
  transform-origin: top center;
}
.fit-inner { transform-origin: top center; }
.a4-sheet.is-flow .page { min-height: 0 !important; }

/* stand-in glyphs for the unreachable weapon icons */
.glyph-swap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11mm !important;   /* beats the .token-item span rule */
  line-height: 1;
  z-index: 1;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.55));
}

/* keep cut-out tokens whole when a sheet spans two pages */
.tokens-grid {
  display: flex !important;
  flex-wrap: wrap;
  gap: 3mm;
  justify-content: center;
  align-content: flex-start;
}
.token-item, .card, .char-card, .ability-card, .clue-card, .vote-slip {
  break-inside: avoid;
  page-break-inside: avoid;
}
`;

// Fetch the Google Fonts stylesheet and inline every woff2 as a data URI, so
// the render never depends on the browser reaching the network.
function buildFontCss() {
  const cachePath = path.join(os.tmpdir(), 'a4-fonts-inline.css');
  if (fs.existsSync(cachePath)) return fs.readFileSync(cachePath, 'utf8');

  const get = (url, binary) => execFileSync('curl', ['-sSfL', '-A', UA, url],
    { encoding: binary ? 'buffer' : 'utf8', maxBuffer: 64 * 1024 * 1024 });

  let css = get(FONTS_HREF, false);
  const urls = [...new Set(css.match(/https:\/\/fonts\.gstatic\.com\/[^)]+/g) || [])];
  for (const u of urls) {
    const b64 = get(u, true).toString('base64');
    css = css.split(u).join('data:font/woff2;base64,' + b64);
  }
  fs.writeFileSync(cachePath, css);
  return css;
}

const FONT_CSS = buildFontCss();

async function convert(browser, src, out) {
  const page = await browser.newPage({ viewportSize: { width: 1000, height: 1400 } });
  await page.goto('file://' + path.resolve(src), { waitUntil: 'load' });

  // The source HTML puts @import after @page, which makes the Google Fonts
  // import invalid, so none of the display faces ever load. Inject them inline.
  await page.addStyleTag({ content: FONT_CSS });

  // The weapon icons live on a host this network can't reach, so every <img>
  // renders as broken alt text. Swap them for equivalent glyphs.
  await page.evaluate((map) => {
    document.querySelectorAll('img').forEach((img) => {
      const glyph = map[(img.alt || '').trim().toLowerCase()];
      if (!glyph) return;
      const span = document.createElement('span');
      span.className = 'glyph-swap';
      span.textContent = glyph;
      const cs = getComputedStyle(img);
      span.style.width = cs.width;
      span.style.height = cs.height;
      span.style.marginBottom = cs.marginBottom;
      img.replaceWith(span);
    });
  }, GLYPHS);

  try { await page.evaluate(() => document.fonts.ready); } catch (e) {}
  await page.waitForTimeout(2500);
  await page.addStyleTag({ content: PRINT_CSS });
  await page.emulateMedia({ media: 'print' });

  // wrap every .page in a fixed-height A4 sheet
  await page.evaluate(() => {
    document.querySelectorAll('.page').forEach((pg) => {
      const sheet = document.createElement('div');
      sheet.className = 'a4-sheet';
      pg.parentNode.insertBefore(sheet, pg);
      sheet.appendChild(pg);
    });
  });
  await page.waitForTimeout(1200);

  // measure, then shrink-to-fit or mark as flowing
  const report = await page.evaluate(({ SHEET_MM, MIN_SCALE }) => {
    const mm = 96 / 25.4;
    const rows = [];
    document.querySelectorAll('.a4-sheet').forEach((sheet, i) => {
      const pg = sheet.querySelector('.page');
      const h = pg.scrollHeight / mm;
      let scale = 1, mode = 'fits';
      if (h > SHEET_MM + 0.5) {
        // Scale the content, not the .page box, so the parchment and its
        // burnt frame still bleed to all four edges of the sheet.
        const cs = getComputedStyle(pg);
        const padT = parseFloat(cs.paddingTop) / mm;
        const padB = parseFloat(cs.paddingBottom) / mm;
        scale = (SHEET_MM - padT - padB) / (h - padT - padB);
        if (scale >= MIN_SCALE) {
          const inner = document.createElement('div');
          inner.className = 'fit-inner';
          while (pg.firstChild) inner.appendChild(pg.firstChild);
          pg.appendChild(inner);
          inner.style.transform = `scale(${scale})`;
          pg.style.height = SHEET_MM + 'mm';
          pg.style.minHeight = SHEET_MM + 'mm';
          pg.style.overflow = 'hidden';
          mode = 'scaled';
        } else {
          sheet.classList.add('is-flow');
          scale = 1;
          mode = 'flow';
        }
      }
      rows.push({ n: i + 1, h: +h.toFixed(1), scale: +scale.toFixed(3), mode });
    });
    return rows;
  }, { SHEET_MM, MIN_SCALE });

  await page.waitForTimeout(800);
  await page.pdf({
    path: out,
    width: '210mm',
    height: '297mm',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
    preferCSSPageSize: false,
  });
  await page.close();
  return report;
}

(async () => {
  const jobs = process.argv.slice(2);
  const browser = await chromium.launch();
  for (let i = 0; i < jobs.length; i += 2) {
    const rep = await convert(browser, jobs[i], jobs[i + 1]);
    console.log('### ' + path.basename(jobs[i + 1]));
    for (const r of rep) {
      if (r.mode !== 'fits') console.log(`   sheet ${r.n}: ${r.h}mm -> ${r.mode} ${r.mode === 'scaled' ? '(x' + r.scale + ')' : ''}`);
    }
  }
  await browser.close();
})();
