# 소스

- cards.html / cards.css — 6장 독립 article.card, B01 인라인, Noto Sans KR VF(OFL)
- render.cjs — `node source/render.cjs` : exports/01~06.png, video-template/05-video-background.png, qa/layout-check.json(contentBottom·bottomGap·안전영역·겹침)
- post.py — `python3 source/post.py` : qa/*-mobile.png(360×450), 05 영상 오버레이 생성·alpha 검사, placement.json
Playwright는 전역(/opt/node-tools/node_modules/playwright) 또는 NODE_PATH로 로드.
