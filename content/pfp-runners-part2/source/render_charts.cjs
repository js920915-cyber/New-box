// source/charts/*.html → assets/charts/*.png (888×560, 2배 해상도)
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
(async () => {
  const dir = path.join(__dirname, 'charts'), out = path.join(__dirname, '../assets/charts');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 888, height: 560 }, deviceScaleFactor: 2 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    await p.goto('file://' + path.join(dir, f)); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')) });
  }
  await b.close();
})();
