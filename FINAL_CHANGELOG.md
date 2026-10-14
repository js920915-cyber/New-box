# V5 변경 기록 — 2026-10-14

- **매 주제 Adobe Express 편집용 PPTX 기본 납품.** 요청 없어도 제작. 폰트·글자 크기·줄바꿈·줄 간격·위치가 PNG와 같아야 함.
- 공용 도구 `tools/cardkit/` 신설(render·extract_layers·build_pptx·verify_pptx·deliver·make_all). 한 줄=한 텍스트 상자, wrap=none, noAutofit, 여백·문단 간격 0, pt=px×0.75, 줄 중심 기준 가운데 정렬. PowerPoint 렌더와 PNG 비교 PASS(세로 ≤2px) 후에만 납품.
- 굵기별 고정 폰트 `templates/fonts/RCardnews-W500~W850.ttf`. 폰트 내부 한국어 이름 "Noto Sans KR"·STAT 제거, 각각 독립 Regular 패밀리로 표기(한국어 Windows·PowerPoint에서 원래 Noto Sans KR로 오인되던 위험 제거). CSS 굵기는 500·650·700·750·800·850만 사용.
- **납품물은 `content/<slug>/delivery/`의 PNG·PPTX·caption.md 3종만.** 연구·QA·사용권 기록은 폴더에 보존하되 납품·나열하지 않음. 최종 보고 간소화.
- 첫 적용·검증: content/strength-training-acsm-2026 (PowerPoint 세로 차이 0~1px, PASS). Adobe Express 내부 실제 가져오기는 미확인.
- 조판 주의 추가: 카드 kind 클래스와 내부 블록 클래스 이름 충돌 금지, Windows PowerShell 5.1용 .ps1은 UTF-8 BOM으로 저장.
# V4 최종 통합 변경 기록 — 2026-10-13

- 전역 타이포 확대 시작값 통일: 표지88/내부84/본문44/보조36px. 역할별 범위와 안전 문장·수치·항목 크기 추가. 사용자 피드백을 구현한 제작 기준이며 새 확대 이미지의 사용자 승인을 뜻하지 않는다.
- 실제 콘텐츠 하단/프레임 아래 여백의 수치 검사, 200px 초과 검토·출고 차단, 예외 기록 추가. 카드2·3만이 아닌 전체 설명·단계·평가·요약에 적용.
- 의미 없는 문장·장식·spacer로 채우거나 폰트를 자동 축소하는 해결 방식 금지. 확대 후 주변 레이아웃 재조판.
- 오래된 제목 축소와 여러 크기 기준을 활성 루트 문서에서 정리. V4 토큰을 단일 기준으로 사용.
- B01·가운데 정렬·사람 표지·임상 정확성·저작권·트레이너 역할·footer 삭제·영상 내부 해설 유지.
- Express는 후속 편집용, 직접 제작 PPTX 우선. PDF 변환 오류와 이미지 레이어 편집 범위·폰트/계정 제약·미검수 상태 보존.
- 과거 결과/레퍼런스/임상 자료는 보존. large-type 초안은 완성본으로 승격하지 않음. 이번 작업은 지침 통합·패키징이며 카드/임상/Express 실검수 작업이 아님.
- 이전 루트 문서와 예전 지침 갱신기는 final-delivery/history-before-v4/에 백업. 폐기된 갱신기가 옛 수치를 복원하지 않도록 중단.
