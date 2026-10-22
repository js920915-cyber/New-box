# R스포츠재활센터 브랜드 필름 — FROM SPACE TO MOVEMENT (모션그래픽)

55초 · 1920×1080 · 30fps. Remotion(React) 코드로 그린 모션그래픽 버전이다. 촬영본·AI 생성 영상이 아니라 픽토그램 인물, 지도, 3D 선화, 데이터 그래픽으로 브리프의 8개 장면을 구현했다.

## 장면 구성

| 시간 | 장면 | 구현 |
|---|---|---|
| 0–5s | 1 THE UNIVERSE | 별 필드 전진, 점 지구(Natural Earth), 태양 림 라이트, 도시 간 이동 궤적. 「수많은 움직임이 존재하는 지구.」 |
| 5–10s | 2 DESTINATION SEOUL | 대기권 통과(헤이즈·구름), 한반도 하이라이트, 서울 도시 블록·한강, 마곡 핀. 「대한민국, 서울.」 |
| 10–15s | 3 DISCOVER THE CENTER | 도시 블록이 솟아오르는 3D 비행 → 센터 외관·간판 → 유리문 통과 → 내부(포스플레이트, 모션캡처, 랙, 트레드밀). 「움직임을 위한 전문적인 공간.」 |
| 15–21s | 4 THE QUESTION | 러너·축구선수·일상(계단) 무릎 불편감, 슬로모션과 비트 정지. 「통증이 줄었다고, 회복이 끝난 걸까요?」 |
| 21–31s | 5 ASSESSMENT FIRST | AI 러닝 분석, 휴대용 근력계, 포스플레이트 점프·착지, 3D 움직임 분석, 결과 설명. 「우리는 먼저 평가합니다.」 |
| 31–41s | 6 REHAB & PERFORMANCE | 데이터 → 실제 운동 전환. 고블릿 스쿼트, 싱글 레그 RDL, 허들 홉 착지(슬로모션), 방향 전환. 「평가를 바탕으로, 필요한 과정을 설계합니다.」 |
| 41–49s | 7 BACK TO MOVEMENT | 계단 오르기, 한강 러닝(새벽·남산타워·다리), 축구 방향 전환. 「일상으로. 운동으로. 다시 당신의 움직임으로.」 |
| 49–55s | 8 BRAND REVEAL | 파랑·빨강 궤적이 중앙으로 모임 → R스포츠재활센터 / EVALUATE. REHABILITATE. PERFORM. (2초 이상 유지 후 페이드아웃) |

## 렌더링

```bash
npm i
npm run fonts     # 카드뉴스 글꼴(templates/fonts) 복사 — dev/render 전에도 자동 실행
npm run score     # 임시 음악 public/audio/score.wav 생성 (python3 + numpy + scipy)
npm run render    # out/brand-film.mp4
npx remotion studio   # 미리보기·장면별 타임라인(Scenes 폴더)
```

클라우드/Linux에서는 remotion.config.ts가 미리 설치된 Chromium을 자동으로 사용한다.

## 교체 지점

- **공식 로고**: `public/logo.png`를 넣고 Root.tsx의 BrandFilm `defaultProps`에 `logo: 'logo.png'`를 주면 마지막 장면의 글자 워드마크 대신 로고 이미지가 나온다. 현재 워드마크는 RCardnews 글꼴로 쓴 임시 표기이며 공식 로고가 아니다.
- **음악**: `scripts/score.py`가 코드로 합성한 임시 가이드 트랙(120BPM, D단조, 장면 전환이 박자에 맞음). 라이선스 음원으로 바꾸려면 `public/audio/score.wav`를 교체하거나 `music: false`로 끄고 편집 단계에서 얹는다.
- **센터 외관·내부**: 3장면의 건물·간판·내부 장비는 가상의 선화다. 실제 센터 사진/영상이 있으면 그것을 우선 사용하도록 브리프에 적혀 있으므로, 받으면 해당 구간을 교체한다.
- **브랜드 색**: `src/theme.ts` (카드뉴스 디자인 시스템의 #0879D8 / #CC414A를 어두운 배경용으로 약간 밝힘).

## 정확성 메모

- 인물 동작은 측면 2D 관절 모델(`src/lib/body.ts`, `gaits.ts`, `moves.ts`)로 계산한다. 달리기·걷기 관절 각도는 교과서적 보행 데이터 범위를 근사했고, 접지 발이 미끄러지지 않도록 지면 속도를 계산한다.
- 포스플레이트 그래프는 점프 애니메이션의 엉덩이 궤적에서 F = m(g + a)로 역산한 값이라 화면 동작과 일치한다. 점프 높이 31cm는 체공 0.5초에서 계산한 값이다.
- 화면의 수치(근력 312/268N, LSI 86%, 케이던스 171spm 등)는 연출용 예시이며 실제 회원 데이터나 임상 기준이 아니다.
- 한강 물길·도시 블록은 단순화한 모식도다. 지도 윤곽은 Natural Earth(퍼블릭 도메인, world-atlas 패키지).
