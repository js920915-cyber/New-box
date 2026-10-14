// 사용자 사진/영상 카드: 빈 배경·투명 오버레이 생성 + 자리 좌표·alpha 검사
// 사용: python3 source/build_cards.py && node source/render_media.cjs
const path = require('path'), fs = require('fs');
const { pathToFileURL } = require('url');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
(async () => {
  const root = path.resolve(__dirname, '..'), out = path.join(root, 'media-template');
  const slots = JSON.parse(fs.readFileSync(path.join(__dirname, 'slots.json')));
  const cardsWithSlots = [...new Set(slots.map(s => s.card))];
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  await page.goto(pathToFileURL(path.join(__dirname, 'cards-clean.html')).href);
  await page.evaluate(() => document.fonts.ready);
  for (const n of cardsWithSlots) {
    const dom = await page.evaluate(id => {
      const c = document.getElementById(id).getBoundingClientRect();
      return [...document.querySelectorAll('#' + id + ' .slot')].map(e => { const r = e.getBoundingClientRect(); return { id: e.dataset.slot, x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height }; });
    }, 'c' + n);
    for (const s of slots.filter(s => s.card === n)) {
      const d = dom.find(d => d.id === s.id);
      if (!d || d.x !== s.x || d.y !== s.y || d.w !== s.width || d.h !== s.height) throw new Error('slot mismatch ' + s.id + ' ' + JSON.stringify(d));
    }
    await page.locator('#c' + n).screenshot({ path: path.join(out, n + '-background.png') });
    fs.copyFileSync(path.join(root, 'exports', n + '.png'), path.join(out, n + '-preview.png'));
  }
  const cv = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  await cv.setContent('<canvas id=c width=1080 height=1350></canvas>');
  for (const n of cardsWithSlots) {
    const b64 = fs.readFileSync(path.join(out, n + '-background.png')).toString('base64');
    const S = slots.filter(s => s.card === n);
    const res = await cv.evaluate(async ({ b64, S }) => {
      const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
      const c = document.getElementById('c'), x = c.getContext('2d');
      x.clearRect(0, 0, 1080, 1350); x.drawImage(img, 0, 0);
      for (const s of S) x.clearRect(s.x, s.y, s.width, s.height);
      const d = x.getImageData(0, 0, 1080, 1350).data; let bad = 0;
      for (let yy = 0; yy < 1350; yy++) for (let xx = 0; xx < 1080; xx++) {
        const inside = S.some(s => xx >= s.x && xx < s.x + s.width && yy >= s.y && yy < s.y + s.height);
        if (d[(yy * 1080 + xx) * 4 + 3] !== (inside ? 0 : 255)) bad++;
      }
      return { url: c.toDataURL('image/png'), bad };
    }, { b64, S });
    if (res.bad) throw new Error(n + ' alpha check failed ' + res.bad);
    fs.writeFileSync(path.join(out, n + '-overlay.png'), Buffer.from(res.url.split(',')[1], 'base64'));
  }
  await browser.close();
  fs.writeFileSync(path.join(out, 'placement.json'), JSON.stringify({ canvas: [1080, 1350], slots }, null, 2));
  console.log('PASS:', cardsWithSlots.join(','), '— background/overlay/preview, slot coords match, alpha in=0 out=255');
})();
