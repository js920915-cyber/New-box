# QA 보고 — ACL 「점프 거리가 같으면 무릎도 회복된 걸까?」 (6장, 2026-10-26 2차)

2차 수정(사용자 지시): 글보다 논문 그림 위주 — 02 논문 제목, 03 Figure 3, 04 Figure 2, 05 가이드라인 Box 5 원문, 06 가이드라인 제목·저자 + Andreas만(조인혁 선생님 제외). 1차 시안은 커밋 596348e.

실행(Linux 클라우드, PowerPoint 없음):
`python3 source/paper_figures.py <Kotsifaki2022.pdf> <Aspetar2023.pdf>` → `python3 source/build.py` → `node tools/cardkit/linux_render.cjs content/acl-hop-distance-knee-work` → `python3 tools/cardkit/build_pptx.py content/acl-hop-distance-knee-work "점프 거리가 같으면 무릎도 회복된 걸까?"` → `python3 tools/cardkit/verify_pptx_lo.py content/acl-hop-distance-knee-work`

## 파일
- exports/01~06.png: 6장, 각 1080×1350. qa/01~06-mobile.png(360×450).
- 원본 6장 모두 1080px로 열어 육안 확인: 글 잘림·겹침 없음, 가운데 정렬, B01 프레임, 상단 로고·번호·하단 footer·파란 세로선 없음. 논문 그림 크롭 경계(위·아래 다른 줄 걸림, 아이콘 잘림) 확인 후 수정.
- 논문 그림 해상도: PDF 내장 원본(Figure 2 1856px, Figure 3 872px 폭) 또는 400dpi 렌더 → 카드 표시 크기 대비 약 2배 이상.

## 타이포 (qa/layout-check.json 실측)
표지 88/850 · 내부 제목 84/850 · 본문 44/500(강조 750) · 보조 48/650~700 · 핵심 수치 64/850 · 그래프 이름표 40/750 · 막대 값 52/850 · 보조 36/500~700 · 표준편차 34/650 · 유의 표시 34/700 · 축 눈금 32/500 · 강사 이름 48/800. 굵기는 500·650·700·750·800·850만.
- 논문 그림 속 영어 글자는 원문 그대로라 카드 글보다 작다(Figure 3 약 18px, Figure 2 이름표 약 14px). 핵심 값은 그림 옆·아래 한국어 글(36~64px)로 반복.

## 하단 여백 (bottomGap = 1316 − contentBottom)
| 카드 | contentBottom | bottomGap | 오류 |
|---|---:|---:|---|
| 01 | 1147.7 | 168.3 | 없음 |
| 02 | 1183.1 | 132.9 | 없음 |
| 03 | 1201.8 | 114.2 | 없음 |
| 04 | 1216.9 | 99.1 | 없음 |
| 05 | 1234.3 | 81.7 | 없음 |
| 06 | 1229.8 | 86.2 | 없음 |
6장 모두 목표 y1140~1240 안, 안전 영역 오류 없음.

## 2차 수정 이력
1. 02 본문 줄 넘침·하단 1290 → 논문 제목 776px로 줄이고 측정 조건은 출처 줄로 합침.
2. 05 하단 여백 253px → Box 5 머리글(Return to sport/completion, 전문 선수 최소 기준) 원문 조각 추가.
3. 05 머리글 조각 위 아이콘 잘림 → “Return to sport” 제목부터 자르고 두 조각 840px로 맞춤. 하단 1244 → 간격 조정 1234.
4. 05 Box 5 항목 조각 위·아래 다른 줄 걸림 → 범위 축소.
5. 06 경력 줄 꺾임·안전 영역 넘침 → 사진 자리 272px, 글 칸 600px. 저자 글씨를 키우려 OPEN ACCESS 로고 제외.

## 근거·수치 (사용자 제공 원문 PDF 2편 — research/sources.md, claims.md)
- 26명(전원 남성, 복귀 승인 후 2주 안 측정), 홉 거리 LSI 97±4%, 도약 시 무릎 일 LSI 69% ✔
- 03 그림 옆 9.7±3.9 / 13.5±4.0 / 11.9±4.2 = Table 2(수정 반영본). 그림 속 10/14/12%는 반올림임을 카드에 표기 ✔
- 유의 표시: 수술측–비수술측 p<0.001만. 수술측–대조군 p=0.03(보정 기준 p<0.017 미충족) 표시 안 함 ✔
- 04 “이 연구에서 도약 일의 약 88%는 고관절·발목, 무릎 약 12%” = Discussion 문장 ✔ (Figure 2 *·†는 캡션에서 설명)
- 05 Box 5 원문(“normalise absolute and symmetry values for moments, angles and work …”)과 한국어 요약 일치 ✔. 두 조각 사이 항목은 생략(머리글 + 해당 항목만).
- 06 Andreas Bjerregaard 7번째 저자(pdftotext 글자 좌표로 테두리 위치 확인) ✔ / 2022 논문 저자 아님 → 연결하지 않음 ✔ / 조인혁 선생님 카드·캡션에서 삭제 ✔
- 재부상 위험 인과 표현 없음 ✔

## 권리 — 게시 전 확인 필요
- **논문 그림 사용은 사용자 지시에 따른 것이며, 두 원문 모두 상업적 재사용 금지**(2022: “No commercial re-use”, 2023: CC BY-NC 4.0). 프로젝트 규칙(AGENTS.md: 논문 Figure는 CC BY만, BY-NC 불가)과 다르다. 센터 홍보·유료 강의 안내는 상업적 이용으로 볼 수 있어 BMJ 이용 허락(RightsLink) 또는 저자 측 허락을 권한다. 출처는 카드(“논문 Figure 2/3”, “Kotsifaki 등 · Br J Sports Med 2022”, “Aspetar ACL 가이드라인”)와 캡션 “그림:” 줄에 표기.
- 01 표지·06 프로필은 **사진 자리**(안내 글자가 PNG에 보임) — 사진 삽입 전 게시 금지.

## Express PPTX
- delivery/acl-hop-distance-knee-work.pptx: 6장, 줄 상자 57개(한 줄=한 상자, wrap=none, noAutofit, 여백 0, pt=px×0.75, RCardnews W500~W850 latin/ea/cs, b=0). 논문 그림 6개는 보이는 크롭 그대로 사진, 강조 테두리·LSI 막대·사진 자리·연한 바탕은 실제 도형. build_pptx WARN 없음.
- 구조 대조: 6장 모두 PPTX 글 상자 텍스트 = HTML 줄 텍스트(57/57).
- **PowerPoint 검증: 미실시**(PowerPoint 없음). qa/pptx-check.json 없음.
- LibreOffice 대체 검사: LO-FAIL — 02·06 통과, 01 세로 5px, 03·05 픽셀 차 8.04%, 04 세로 3px. 나란히 비교 결과 그림 위치·테두리·줄 수·줄바꿈 같음. 차이는 LibreOffice의 한글–숫자/라틴/기호 자동 간격과 PowerPoint 기준 세로 보정값(cardkit README 기록된 한계).
- **Express 실제 가져오기: 미확인.**

## 미검수·한계
- PowerPoint 검증, Express 실제 가져오기 미실시.
- 01·06 사진 자리 미삽입, 캡션 강의 일시·장소·신청 방법 미기입.
- 논문 그림 상업적 이용 허락 미확인.
- 게시 전 임상·학술 표현은 담당 전문가 검토 범위.
