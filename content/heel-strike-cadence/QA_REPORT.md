# QA 보고 — heel-strike-cadence (2026-11-11)

## 카드별
| 카드 | 크기 | 실제 폰트 | contentBottom | bottomGap | LO 픽셀차/세로 | 확인 |
|---|---|---|---|---|---|---|
| 01 | 1080x1350 | headline 88px/850, accent 88px/850, body 44px/500 | 1195 | 121 | 5.14% / 0px | 원본·360px 육안 확인 |
| 02 | 1080x1350 | headline 84px/850, accent 84px/850, body 44px/500, strong 44px/750 | 1170 | 146 | 5.41% / 2px | 원본·360px 육안 확인 |
| 03 | 1080x1350 | headline 84px/850, accent 84px/850, body 44px/500, strong 44px/750, note 36px/500 | 1171.9 | 144.1 | 6.57% / 1px | 원본·360px 육안 확인 |
| 04 | 1080x1350 | headline 84px/850, accent 84px/850, note 36px/500, body 44px/500, strong 44px/750 | 1197.8 | 118.2 | 6.58% / 1px | 원본·360px 육안 확인 |
| 05 | 1080x1350 | headline 84px/850, accent 84px/850, item 48px/800, body 44px/500, safety 38px/700 | 1186.5 | 129.5 | 9.69% / 2px | 원본·360px 육안 확인 |
| 06 | 1080x1350 | headline 84px/850, accent 84px/850, key 56px/800, body 44px/500, safety 38px/700, warn 38px/700 | 1136.8 | 179.2 | 11.46% / 3px | 원본·360px 육안 확인 |

- 모든 카드 contentBottom y1137~1198(목표 1140~1240 근처, 06은 1137이지만 bottomGap 179<200). 잘림·겹침·오류 없음(qa.js).
- 수정 이력: 02 하단 여백 246→146(사진 440→540), 05 202→130(핵심 설명을 보조 36px→본문 44px로 상향), 04 "가장 편한 값"→"가장 효율적인 값"(원문 energetically optimal), 범례 설명 "연구·조건 하나의 평균", 05 "달라집니다"→"달라질 수 있습니다"(2차 검수).
- B01 프레임, 가운데 정렬, 상단 로고·번호·하단 footer 없음 확인.
- 04 원문 Fig. 1: 크롭 외 수정 없음. 360px에서 그림 속 영문 축 글자는 작아 읽기 어려움 → 그림 아래 한국어 축 설명(36px)과 본문 문장으로 보완.

## PPTX
- tools/cardkit build_pptx.py: 6장, 줄 상자 50개, WARN 없음.
- verify_pptx_lo.py: **LO-FAIL (PowerPoint 미검증)**. 경고(줄바꿈·자동 맞춤·장수) 없음, 세로 어긋남 0~3px. 05·06 픽셀 차이 9.7%·11.5%는 LibreOffice가 '·', '?', ',' 앞뒤에 자동 간격을 넣는 특성 때문이며 LO 렌더를 육안 대조한 결과 줄 수·줄바꿈 동일, 넘침 없음. PowerPoint 실검증과 Adobe Express 실제 가져오기는 미실시.
