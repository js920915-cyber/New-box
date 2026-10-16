# QA 보고 — PFP 2탄 재제작 (9장, 2026-10-16)

실행(Linux 클라우드, PowerPoint 없음):
`python3 source/charts.py` → `node source/render_charts.cjs` → `python3 source/build.py` → `node tools/cardkit/linux_render.cjs content/pfp-runners-part2` → `python3 tools/cardkit/build_pptx.py ...` → `python3 tools/cardkit/verify_pptx_lo.py ...`
(Playwright Chromium. `linux_render.cjs`는 render.ps1·extract_layers.ps1과 같은 qa.js·layers.js를 실행)

## 파일
- exports/01~09.png: 9장, 각 1080×1350. qa/01~09-mobile.png(360×450) 확인.
- 원본 9장 모두 1080px로 열어 육안 확인: 텍스트 잘림·겹침 없음, 가운데 정렬, B01 프레임 유지, 상단 로고·번호·하단 footer 없음.

## 타이포 (실제 CSS)
표지 88/850 · 내부 제목 84/850 · 요약 항목 56/800 · 항목 48/800 · 본문 44/500(강조 750) · 보조 36/500 · 안전 38/700 · 사진 자리 안내 36. 굵기는 500·650·700·750·800·850만 사용. 그래프 PNG 안 글자 26~34px(눈금·선 이름, 결론은 본문 문장으로 반복).

## 하단 여백 (qa/layout-check.json, bottomGap = 1316 − contentBottom)
| 카드 | contentBottom | bottomGap | 오류 |
|---|---:|---:|---|
| 01 | 1143.0 | 173.0 | 없음 |
| 02 | 1168.8 | 147.2 | 없음 |
| 03 | 1155.5 | 160.5 | 없음 |
| 04 | 1195.0 | 121.0 | 없음 |
| 05 | 1172.0 | 144.0 | 없음 |
| 06 | 1186.9 | 129.1 | 없음 |
| 07 | 1170.5 | 145.5 | 없음 |
| 08 | 1173.3 | 142.7 | 없음 |
| 09 | 1138.3 | 177.7 | 없음 (목표 1140에 1.7px 미달, 여백 200 미만으로 허용) |

## 수정 이력
1. 03·04 그래프 img가 카드 전체를 크롭 영역으로 잡아 안전 영역 오류 → 그래프를 overflow:hidden 창으로 감쌈.
2. 06 사진 크롭에서 머리가 잘림 → 전신이 들어가게 확대 비율·위치 조정.
3. 09 하단 여백 297px → 요약 항목을 56/800 + 본문 44로 키우고 간격 재배분.
4. 04 “약 4 MPa 아래” → 원문 수치(45°에서 4.2 MPa)에 맞게 “약 4 MPa 이하”.
5. 04 그래프 ‘무릎 펴기’ 이름표가 흐린 스쿼트 선과 겹침 → 아래로 이동.
6. linux_render.cjs: 사진 크롭 PNG가 빈 화면으로 나오던 문제(about:blank에서 file:// 이미지 차단) → 임시 file:// 페이지로 렌더.

## Express PPTX
- adobe-express/pfp-runners-part2-express.pptx: 9장, 줄 상자 75개(한 줄=한 상자, wrap=none, noAutofit, 여백 0, pt=px×0.75, RCardnews W500~W850 latin/ea/cs), 사진·그래프는 보이는 크롭 그대로 이미지, 07 사진 자리와 05 안전 박스는 실제 도형. build_pptx WARN 없음.
- **PowerPoint 검증(verify_pptx.ps1): 미실시** — 이 환경에 PowerPoint 없음. qa/pptx-check.json 없음.
- 대체 검사(LibreOffice, qa/pptx-check-libreoffice.json): 9장 모두 줄 수·줄바꿈·글자 크기·위치 일치, 세로 어긋남 1~3px. 결과 LO-FAIL: 02·09의 픽셀 차이 8.1%/6.8%와 세로 3px. 원인은 LibreOffice가 한글–숫자/라틴/기호 사이에 자동 간격을 넣고(“1 탄”, “앞 ( 무릎”) 세로 보정값(Y_NUDGE)이 PowerPoint 실측 기준이기 때문. 줄 넘침·겹침 없음. 이전 PowerPoint 실측 사례(strength-training-acsm-2026)의 세로 0~1px과 같은 코드 경로.
- **Express 실제 가져오기·폰트 적용: 미확인.**

## 근거·안전·권리
- 근거는 기존 research/sources.md(S1 Powers 2014 원문 확인, S3·S4 초록 수준) 그대로. 이번 재제작에서 문헌을 새로 검색하지 않음. 문장 매핑은 research/claims.md.
- 사진 3장 사용권 확인(CC BY 2.0, CC BY-SA 4.0, CC BY-SA 2.0), 캡션 끝 “사진:” 줄에 저작자 표시. 상세 assets/asset_manifest.md.
- 06 사진은 0~45° 안의 얕은 미니 스쿼트(약 20~30°로 보임)로, 45° 깊이 자체의 시범은 아님 → 문구를 “얕은 범위에서 시작”으로 맞춤.
- 08 사진은 옆모습만이라 “무릎은 둘째 발가락 방향·골반 수평”은 사진으로 보이지 않는 코칭 문구.
- 07은 맞는 사진(앉아서 발목 중량 무릎 펴기)을 찾지 못해 사진 자리로 둠. 게시 전 사용자 사진 삽입 필요.

## 미검수·한계
- PowerPoint 검증, Express 실제 가져오기 미실시.
- 07 사진 자리 미삽입 상태(안내 글자가 PNG에 보임) — 이 상태로 게시하지 않는다.
- 게시 전 임상 판단(운동 각도·코칭 문구)은 담당 전문가 검토 범위.
