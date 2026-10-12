// Render an SVG concept painting to JPG/PNG with headless Chromium.
// usage: node render.js in.svg out.jpg [width height]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [inp, out, w = '1600', h = '900'] = process.argv.slice(2);
  const svg = fs.readFileSync(inp, 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h } });
  await page.setContent(
    `<html><body style="margin:0;background:#000">${svg}</body></html>`
  );
  await page.waitForTimeout(300);
  const type = path.extname(out) === '.png' ? 'png' : 'jpeg';
  await page.screenshot({
    path: out,
    type,
    ...(type === 'jpeg' ? { quality: 90 } : { omitBackground: true }),
    clip: { x: 0, y: 0, width: +w, height: +h },
  });
  await browser.close();
})();
