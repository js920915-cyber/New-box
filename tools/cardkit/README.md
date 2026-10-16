# cardkit — PNG + Adobe Express 편집용 PPTX 공용 제작 도구

모든 신규 주제는 이 도구로 출고한다. 첫 적용·검증 사례: `content/strength-training-acsm-2026` (PowerPoint 렌더 세로 차이 0~1px).

## 필요 환경 (Windows)

- Google Chrome (`C:/Program Files/Google/Chrome/Application/chrome.exe`) — 렌더·측정·좌표 추출
- Python 3 — 외부 라이브러리 없이 PPTX 작성. 폰트 재생성 때만 `fonttools`
- Microsoft PowerPoint — 검증(verify_pptx.ps1). 없으면 검증 미실시로 보고하고 PASS라고 하지 않는다

## 주제 폴더 규칙

- `source/build.py`가 `source/01.html ...`을 만든다. 각 HTML의 `</body>` 앞에 `tools/cardkit/qa.js`와 `layers.js` 내용을 `<script>`로 넣는다(참고: strength-training-acsm-2026/source/build.py).
- 카드 클래스 이름과 내부 블록 클래스 이름이 겹치지 않게 한다(예: 카드 `kind-steps`, 내부 `.steps`). 겹치면 카드 전체에 margin/gap이 붙어 밀린다.
- 글은 `h1`, `p` 안에 둔다(줄 추출 대상). 굵기는 500·650·700·750·800·850만 쓴다(정적 폰트와 1:1).
- 사진은 `<img>`. 크롭은 `overflow:hidden` 부모로 한다 → 보이는 영역 그대로 PPTX 사진이 된다.
- 연한 박스는 background-color, 구분선은 border-top/bottom → PPTX 실제 도형. B01 프레임은 자동.
- 인라인 SVG 화살표·도식은 자동 변환되지 않는다(build_pptx가 WARN 출력). 필요하면 PNG/SVG 파일을 `<img>`로 넣는다.

## 실행

```bash
powershell -ExecutionPolicy Bypass -File tools/cardkit/make_all.ps1 -Topic content/<slug>
```

단계별: `render.ps1` → `extract_layers.ps1` → `build_pptx.py` → `verify_pptx.ps1` → `deliver.ps1`.

## Linux(클라우드)에서 실행

PowerShell·PowerPoint가 없는 환경용. 같은 qa.js·layers.js·build_pptx.py를 쓴다.

```bash
python3 content/<slug>/source/build.py
node tools/cardkit/linux_render.cjs content/<slug>          # render.ps1 + extract_layers.ps1 (Playwright Chromium)
python3 tools/cardkit/build_pptx.py content/<slug>
python3 tools/cardkit/verify_pptx_lo.py content/<slug>      # LibreOffice 대체 검사 → qa/pptx-check-libreoffice.json
```

verify_pptx_lo.py 결과는 LO-PASS/LO-FAIL이며 PowerPoint PASS가 아니다. LibreOffice는 한글–숫자/라틴 사이에 자동 간격을 넣고 세로 보정값이 PowerPoint 기준이라 픽셀 차이가 약간 크게 나온다. 줄 수·줄바꿈·넘침 확인용으로 쓰고, PowerPoint 검증은 미실시로 보고한다.

## PPTX 설계 (폰트·크기·줄·간격 보존)

| 항목 | 처리 |
|---|---|
| 줄 | 한 줄 = 한 텍스트 상자, wrap=none → Express에서 다시 줄바꿈되지 않음 |
| 크기 | noAutofit, pt = px × 0.75 고정. 슬라이드 1080×1350px(10287000×12858750 EMU) |
| 폰트 | `RCardnews W500/650/700/750/800/850`(templates/fonts). latin·ea·cs 모두 지정, b=0. 한국어 이름 "Noto Sans KR" 제거로 오인 방지 |
| 위치 | 줄 중심 기준 좌우 60px 여유 + 가운데 정렬, 세로 가운데. PowerPoint 기준 세로 보정 0.06×글자크기 |
| 간격 | 문단 앞뒤 0, 줄 간격 100%, 상자 여백 0. 줄 사이 간격은 상자 좌표로 고정 |
| 자간 | CSS letter-spacing → spc(1/100pt) |

## 출고 기준

- `qa/layout-check.json`: 6장 1080×1350, 오류 없음, contentBottom 기준(DESIGN_SYSTEM.md)
- `qa/pptx-check.json`: result PASS (세로 어긋남 ≤2px, 픽셀 차이 <8%, wrap/autosize 경고 없음, 장수 일치)
- `delivery/`: `01~NN.png`, `<slug>.pptx`, `caption.md` 3종만. 연구·QA 기록은 주제 폴더에 남기되 납품하지 않는다

## Adobe Express 쪽 (사용자 1회 설정)

`templates/fonts/RCardnews-W*.ttf` 6개를 Express에 한 번 업로드해 두면 이후 모든 PPTX에 그대로 적용된다(SIL OFL 1.1, 사용자 글꼴 업로드는 유료 플랜 기능). 업로드 전이거나 대체 글꼴이 보이면 해당 상자에 같은 이름 글꼴을 다시 지정한다. Express 내부 가져오기 결과는 이 도구가 검증하지 못한다.

## 폰트 재생성

`python tools/cardkit/make_fonts.py` (fontTools 필요). 원본: templates/fonts/NotoSansKR-VF.ttf.
