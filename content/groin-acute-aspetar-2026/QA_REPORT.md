# QA 보고 — 급성 서혜부 손상, 아스페타 방식 (8장, 2026-11-05)

실행(Linux 클라우드, PowerPoint 없음):
`python3 content/groin-acute-aspetar-2026/source/build.py` → `node tools/cardkit/linux_render.cjs content/groin-acute-aspetar-2026` → `python3 tools/cardkit/build_pptx.py content/groin-acute-aspetar-2026` → `python3 tools/cardkit/verify_pptx_lo.py content/groin-acute-aspetar-2026`

## 파일
- exports/01~08.png: 8장, 각 1080×1350. 8장 모두 1080px 원본을 열어 육안 확인: 텍스트 잘림·겹침 없음, 가운데 정렬, B01 프레임 유지, 상단 로고·번호·하단 footer·파란 세로선 없음.
- qa/01~08-mobile.png(360×450): 8장을 1:1 크기로 나란히 놓고 확인. 제목·본문 판독 가능, 회색 보조(36–38px)는 작지만 판독 가능.

## 타이포 (실제 렌더 값)
36px/500, 36px/700, 38px/500, 38px/700, 44px/500, 44px/750, 46px/800, 52px/800, 84px/850, 88px/850. 굵기는 500·650·700·750·800·850만 사용.

## 하단 여백·LibreOffice 대체 검사
| 카드 | contentBottom | bottomGap | 레이아웃 오류 | LO 세로 어긋남 / 픽셀 차이 |
|---|---:|---:|---|---|
| 01 | 1183 | 133 | 없음 | 1px / 5.24% |
| 02 | 1175 | 141 | 없음 | 2px / 7.59% |
| 03 | 1232.5 | 83.5 | 없음 | 2px / 10.12% |
| 04 | 1196 | 120 | 없음 | 2px / 7.57% |
| 05 | 1229.7 | 86.3 | 없음 | 2px / 6.78% |
| 06 | 1232.2 | 83.8 | 없음 | 1px / 9.31% |
| 07 | 1149 | 167 | 없음 | 2px / 5.87% |
| 08 | 1144.5 | 171.5 | 없음 | 2px / 7.69% |

- 모든 장 contentBottom이 안전 영역(y≤1252) 안, bottomGap 200px 미만.
- PPTX: 한 줄 = 한 상자, wrap=none·noAutofit 경고 없음, 줄 상자 수 = 렌더 줄 수.
- LibreOffice 결과: LO-FAIL. 8%를 넘은 장은 LibreOffice가 한글과 영문·숫자·가운뎃점 사이에 자동 간격을 넣어 생긴 차이로, 렌더 이미지를 열어 줄 수·줄바꿈·위치가 같음을 확인함. **PowerPoint 검증은 미실시**(환경에 PowerPoint 없음). Adobe Express 실제 가져오기도 미확인.

## 수정 이력
1. 03 과밀(하단 1337, 안전 영역 초과) → 단계 간격 22→16px, 하단 문장 2줄→1줄.
2. 02·07 하단 여백 247·237px → 문단·박스 간격 재배분.
3. 06 사진에서 킥하는 다리가 잘림 → 크롭 위치·배율 조정해 전신과 공이 보이게 함.
4. 04·07 줄 끝에 "·"가 걸리는 줄바꿈 → 문장 구조 변경.
5. 2차 근거 검수로 표현 수정(research/claims.md 하단 기록): 02 제목·본문, 03 단계 설명, 07 "운동 중".
