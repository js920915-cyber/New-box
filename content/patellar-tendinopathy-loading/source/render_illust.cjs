// source/illust/*.html → assets/illust/*.png (SVG 크기 그대로, 2배 해상도)
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
(async () => {
  const dir = path.join(__dirname, 'illust'), out = path.join(__dirname, '../assets/illust');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    const [, w, h] = html.match(/width="(\d+)" height="(\d+)"/);
    const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(dir, f));
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')) }); await p.close();
  }
  await b.close();
})();
