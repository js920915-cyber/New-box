// ?layers 로 열 때만 실행: PPTX용 줄 단위 텍스트(스타일 구간 포함)와 배경 도형/사진 좌표를 JSON으로 기록한다.
if (location.search.includes('layers')) (async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  const card = document.querySelector('.card'), lines = [], shapes = [];
  const rgb = c => '#' + c.match(/\d+/g).slice(0, 3).map(n => (+n).toString(16).padStart(2, '0')).join('');
  for (const block of card.querySelectorAll('h1, p')) {
    let line = null, run = null;
    const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode, cs = getComputedStyle(node.parentElement);
      const style = {size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight), color: rgb(cs.color), spacing: parseFloat(cs.letterSpacing) || 0};
      for (let i = 0; i < node.textContent.length; i++) {
        const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + 1);
        const b = r.getBoundingClientRect();
        if (!b.width && !b.height) continue;
        if (!line || b.left < line.right - 2) {  // 줄 바뀜: 왼쪽으로 되돌아감
          line = {left: b.left, right: b.right, top: b.top, bottom: b.bottom, runs: []}; lines.push(line); run = null;
        }
        if (!run || JSON.stringify(run.style) !== JSON.stringify(style)) { run = {text: '', style}; line.runs.push(run); }
        run.text += node.textContent[i];
        line.left = Math.min(line.left, b.left); line.right = Math.max(line.right, b.right);
        line.top = Math.min(line.top, b.top); line.bottom = Math.max(line.bottom, b.bottom);
      }
    }
  }
  for (const l of lines) { while (l.runs.length && !l.runs.at(-1).text.trim()) l.runs.pop(); const last = l.runs.at(-1); if (last) last.text = last.text.replace(/\s+$/, ''); const first = l.runs[0]; if (first) first.text = first.text.replace(/^\s+/, ''); }
  for (const el of card.querySelectorAll('*')) {
    if (el.closest('.card-frame')) continue;
    const cs = getComputedStyle(el), b = el.getBoundingClientRect();
    if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') shapes.push({type: 'box', x: b.left, y: b.top, w: b.width, h: b.height, fill: rgb(cs.backgroundColor), radius: parseFloat(cs.borderTopLeftRadius) || 0});
    if (parseFloat(cs.borderTopWidth) > 0) shapes.push({type: 'line', x: b.left, y: b.top, w: b.width, h: parseFloat(cs.borderTopWidth), fill: rgb(cs.borderTopColor)});
    if (parseFloat(cs.borderBottomWidth) > 0) shapes.push({type: 'line', x: b.left, y: b.bottom - parseFloat(cs.borderBottomWidth), w: b.width, h: parseFloat(cs.borderBottomWidth), fill: rgb(cs.borderBottomColor)});
    if (el.tagName.toLowerCase() === 'svg') shapes.push({type: 'unsupported', what: 'inline svg', x: b.left, y: b.top, w: b.width, h: b.height});
    if (el.tagName === 'IMG') {  // overflow:hidden 부모가 있으면 그 영역이 보이는 사진(크롭)
      const clip = getComputedStyle(el.parentElement).overflow === 'hidden' ? el.parentElement : el;
      const c = clip.getBoundingClientRect();
      shapes.push({type: 'photo', x: c.left, y: c.top, w: c.width, h: c.height, src: el.getAttribute('src'), alt: el.alt || '사진',
        img: {x: b.left, y: b.top, w: b.width, h: b.height, naturalW: el.naturalWidth, naturalH: el.naturalHeight}});
    }
  }
  const out = document.createElement('pre'); out.id = 'layers-out';
  out.textContent = JSON.stringify({lines: lines.filter(l => l.runs.length), shapes});
  document.body.appendChild(out);
})();
