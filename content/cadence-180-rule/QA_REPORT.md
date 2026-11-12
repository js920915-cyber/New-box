# QA 보고 — cadence-180-rule (2026-11-12)

## 카드별
| 카드 | 크기 | 실제 폰트 | contentBottom | bottomGap | LO 픽셀차/세로 | 확인 |
|---|---|---|---|---|---|---|
| 01 | 1080x1350 | headline 88px/850, accent 88px/850, body 44px/500 | 1195 | 121 | 4.66% / 1px | 원본·360px 육안 확인 |
| 02 | 1080x1350 | headline 84px/850, accent 84px/850, body 44px/500, note 36px/500 | 1163.4 | 152.6 | 6.71% / 1px | 원본·360px 육안 확인 |
| 03 | 1080x1350 | headline 84px/850, accent 84px/850, note 36px/500, body 44px/500, strong 44px/750 | 1197.8 | 118.2 | 5.25% / 1px | 원본·360px 육안 확인 |
| 04 | 1080x1350 | headline 84px/850, accent 84px/850, item 48px/800, body 44px/500, key 56px/800 | 1122 | 194 | 8.17% / 3px | 원본·360px 육안 확인 |
| 05 | 1080x1350 | headline 84px/850, accent 84px/850, body 44px/500, big 144px/850, note 36px/500, strong 44px/750, safety 38px/700 | 1135.7 | 180.3 | 11.06% / 2px | 원본·360px 육안 확인 |
| 06 | 1080x1350 | headline 84px/850, accent 56px/800, key 56px/800, body 44px/500 | 1224.5 | 91.5 | 8.17% / 2px | 원본·360px 육안 확인 |
| 07 | 1080x1350 | headline 84px/850, accent 84px/850, key 56px/800, body 44px/500, safety 38px/700, warn 38px/700 | 1228.3 | 87.8 | 8.56% / 3px | 원본·360px 육안 확인 |

- 7장 모두 1080×1350, 잘림·겹침·오류 없음(qa.js). bottomGap 88~194px(모두 200 미만). 04는 contentBottom 1122로 목표 1140보다 약간 위지만 큰 항목 4개+결론 구성, 여백 194px로 기준 이내.
- 수정 이력: 05·06·07 하단 여백 367/376/296px → 05 연구 한계 박스, 06 러너 사진, 07 PFP 예외 박스 추가(숫자 맞추기용 장식 아님, 근거 문장). 06 사진이 flex 축소로 눌린 것을 발견 → `.photo{flex:none}` 추가 후 높이 280으로 재조정(다른 장 수치 변화 없음 확인). 2차 검수로 02·04 문구 수정.
- 03 원문 Fig. 1: 크롭 외 수정 없음. 360px에서 그림 속 영문 축 글씨는 작음 → 한국어 축 설명(36px)과 본문으로 보완.
- B01 프레임, 가운데 정렬, 상단 로고·번호·하단 footer 없음.

## PPTX
- build_pptx.py: 7장, 줄 상자 62개, WARN 없음.
- verify_pptx_lo.py: **LO-FAIL (PowerPoint 미검증)**. 경고(줄바꿈·자동 맞춤·장수) 없음, 세로 어긋남 1~3px. 04~07 픽셀 차이 8.2~11.1%는 LibreOffice가 '·', '?', ',', 숫자 주변에 자동 간격을 넣는 특성 때문 — LO 렌더 육안 대조 결과 줄 수·줄바꿈 동일, 넘침 없음. PowerPoint 실검증·Express 실제 가져오기 미실시.
