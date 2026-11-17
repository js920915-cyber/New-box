# QA — 달리기 자세, 무작정 배우지 마세요 (10장)

- 렌더: Playwright(linux_render.cjs, Windows, NODE_PATH=전역 npm). 1080×1350 10장.
- contentBottom: 01 1169 / 02 1153 / 03 1203 / 04 1176 / 05 1155 / 06 1126 / 07 1148 / 08 1176 / 09 1217 / 10 1142 → 모두 y≤1252, bottomGap 99~190px(>200 없음). 04·06·07은 사진 없는 카드라 세로 가운데 정렬.
- 'unsafe text'(제목 첫 줄): 글꼴 박스 윗변 계측 특성(듀티팩터 편과 같음), 육안 확인.
- PPTX: verify_pptx.ps1 PowerPoint PASS (세로 0~1px, 픽셀 차이 1.8~5.2%). Adobe Express 실제 가져오기 미검수.
- 이미지: AI 생성 6장 육안 검수.
- 근거: Chan 2018 원문 전체 정독, research/claims.md. 6~10장은 센터 제안으로 표시(카드 6 상단, 캡션).
- 남은 확인: 게시 전 담당 전문가 임상 검토.
