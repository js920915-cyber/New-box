# QA 보고 — ACL 「점프 거리가 같으면 무릎도 회복된 걸까?」 (6장, 2026-10-26)

실행(Linux 클라우드, PowerPoint 없음):
`python3 source/build.py` → `node tools/cardkit/linux_render.cjs content/acl-hop-distance-knee-work` → `python3 tools/cardkit/build_pptx.py content/acl-hop-distance-knee-work "점프 거리가 같으면 무릎도 회복된 걸까?"` → `python3 tools/cardkit/verify_pptx_lo.py content/acl-hop-distance-knee-work`

## 파일
- exports/01~06.png: 6장, 각 1080×1350. qa/01~06-mobile.png(360×450) 확인.
- 원본 6장 모두 1080px로 열어 육안 확인: 글 잘림·겹침 없음, 가운데 정렬, B01 프레임 유지, 상단 로고·번호·진행바·하단 출처/AI footer·파란 세로선 없음.
- 레퍼런스 시각 확인: references/user_selected 6장, approved_acl_v3 01~06, approved_frame_b01, avoid, original 일부, 기존 V5 결과(pfp-runners-part2)를 이미지로 열어 비교.

## 타이포 (qa/layout-check.json 실측)
표지 88/850 · 내부 제목 84/850 · 본문 44/500(강조 750) · 표지 보조 48/700 · 04 보조 48/650 · 항목 48/800 · 핵심 56/800~850 · 보조 36/500~700 · 그래프 이름표 40/750 · 그래프 값 52/850 · 표준편차 34/650 · 축 눈금 32/500 · 강사 이름 40/800. 굵기는 500·650·700·750·800·850만.
- 축 눈금(32px)·표준편차(34px)는 그래프 주석으로 보조 36px보다 작게 둠. 핵심 값(평균·LSI)은 52~84px.

## 하단 여백 (bottomGap = 1316 − contentBottom)
| 카드 | contentBottom | bottomGap | 오류 |
|---|---:|---:|---|
| 01 | 1147.7 | 168.3 | 없음 |
| 02 | 1225.8 | 90.2 | 없음 |
| 03 | 1212.8 | 103.2 | 없음 |
| 04 | 1209.3 | 106.7 | 없음 |
| 05 | 1142.5 | 173.5 | 없음 |
| 06 | 1150.2 | 165.8 | 없음 |
6장 모두 목표 y1140~1240 안, 안전 영역(x88~992, y96~1252) 오류 없음.

## 수정 이력
1. 04·05·06 제목이 84px에서 888px 초과(측정 946·1027·1047px) → 문구 유지, 줄바꿈만 변경.
2. 02 축 눈금 ‘100%’ 글 상자 넘침(qa overflow) → 상자 폭·위치 조정.
3. 04 막대–이름표 연결선이 떠 보임 → 연결선 제거, 이름표를 막대 오른쪽에 붙임.
4. 05 ‘일(Work)’이 열 폭에 꽉 참 → 60→56px.
5. 01 contentBottom 1131.7(목표 미달) → 사진 자리 664→680px. 05 1138.5 → 문단 간격 28→32px.

## 근거·수치 검수 (사용자 제공 원문 PDF 2편 직접 확인 — research/sources.md, claims.md)
- 26명(전원 남성, 복귀 승인 후 2주 안 측정), 홉 거리 LSI 97±4%: Table 1·Results ✔
- 도약 시 무릎 일 LSI 69%: Abstract·Discussion ✔ (Table에는 없는 값, 본문 수치)
- 무릎 기여율 9.7±3.9 / 13.5±4.0 / 11.9±4.2: Table 2(수정 반영본) ✔
- 유의 표시: 수술–비수술 p<0.001(d=0.95)만. 수술–대조 p=0.03은 Bonferroni 기준 p<0.017 미충족 → 표시 안 함 ✔
- 수술측 고관절 49.7 · 무릎 9.7 · 발목 40.6 (합 100.0): Table 2 ✔ / 사용자 제공 Figure 3 반올림값(50·10·40)과 일치
- ‘보완’은 고관절만(수술–비수술 고관절 기여 p<0.001). 발목 기여율 차이 없음(p=0.65) → 발목이 보완했다고 쓰지 않음 ✔
- 69%(LSI)와 9.7%(기여율)를 다른 지표로 03장에 명시 ✔
- 재부상 위험 인과 표현 없음. 05장 “재부상 예방이 검증된 기준은 아닙니다”(가이드라인 본문 근거) ✔
- Box 5 Jumping biomechanics 원문(“normalise absolute and symmetry values for moments, angles and work in vertical and horizontal jumps … at hip, knee and ankle”) ✔
- Andreas Bjerregaard: 2023 가이드라인 7번째 저자·GDG 구성원 ✔ / 2022 홉 논문 저자 아님(저자 8명 확인) → 카드·캡션에서 연결하지 않음 ✔
- “전 Aspetar ACL Rehabilitation Team 물리치료사”: 사용자 제공. 원문으로 ‘전(前)’ 여부는 확인 불가.

## 권리
- 외부 사진 미사용. 논문(No commercial re-use)·가이드라인(CC BY-NC) 그림 미사용, 표 수치로 새 그래프.
- 01 표지(한국인 성인 선수 측면 한 발 멀리뛰기)와 06 프로필 2장은 **사진 자리** — 사용권 있는 성인 SLHD 측면 사진을 찾지 못했고, 프로필은 승인본만 사용 지시. 안내 글자가 PNG에 보이므로 **이 상태로 게시하지 않는다.**

## Express PPTX
- adobe-express/acl-hop-distance-knee-work-express.pptx → delivery/acl-hop-distance-knee-work.pptx: 6장, 줄 상자 82개(한 줄=한 상자, wrap=none, noAutofit, 여백 0, pt=px×0.75, RCardnews W500~W850 latin/ea/cs, b=0). build_pptx WARN 없음(인라인 SVG 없음).
- 그래프는 이미지가 아니라 실제 도형(막대·트랙·오차선·캡·괄호·눈금선) + 글 상자(값·이름표·눈금) → Express에서 수치·색 편집 가능. 사진 자리 3개는 도형.
- 구조 대조(스크립트): 6장 모두 PPTX 글 상자 텍스트 = HTML 줄 텍스트(82/82 일치).
- **PowerPoint 검증(verify_pptx.ps1): 미실시** — 이 환경에 PowerPoint 없음. qa/pptx-check.json 없음.
- 대체 검사(LibreOffice, qa/pptx-check-libreoffice.json): LO-FAIL. 03·04·06 통과, 01 세로 5px, 02 픽셀 차 9.8%, 05 8.8%. 나란히 비교 결과 줄 수·줄바꿈·위치는 같고, 차이는 LibreOffice가 한글–숫자/라틴/기호 사이에 자동 간격을 넣는 현상(“26 명”, “Aspetar 는”, “일 (Work)”)과 PowerPoint 기준 세로 보정값(0.06×글자 크기, 88px 표지 제목 ≈5px) 때문. 줄 넘침·겹침 없음. cardkit README에 기록된 LibreOffice 한계와 같음.
- **Express 실제 가져오기·폰트 적용: 미확인.**

## 미검수·한계
- PowerPoint 검증, Express 실제 가져오기 미실시.
- 01·06 사진 자리 미삽입(사용자 사진 필요). 캡션의 강의 일시·장소·신청 방법 자리 미기입.
- 게시 전 임상·학술 표현은 담당 전문가 검토 범위.
