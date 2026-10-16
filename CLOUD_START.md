# 다른 환경에서 시작하기 — V5.1

## 전달할 묶음

- 마크다운 전용 ZIP: 지침 확인·복사·편집용. 실제 레퍼런스/이미지/소스는 포함되지 않으므로 이것만으로 기존 디자인을 시각 확인했다고 할 수 없다.
- 전체 프로젝트 ZIP: 루트 V4 지침, 실제 references/, templates/, content/, 소스·폰트·라이선스·기존 결과·편집 파일 포함. 재현/후속 작업에는 이 묶음을 사용한다.

ZIP을 해제하거나 GitHub 저장소(js920915-cyber/New-box)를 받아 그 폴더를 프로젝트 루트로 삼는다. 다른 도구는 기본으로 **main 브랜치**를 받으므로, 지침 변경은 main에 합쳐져야 모든 플랫폼에 똑같이 적용된다(작업 브랜치에만 있는 규칙은 다른 플랫폼이 모른다). Markdown/이미지/소스의 상대 경로를 유지한다.

## 시작 메시지는 붙이지 않아도 된다 (자동 적용)

프로젝트 루트를 연 작업 도구는 지침을 스스로 읽는다. 주제만 말하면 된다.

| 도구 | 자동으로 읽는 파일 |
|---|---|
| Claude Code (데스크톱·CLI·웹) | CLAUDE.md → `@AGENTS.md` 불러옴 |
| Codex, Cursor, GitHub Copilot 등 | AGENTS.md |

AGENTS.md 맨 앞의 "시작 시 자동 절차"에 아래 첫 메시지 내용이 모두 들어 있다. 규칙은 AGENTS.md 한 곳만 고친다.

예외: 폴더를 열지 않는 채팅형 환경(claude.ai 일반 채팅, ChatGPT 등)은 파일을 자동으로 읽지 못한다. 그때만 프로젝트 지침(Project instructions) 칸에 아래 문장을 **한 번** 넣어 두면 매번 붙일 필요가 없다. 더 자세한 규칙이 필요하면 CARDNEWS_PROMPT.md의 블록 전체를 넣는다. 단, 그 환경에서는 tools/cardkit을 실행할 수 없으면 PPTX 검증을 하지 못한다.

## (예외용) 첫 메시지 / 프로젝트 지침 문장

```text
이 폴더는 R스포츠재활센터 카드뉴스 프로젝트다. 루트 AGENTS.md, DESIGN_SYSTEM.md, CARDNEWS_WORKFLOW.md, CARDNEWS_PROMPT.md, PROJECT_HANDOFF.md, tools/cardkit/README.md를 읽고 V5 지침을 적용해라. B01 프레임·가운데 정렬·기존 코드 디자인을 유지하고 Adobe 템플릿으로 대체하지 마라. 표지88/내부84/본문44/보조36px 시작값과 일반 설명 콘텐츠 하단 y1140~1240, 과도한 하단 여백 검수를 전체 카드에 적용해라. 기존 결과는 V4 확대 전 비교 자료이며 large-type은 미완료 초안이다. 실제 영상과 Express 가져오기 검수를 완료한 것으로 가정하지 마라. 시각자료는 직접 그린 그림 대신 사용권이 확인된 사진(내 사진 → CC0/CC BY/CC BY-SA 등)을 쓰고, 못 구하면 사진 자리로 비워 이유를 알려라. 요청 범위에 맞춰 작업하고 신규 주제면 근거 조사부터 진행해, tools/cardkit로 content/<slug>/delivery/에 PNG·Adobe Express 편집용 PPTX(폰트·크기·줄바꿈·간격 보존, PowerPoint 검증 PASS, PowerPoint가 없으면 미검증으로 보고)·caption.md 3종만 납품하고, 3종 전부를 대화창에서 내려받을 수 있는 첨부 파일로 보내라.
```

## 실행 환경

V5 출고 도구(tools/cardkit)는 Windows + Google Chrome + Python 3 + Microsoft PowerPoint(검증용)를 쓴다. 폰트 재생성 때만 fontTools가 필요하다. 클라우드·Linux(Claude Code 웹 등)는 Node.js + Playwright Chromium + Python 3(Pillow) + LibreOffice로 `linux_render.cjs` → `build_pptx.py` → `verify_pptx_lo.py`를 실행하고, PowerPoint 검증은 미실시로 보고한다(2026-10-16 pfp-runners-part2에서 실행 확인). 아래는 이전 ACL 코드에 대한 기록이다.


Python·Node.js·Playwright·Sharp와 Chromium/Chrome을 확인한다. 기존 source/render.cjs 등은 Windows 런타임과 Chrome 절대경로가 있으므로 새 환경 경로/일반 모듈 import로 수정해야 한다. 런타임·설치 라이브러리·브라우저는 압축에 포함하지 않는다. 클라우드 실행 성공을 검증한 패키지는 아니다.

ACL 기존 코드의 cards.json→build.py→render.cjs 재생성 경로를 참고하되 build.py가 예전 수치를 다시 쓰므로 먼저 V4 토큰을 반영한다. 다른 주제도 해당 생성기·CSS의 하드코딩을 먼저 수정한다. 원본을 보존하고 새 주제/수정 폴더에서 렌더·시각·임상 검수를 수행한다.

전체 패키지 재생성: `python tools/package_final.py`. 과거 tools/update_handoff_docs.py는 폐기된 이전 수치 복원 도구이며 실행해도 지침을 변경하지 않도록 중단 처리했다. 예전 cloud-delivery ZIP은 V4 최종본이 아니다.
