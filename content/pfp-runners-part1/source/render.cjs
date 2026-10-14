// 사용: node source/render.cjs  (playwright 전역 설치 또는 NODE_PATH 필요)
const path = require('path'), fs = require('fs');
const { pathToFileURL } = require('url');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(__dirname, 'cards.html')).href);
  await page.evaluate(() => document.fonts.ready);
  const report = await page.evaluate(() => {
    const out = [];
    for (const card of document.querySelectorAll('article.card')) {
      const c = card.getBoundingClientRect();
      const errors = [];
      let bottom = 0, top = 1e9;
      const walker = document.createTreeWalker(card, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        if (!n.textContent.trim() || n.parentElement.closest('svg')) continue;
        const r = document.createRange(); r.selectNodeContents(n);
        for (const rr of r.getClientRects()) {
          bottom = Math.max(bottom, rr.bottom - c.top); top = Math.min(top, rr.top - c.top);
          if (rr.left - c.left < 88 || rr.right - c.left > 992) errors.push('text outside safe x: ' + n.textContent.slice(0, 20));
        }
      }
      for (const v of card.querySelectorAll('svg:not(.card-frame), img, .cover-art, .callout, .next')) {
        const r = v.getBoundingClientRect();
        bottom = Math.max(bottom, r.bottom - c.top);
        if (r.left - c.left < 88 || r.right - c.left > 992) errors.push('visual outside safe x: ' + v.className.baseVal ?? v.className);
      }
      for (const e of card.querySelectorAll('*')) {
        if (e.closest('svg')) continue;
        if (e.clientWidth && e.scrollWidth > e.clientWidth + 1) errors.push('h-overflow ' + e.className);
      }
      if (bottom > 1252) errors.push('content below safe bottom');
      const fs = {};
      for (const e of card.querySelectorAll('h1,h2,h3,p,.big-num,.num-label,.tag')) {
        const s = getComputedStyle(e); fs[e.className || e.tagName] = s.fontSize + '/' + s.fontWeight;
      }
      out.push({ id: card.id, contentTop: Math.round(top), contentBottom: Math.round(bottom), bottomGap: Math.round(1316 - bottom), fonts: fs, errors });
    }
    return out;
  });
  const exp = path.join(root, 'exports'), qa = path.join(root, 'qa');
  for (const r of report) {
    const n = r.id.slice(1);
    const p = path.join(exp, n + '.png');
    await page.locator('#' + r.id).screenshot({ path: p });
  }
  // 360px 미리보기
  const small = await browser.newPage({ viewport: { width: 360, height: 450 } });
  for (const r of report) {
    const n = r.id.slice(1);
    const b64 = fs.readFileSync(path.join(exp, n + '.png')).toString('base64');
    await small.setContent(`<body style="margin:0"><img src="data:image/png;base64,${b64}" style="width:360px;height:450px;display:block"></body>`);
    await small.screenshot({ path: path.join(qa, n + '-mobile.png') });
  }
  await browser.close();
  fs.writeFileSync(path.join(qa, 'layout-check.json'), JSON.stringify(report, null, 2));
  for (const r of report) console.log(r.id, 'bottom', r.contentBottom, 'gap', r.bottomGap, r.errors.length ? r.errors : 'OK');
})();
