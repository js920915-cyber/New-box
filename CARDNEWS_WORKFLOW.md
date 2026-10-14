# 제작·검수 워크플로 — V5

버전: 2026-10-14. [AGENTS.md](./AGENTS.md)와 [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)의 전체 카드 기준을 실행한다.

## 1. 시작

주제·대상군·핵심 질문/답·오해·독자 행동을 기록한다. 기본 6장. 수정 요청이면 해당 범위와 소스를 먼저 확인한다. 신규 디자인은 실제 레퍼런스25개(원본10/선택6/실패1/ACL8)와 B01 승인 이미지를 비교한다. 파일 목록 확인을 시각 확인이라고 하지 않는다. 누락·원문 검색·생성·렌더·앱 접근 가능 여부를 기록한다.

## 2. 조사·임상·권리

공식 가이드라인/프로토콜·동료심사 원문 우선. DOI/PMID/제목에서 원문 Methods/Results/Figure까지 확인하고 초록만 확인한 자료를 구분한다. 대상·수치·시점·조건·한계를 기록하고 카드 문장마다 근거ID를 매핑한다. 수술별 회복 차이·상관/인과·약어 의미를 정확히 편집한다.

실제 동작 자료의 관절 각도·기구·지지면·시작/끝 자세와 라이선스를 확인한다. 생성 이미지는 별도 해부학 검수. Askling Diver 오표기, ATRA 조건/랜드마크/단독 진단 오류, 근육·인대 위치 오류, 근거 없는 처방, 무단 소재는 BLOCK. 수정·대체하거나 제한을 보고한다.

## 3. 스토리보드와 조판

카드별 역할·핵심 주장·제목·본문·강조·시각자료·영상·근거·레이아웃을 기록한다. 표지 행동/표정과 후킹을 연결한다. 밈은 임상 시범과 분리한다. 새 주제에 기존 문구/수치를 복사하지 않는다.

design_tokens.json을 적용하고 제목뿐 아니라 본문·보조·안전 문장까지 확대한다. 카드 하나당 독립 아트보드·편집 레이어. B01·가운데 정렬 유지. 과밀하면 문장/줄바꿈/구도를 먼저 정리하고 자동 축소 금지.

일반 설명 contentBottom y1140~1240 목표. 실제 마지막 줄에서 아래 여백을 측정한다. 빈 배경/패딩으로 차 있다고 판단하지 않고 내용·장식·footer를 억지로 추가하지 않는다.

## 4. 영상

rotation_state.json과 실제 수/비율/목적으로 T01~T05를 선택하고 최근 반복을 피한다. 건너뛴 이유를 기록하고 같은 주제 수정은 이력 중복 없이 갱신한다. 영상이 없어도 삽입 틀을 제공한다.

VIDEO_PLAN.md에 장면·길이·구도·비율·좌표·크기를 기록한다. 안내 미리보기, 삽입 안내 문구 없는 배경, 투명 오버레이, placement.json, 소스를 제공한다. 창 안 모든 픽셀 alpha=0, 밖 alpha=255 검사. 실제 영상 자세·측정값·완성 MP4는 별도 검수다.

## 5. 원본·모바일·하단 검사

각 실제 PNG와 360×450 축소본을 연다. contact sheet는 내부 비교용이고 개별 검사를 대신하지 않는다.

| 항목 | 기준 |
|---|---|
| 파일 | 실제 존재, 각각 1080×1350 |
| 글 | 오타·줄바꿈·넘침·잘림·겹침·읽힘 |
| 크기 | V4 역할별 값과 위계, 주요 의미를 보조로 낮추지 않음 |
| 하단 | 실제 contentBottom, bottomGap=1316-contentBottom 기록 |
| 빈 여백 | >200px이면 개선. 예외는 구체적 이유+실물 검토 기록 |
| 안전 | x88~992, y96~1252. 정당한 이미지/제목 예외는 기록 |
| 정렬 | 같은 역할 스타일 일치, 좌우 top≤0.1px+육안 |
| 형태 | B01 유지, 제목→핵심 시각/논점→짧은 해설 |
| 제외 | UI/번호/로고/하단 출처·AI footer/파란 세로선 없음 |

