// ?qa 로 열 때만 실행: contentBottom(실제 마지막 텍스트 줄/이미지), 안전영역, 넘침, 정렬, 폰트 크기를 기록한다.
if (location.search.includes('qa')) (async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  const card = document.querySelector('.card'), errors = [], fonts = {};
  let bottom = 0;
  const walker = document.createTreeWalker(card, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode;
    if (!t.textContent.trim() || t.parentElement.closest('.card-frame')) continue;
    const r = document.createRange(); r.selectNodeContents(t);
    for (const b of r.getClientRects()) {
      bottom = Math.max(bottom, b.bottom);
      if (b.left < 88 || b.right > 992 || b.top < 96 || b.bottom > 1252) errors.push('unsafe text: ' + t.textContent.trim().slice(0, 20));
    }
    const el = t.parentElement, cs = getComputedStyle(el);
    fonts[(el.className || el.tagName) + ''] = cs.fontSize + '/' + cs.fontWeight;
    if (cs.textAlign !== 'center') errors.push('not centered: ' + el.className);
  }
  for (const img of card.querySelectorAll('img')) {
    const clip = getComputedStyle(img.parentElement).overflow === 'hidden' ? img.parentElement : img; const b = clip.getBoundingClientRect(); bottom = Math.max(bottom, b.bottom);
    if (b.left < 88 || b.right > 992 || b.bottom > 1252) errors.push('unsafe img');
  }
  for (const el of card.querySelectorAll('*')) {
    if (el.closest('.card-frame') || el.querySelector(':scope > img')) continue;
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth) errors.push('overflow: ' + el.className);
  }
  const out = document.createElement('pre'); out.id = 'qa-out';
  out.textContent = JSON.stringify({contentBottom: Math.round(bottom * 10) / 10, bottomGap: Math.round((1316 - bottom) * 10) / 10, errors, fonts});
  document.body.appendChild(out);
})();
