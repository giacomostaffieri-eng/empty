const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
  + 'Chrome/131.0.0.0 Safari/537.36';

const HREF = 'https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900'
  + '&family=Cinzel:wght@700;900&family=Special+Elite'
  + '&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Pirata+One&family=Nosifer&display=swap';

// Fetch the Google Fonts stylesheet and inline every woff2 as a data URI, so
// rendering never depends on the browser reaching the network.
function buildFontCss() {
  const cachePath = path.join(os.tmpdir(), 'a4-fonts-inline.css');
  if (fs.existsSync(cachePath)) return fs.readFileSync(cachePath, 'utf8');

  const get = (url, binary) => execFileSync('curl', ['-sSfL', '-A', UA, url],
    { encoding: binary ? 'buffer' : 'utf8', maxBuffer: 64 * 1024 * 1024 });

  let css = get(HREF, false);
  const urls = [...new Set(css.match(/https:\/\/fonts\.gstatic\.com\/[^)]+/g) || [])];
  for (const u of urls) {
    css = css.split(u).join('data:font/woff2;base64,' + get(u, true).toString('base64'));
  }
  fs.writeFileSync(cachePath, css);
  return css;
}

module.exports = { buildFontCss, FONTS_HREF: HREF, UA };
