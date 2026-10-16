// Linux(클라우드)용 render.ps1 + extract_layers.ps1: Playwright Chromium으로 같은 qa.js·layers.js를 실행한다.
// 출력: exports/NN.png, qa/NN-mobile.png, qa/layout-check.json, adobe-express/build/layers.json(+ NN-photoK.png)
// 사용: node tools/cardkit/linux_render.cjs content/<slug>
const fs = require('fs'), path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

(async () => {
  const root = path.resolve(process.argv[2]);
  const src = path.join(root, 'source'), build = path.join(root, 'adobe-express/build');
  for (const d of ['exports', 'qa']) fs.mkdirSync(path.join(root, d), { recursive: true });
  fs.mkdirSync(build, { recursive: true });
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const results = [], cards = [];
  const htmls = fs.readdirSync(src).filter(f => /^\d\d\.html$/.test(f)).sort();
  const readPre = async id => { await page.waitForSelector('#' + id, { state: 'attached', timeout: 15000 }); return JSON.parse(await page.$eval('#' + id, e => e.textContent)); };
  for (const f of htmls) {
    const n = f.slice(0, 2), url = 'file://' + path.join(src, f);
    await page.goto(url); await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(root, `exports/${n}.png`) });
    await page.goto(url + '?qa'); const qa = await readPre('qa-out');
    await page.goto(url + '?layers'); const data = await readPre('layers-out');
    let k = 0;
    for (const s of data.shapes.filter(s => s.type === 'photo')) {
      k++;
      const scale = Math.max(1, s.img.naturalW / s.img.w);
      const p2 = await browser.newPage({ viewport: { width: Math.round(s.w), height: Math.round(s.h) }, deviceScaleFactor: scale });
      const imgSrc = new URL(s.src, url).href;
      const cropPage = path.join(src, `_crop-${n}-${k}.html`);  // file:// 이미지는 file:// 페이지에서만 열린다
      fs.writeFileSync(cropPage, `<!doctype html><body style="margin:0;overflow:hidden"><div style="position:relative;width:${s.w}px;height:${s.h}px;overflow:hidden">` +
        `<img src="${imgSrc}" style="position:absolute;width:${s.img.w}px;height:${s.img.h}px;left:${s.img.x - s.x}px;top:${s.img.y - s.y}px"></div></body>`);
      await p2.goto('file://' + cropPage); fs.unlinkSync(cropPage);
      await p2.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
      s.file = `${n}-photo${k}.png`;
      await p2.screenshot({ path: path.join(build, s.file) }); await p2.close();
    }
    cards.push({ card: n, lines: data.lines, shapes: data.shapes });
    const mob = await browser.newPage({ viewport: { width: 360, height: 450 } });
    await mob.goto('file://' + path.join(root, `exports/${n}.png`));
    await mob.addStyleTag({ content: 'body{margin:0}img{width:360px;height:450px;display:block}' }); await mob.waitForTimeout(100); await mob.screenshot({ path: path.join(root, `qa/${n}-mobile.png`) }); await mob.close();
    results.push({ card: n, size: '1080x1350', contentBottom: qa.contentBottom, bottomGap: qa.bottomGap, errors: qa.errors.join('; '), fonts: qa.fonts });
    console.log(`${n}: bottom ${qa.contentBottom} gap ${qa.bottomGap} lines ${data.lines.length} shapes ${data.shapes.length} ${qa.errors.length ? 'ERR ' + qa.errors.join('; ') : ''}`);
  }
  fs.writeFileSync(path.join(root, 'qa/layout-check.json'), JSON.stringify(results, null, 2));
  fs.writeFileSync(path.join(build, 'layers.json'), JSON.stringify(cards, null, 2));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
