// HTML 원래 좌표에서 PPTX용 레이아웃 추출: 줄별 텍스트·도형·도식 PNG
// 사용: node source/extract_layout.cjs
const path = require('path'), fs = require('fs');
const { pathToFileURL } = require('url');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const root = path.resolve(__dirname, '..');
  const outDir = path.join(root, 'adobe-express', 'build');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(__dirname, 'cards.html')).href);
  await page.evaluate(() => document.fonts.ready);

  const layout = await page.evaluate(() => {
    const px = v => parseFloat(v) || 0;
    const cards = [];
    for (const card of document.querySelectorAll('article.card')) {
      const c = card.getBoundingClientRect();
      const X = r => r.left - c.left, Y = r => r.top - c.top;
      // 텍스트: 블록 요소별로 문자 위치를 모아 줄 단위로 묶는다
      const blocks = card.querySelectorAll('h1,h2,h3,p,.big-num,.tag,.badge,.bar > div,.ticks span,.guide > *');
      const lines = [];
      for (const blk of blocks) {
        const chars = [];
        const w = document.createTreeWalker(blk, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = w.nextNode())) {
          const st = getComputedStyle(n.parentElement);
          for (let i = 0; i < n.textContent.length; i++) {
            const ch = n.textContent[i];
            if (ch === '\n') continue;
            const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
            const rr = r.getClientRects()[0];
            if (!rr) continue;
            chars.push({ ch, x: X(rr), y: Y(rr), r: rr.right - c.left, b: rr.bottom - c.top, h: rr.height,
              size: px(st.fontSize), weight: parseInt(st.fontWeight), color: st.color, ls: px(st.letterSpacing) });
          }
        }
        // 줄 묶기: 같은 블록 안에서 문자 하단(bottom)이 근접하면 같은 줄
        const bLines = [];
        for (const ch of chars) {
          let L = bLines.find(l => ch.y < l.bottom - 4 && ch.b > l.top + 4);
          if (!L) { L = { chars: [], top: ch.y, bottom: ch.b, base: ch.b, maxH: ch.h }; bLines.push(L); }
          L.chars.push(ch); L.top = Math.min(L.top, ch.y); L.bottom = Math.max(L.bottom, ch.b);
        }
        for (const L of bLines) {
          // 줄 앞뒤 공백 제거
          while (L.chars.length && L.chars[0].ch === ' ') L.chars.shift();
          while (L.chars.length && L.chars[L.chars.length - 1].ch === ' ') L.chars.pop();
          if (!L.chars.length) continue;
          const runs = [];
          for (const ch of L.chars) {
            const last = runs[runs.length - 1];
            if (last && last.size === ch.size && last.weight === ch.weight && last.color === ch.color && last.ls === ch.ls) last.text += ch.ch;
            else runs.push({ text: ch.ch, size: ch.size, weight: ch.weight, color: ch.color, ls: ch.ls });
          }
          const big = L.chars.reduce((a, b) => (b.size > a.size ? b : a));
          lines.push({ block: blk.tagName.toLowerCase() + (blk.className ? '.' + blk.className.split(' ')[0] : ''),
            left: Math.min(...L.chars.map(c => c.x)), right: Math.max(...L.chars.map(c => c.r)),
            glyphTop: big.y, glyphBottom: big.b, maxSize: big.size, runs });
        }
      }
      // 도형
      const shapes = [];
      for (const e of card.querySelectorAll('.cover-art,.panel,.callout,.next,.badge,.bar > div,.slot')) {
        const r = e.getBoundingClientRect(), st = getComputedStyle(e);
        shapes.push({ kind: e.classList.contains('badge') ? 'ellipse' : 'roundRect', cls: e.className,
          x: X(r), y: Y(r), w: r.width, h: r.height, radius: px(st.borderTopLeftRadius),
          fill: st.backgroundColor, border: px(st.borderTopWidth) && st.borderTopStyle !== 'none' ? { w: px(st.borderTopWidth), color: st.borderTopColor, dash: st.borderTopStyle === 'dashed' } : null, slot: e.dataset.slot || null });
      }
      for (const e of card.querySelectorAll('.band + .band, .c05 .band + .band')) {
        const r = e.getBoundingClientRect(), st = getComputedStyle(e);
        shapes.push({ kind: 'line', x: X(r), y: Y(r) + px(st.borderTopWidth) / 2, w: r.width, h: 0, stroke: px(st.borderTopWidth), color: st.borderTopColor });
      }
      const pics = [];
      card.querySelectorAll('svg:not(.card-frame)').forEach((s, i) => {
        const r = s.getBoundingClientRect();
        s.setAttribute('data-pic', card.id + '-pic' + (i + 1));
        pics.push({ id: card.id + '-pic' + (i + 1), x: X(r), y: Y(r), w: r.width, h: r.height, label: s.getAttribute('aria-label') });
      });
      cards.push({ id: card.id, lines, shapes, pics });
    }
    return cards;
  });

  // 도식만 투명 PNG(2배)로 저장
  const hi = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 2 });
  await hi.goto(pathToFileURL(path.join(__dirname, 'cards.html')).href);
  await hi.evaluate(() => document.fonts.ready);
  await hi.addStyleTag({ content: 'html,body,.card,.cover-art,.panel{background:transparent !important}' });
  for (const card of layout) {
    for (const [i, p] of card.pics.entries()) {
      const loc = hi.locator(`#${card.id} svg:not(.card-frame)`).nth(i);
      await loc.screenshot({ path: path.join(outDir, p.id + '.png'), omitBackground: true });
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(outDir, 'layout.json'), JSON.stringify(layout, null, 1));
  for (const c of layout) console.log(c.id, 'lines', c.lines.length, 'shapes', c.shapes.length, 'pics', c.pics.length);
})();
