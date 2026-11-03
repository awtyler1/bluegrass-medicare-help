// Render a social card: node docs/og/render.js <slug>
// Serves nothing itself: start `python3 -m http.server 8765` at the repo root first.
// Reads docs/og/<slug>.html and writes assets/og/<slug>.png at 1200x630.
const { chromium } = require('playwright');
const slug = process.argv[2];
if (!slug) { console.error('usage: node docs/og/render.js <slug>'); process.exit(1); }
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.goto(`http://localhost:8765/docs/og/${slug}.html`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  if (!(await p.evaluate(() => document.fonts.check('800 40px Figtree')))) throw new Error('Figtree did not load');
  await p.screenshot({ path: `assets/og/${slug}.png` });
  await b.close();
  console.log(`wrote assets/og/${slug}.png`);
})();
