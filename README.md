# R스포츠재활센터 카드뉴스 — V5 지침

버전: 2026-10-14. 다른 작업 환경으로 옮길 수 있도록 현재 규칙을 통합했다.

| 문서 | 역할 |
|---|---|
| [AGENTS.md](./AGENTS.md) | 에이전트 역할·우선순위·기본 계약 |
| [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) | 확대 타이포·B01·하단 여백·CSS |
| [CARDNEWS_WORKFLOW.md](./CARDNEWS_WORKFLOW.md) | 조사·제작·영상·Express·출고 검사 |
| [CARDNEWS_PROMPT.md](./CARDNEWS_PROMPT.md) | 다른 환경에 복사할 독립 프롬프트 |
| [PROJECT_HANDOFF.md](./PROJECT_HANDOFF.md) | 기존 완성본·미완료 초안·검수 범위 |
| [CLOUD_START.md](./CLOUD_START.md) | 전달·새 환경 시작·실행 환경 |
| [tools/cardkit/README.md](./tools/cardkit/README.md) | PNG·Express용 PPTX·캡션 출고 공용 도구 |
| [FINAL_CHANGELOG.md](./FINAL_CHANGELOG.md) | 이번 통합에서 바뀐 규칙과 범위 |

전체 폰트 확대와 빈 하단 방지를 모든 신규 카드에 적용한다. 매 주제 납품은 `content/<slug>/delivery/`의 PNG·Express 편집용 PPTX·caption.md 3종이다. 수치의 단일 기준은 [design_tokens.json](./templates/design_tokens.json)이다. 기존 content/acl-return-to-running-latest와 content/achilles-elongation-anatomy의 결과는 비교·후속 수정 자료이며 V4 확대 완성본이 아니다. content/acl-return-to-running-large-type은 미완료 초안이다.

문서 전용 ZIP과 실제 레퍼런스·소스를 포함한 전체 ZIP은 final-delivery/에 생성한다. 예전 cloud-delivery/ 압축은 최신 지침과 다를 수 있다. 실제 제작에는 전체 ZIP을 사용하고 폴더의 상대경로를 유지한다.
