// T04 영상 틀: 미리보기·배경·투명 오버레이 생성과 alpha 검사
const path = require('path'), fs = require('fs');
const { pathToFileURL } = require('url');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const SLOT = { x: 108, y: 328, width: 864, height: 486 };
(async () => {
  const root = path.resolve(__dirname, '..'), out = path.join(root, 'video-template');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  for (const [src, dst] of [['video-preview.html', 'T04-preview.png'], ['video-clean.html', 'T04-background.png']]) {
    await page.goto(pathToFileURL(path.join(__dirname, src)).href);
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(() => { const c = document.querySelector('.card').getBoundingClientRect(), s = document.querySelector('.slot').getBoundingClientRect(); return { x: s.left - c.left, y: s.top - c.top, w: s.width, h: s.height }; });
    if (r.x !== 108 || r.y !== 328 || r.w !== 864 || r.h !== 486) throw new Error('slot mismatch ' + JSON.stringify(r));
    await page.locator('.card').screenshot({ path: path.join(out, dst) });
  }
  // 오버레이: 배경 PNG에서 창 영역 alpha=0
  const b64 = fs.readFileSync(path.join(out, 'T04-background.png')).toString('base64');
  await page.setViewportSize({ width: 1080, height: 1350 });
  await page.setContent('<canvas id=c width=1080 height=1350></canvas>');
  const res = await page.evaluate(async ({ b64, S }) => {
    const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
    const c = document.getElementById('c'), x = c.getContext('2d');
    x.drawImage(img, 0, 0); x.clearRect(S.x, S.y, S.width, S.height);
    const d = x.getImageData(0, 0, 1080, 1350).data; let bad = 0;
    for (let yy = 0; yy < 1350; yy++) for (let xx = 0; xx < 1080; xx++) {
      const inside = xx >= S.x && xx < S.x + S.width && yy >= S.y && yy < S.y + S.height;
      if (d[(yy * 1080 + xx) * 4 + 3] !== (inside ? 0 : 255)) bad++;
    }
    return { url: c.toDataURL('image/png'), bad };
  }, { b64, S: SLOT });
  fs.writeFileSync(path.join(out, 'T04-overlay.png'), Buffer.from(res.url.split(',')[1], 'base64'));
  await browser.close();
  if (res.bad) throw new Error('alpha check failed: ' + res.bad);
  fs.writeFileSync(path.join(out, 'placement.json'), JSON.stringify({ template: 'T04', card: '07', canvas: [1080, 1350], slots: [{ ...SLOT, ratio: '16:9' }] }, null, 2));
  console.log('PASS: preview/background/overlay, slot 108,328 864x486, alpha in=0 out=255');
})();