QA_REPORT.md에 카드별 실제 폰트 크기·contentBottom·bottomGap·수정·원본/모바일 확인 여부를 적는다. 자동 검사와 육안 확인은 대체 관계가 아니다. 임상·권리 오류와 이유 없는 큰 하단 공백은 수정 전 출고하지 않는다.

## 6. Express 편집용 PPTX — 매 주제 기본

사용자는 마지막 결과를 Adobe Express에서 추가 편집한다. 요청이 없어도 모든 주제에 PPTX를 만들고, 폰트·크기·줄바꿈·줄 간격·위치를 PNG와 같게 유지한다. 디자인은 Adobe로 새로 만들지 않는다. PDF→PPTX→Express 변환 금지.

[tools/cardkit](./tools/cardkit/README.md)으로 실행한다.

```bash
powershell -ExecutionPolicy Bypass -File tools/cardkit/make_all.ps1 -Topic content/<slug>
```

| 단계 | 도구 | 확인 |
|---|---|---|
| 조판 규칙 | source/build.py | qa.js·layers.js 포함, 글은 h1/p, 굵기 500·650·700·750·800·850만, 카드 kind 클래스와 내부 클래스 이름 분리, 사진은 img(+overflow:hidden 크롭) |
| 렌더 | render.ps1 | PNG 1080×1350, 오류 없음, contentBottom |
| 좌표 | extract_layers.ps1 | 줄 수가 카드 문구 줄 수와 같음, 사진 크롭 실제 픽셀 |
| PPTX | build_pptx.py | 한 줄=한 상자, wrap=none, noAutofit, 여백0, pt=px×0.75, RCardnews W*(latin/ea/cs), 도형·사진. WARN(인라인 SVG) 없음 |
| 검증 | verify_pptx.ps1 | PowerPoint 내보내기 vs PNG: 세로 ≤2px, 픽셀 차이 <8%, wrap/autosize 경고 없음 → qa/pptx-check.json PASS |
| 납품 | deliver.ps1 | PASS일 때만 delivery/ 생성 |

PowerPoint가 없는 환경이면 검증 미실시를 보고하고 PASS라고 하지 않는다. Express 내부 가져오기는 이 검사로 확인되지 않으므로 별도 확인 대상으로 남긴다. 사용자는 templates/fonts의 RCardnews 6개를 Express에 한 번 업로드한다(유료 플랜 기능).

## 7. 납품 계약

```text
content/<topic-slug>/
  delivery/                # ← 사용자에게 주는 것은 이 3종뿐
    01.png ... 06.png
    <topic-slug>.pptx      # Adobe Express 편집용
    caption.md
  research/sources.md      # 이하 작업 기록: 보존하되 납품하지 않음
  research/claims.md
  assets/asset_manifest.md
  storyboard.md
  source/
  exports/  qa/  adobe-express/
  video-template/ VIDEO_PLAN.md   # 영상형일 때
  caption.md
  QA_REPORT.md
```

최종 보고는 짧게: delivery 경로와 3종 파일, 핵심 근거 1~2줄, 미검수 사항(Express 실제 가져오기·게시 전 임상 검토·실제 영상). 연구·QA 문서·콜라주·ZIP·폰트 묶음을 따로 나열하거나 전달하지 않는다.

## 8. 영구 수정

반복 피드백은 문제 카드에만 패치하지 않고 디자인 토큰 → AGENTS → 독립 프롬프트 → 워크플로 검사 → 템플릿/코드 기본값에 반영한다. 활성 문서의 예전 제목 축소·서로 다른 폰트 수치를 정리한다. 과거 제작 스냅샷은 이력으로 보존한다. 최신 기준을 적용하지 않은 이미지를 새 확대 완성본/승인본이라고 부르지 않는다.
