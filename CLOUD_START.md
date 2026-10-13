# 다른 환경에서 시작하기 — V4

## 전달할 묶음

- 마크다운 전용 ZIP: 지침 확인·복사·편집용. 실제 레퍼런스/이미지/소스는 포함되지 않으므로 이것만으로 기존 디자인을 시각 확인했다고 할 수 없다.
- 전체 프로젝트 ZIP: 루트 V4 지침, 실제 references/, templates/, content/, 소스·폰트·라이선스·기존 결과·편집 파일 포함. 재현/후속 작업에는 이 묶음을 사용한다.

ZIP을 해제하고 내부 R-Sports-Cardnews/를 프로젝트 루트로 삼는다. 압축 해제 미지원 환경이면 로컬에서 해제한 폴더를 전달한다. Markdown/이미지/소스의 상대 경로를 유지한다. AGENTS.md 자동 적용을 가정하지 말고 직접 읽게 한다.

## 새 에이전트에 보낼 첫 메시지

```text
이 폴더는 R스포츠재활센터 카드뉴스 프로젝트다. 루트 AGENTS.md, DESIGN_SYSTEM.md, CARDNEWS_WORKFLOW.md, CARDNEWS_PROMPT.md, PROJECT_HANDOFF.md를 읽고 V4 지침을 적용해라. B01 프레임·가운데 정렬·기존 코드 디자인을 유지하고 Adobe 템플릿으로 대체하지 마라. 표지88/내부84/본문44/보조36px 시작값과 일반 설명 콘텐츠 하단 y1140~1240, 과도한 하단 여백 검수를 전체 카드에 적용해라. 기존 결과는 V4 확대 전 비교 자료이며 large-type은 미완료 초안이다. 실제 영상과 Express 가져오기 검수를 완료한 것으로 가정하지 마라. 요청 범위에 맞춰 작업하고 신규 주제면 근거 조사부터 개별PNG까지 진행해라.
```

## 실행 환경

Python·Node.js·Playwright·Sharp와 Chromium/Chrome을 확인한다. 기존 source/render.cjs 등은 Windows 런타임과 Chrome 절대경로가 있으므로 새 환경 경로/일반 모듈 import로 수정해야 한다. 런타임·설치 라이브러리·브라우저는 압축에 포함하지 않는다. 클라우드 실행 성공을 검증한 패키지는 아니다.

ACL 기존 코드의 cards.json→build.py→render.cjs 재생성 경로를 참고하되 build.py가 예전 수치를 다시 쓰므로 먼저 V4 토큰을 반영한다. 다른 주제도 해당 생성기·CSS의 하드코딩을 먼저 수정한다. 원본을 보존하고 새 주제/수정 폴더에서 렌더·시각·임상 검수를 수행한다.

전체 패키지 재생성: `python tools/package_final.py`. 과거 tools/update_handoff_docs.py는 폐기된 이전 수치 복원 도구이며 실행해도 지침을 변경하지 않도록 중단 처리했다. 예전 cloud-delivery ZIP은 V4 최종본이 아니다.
