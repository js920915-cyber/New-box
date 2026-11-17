# QA — 러닝 듀티팩터 (10장)

- 렌더: Chrome(render.ps1) + Playwright(linux_render.cjs, Windows에서 실행 — render.ps1의 ?qa/?layers가 사진 카드에서 이미지 decode 대기로 끝나지 않아 대체). 1080×1350 10장.
- contentBottom(Playwright 측정): 01 1169 / 02 1226 / 03 1235 / 04 1223 / 05 1224 / 06 1221 / 07 1234 / 08 1243 / 09 1187 / 10 1172 → 모두 y≤1252, bottomGap 73~147px(>200 없음).
- 'unsafe text'(각 장 제목 첫 줄): Noto Sans KR 글꼴 박스 윗변이 y94~95로 측정되는 계측 특성. 실제 글자는 안전 영역 안, 육안 확인.
- 타이포: 표지 88/내부 84/핵심 56/항목 48/본문 44/보조 36/안전 38, 굵기 500·700·750·800·850.
- PPTX: verify_pptx.ps1 PowerPoint PASS (세로 0~1px, 픽셀 차이 1.8~5.6%). Adobe Express 실제 가져오기는 미검수.
- 이미지: AI 생성 8장 육안 검수(손발·관절·로고·글자). 단체 사진 1차본 폐기 후 재생성.
- 원본/모바일: exports 원본과 qa/NN-mobile.png 확인.
- 남은 확인: 센터 러닝 분석 안내 문구(측정 장비) 미포함, 게시 전 담당 전문가 임상 검토.
