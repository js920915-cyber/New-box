# STEP 6 — Higgsfield 장면별 생성 설정 (첫 5초 + 다음 기준 이미지)

## 공통 설정 (2026-11-10 Higgsfield 계정에서 확인)

| 항목 | 값 | 비고 |
|---|---|---|
| 영상 모델 | **Seedance 2.5** (`seedance_2_5`), mode `omni_reference`, `start_image` = 기준 프레임 | 시작·끝 프레임을 모두 고정하려면 FLUX 3 Video(`start_image`+`end_image`)를 보조로 비교 |
| 길이 | 5초 생성 → 편집에서 0.75~2초만 사용 | 앞뒤 0.5초는 모핑이 생기기 쉬워 버린다 |
| 해상도 | 먼저 **draft(480p) 15 크레딧** → 동작이 맞으면 같은 job을 1080p로 finalize | 바로 1080p 5초는 **80 크레딧**. 잔액 613 크레딧 |
| 오디오 | `generate_audio: false` | 사운드는 Premiere에서 실제 효과음으로 |
| 비율 | 16:9 생성 → 9:16은 Premiere 리프레임 | 피사체를 화면 중앙 1/3 안에 둔 기준 프레임을 쓴다 |
| 이미지 모델 | 원본 사진 + 조명 참고 이미지 → `nano_banana_2_1` 2k (장당 약 2 크레딧) | 해부·글자 정확도 우선. 조명만 더 필요하면 `gpt_image_2_6` 2k high로 재조명 |

> 아래 SHOT별 프롬프트의 조명 문구(차콜 배경, 어두운 톤)는 1차 시안 기준이다. 실제 생성에는 "룩 결정" 규칙을 따른 문구(`Documentary footage … Sony FX3 … Lighting, colors and textures stay exactly as in the start frame`)를 쓴다. 2026-11-10 초안 테스트에 쓴 프롬프트가 이 형식이다.

공통 네거티브 문구(모든 프롬프트 끝에 붙인다):
```
No added or changed text, numbers or logos. No extra fingers or hands. No limb or joint deformation. Equipment keeps its exact shape throughout. No morphing of faces. No camera shake. No sudden lighting changes. No slow-motion artifacts. No sparkles, lens flares or CGI effects.
```

## 룩 결정 (2026-11-10 원장님 피드백 반영)

1차 시안(어두운 차콜 톤)은 **"너무 어둡다", "AI 그래픽 티가 난다"**는 피드백으로 폐기했다. 제작은 AI 중심을 유지하고, 아래 규칙으로 AI 티를 줄인다.

### AI 티 줄이기 규칙
1. **밝은 실제 센터 톤.** 흰 벽·흰 천장 조명을 유지한다. 대비는 어둡게 눌러서가 아니라 빛의 방향(측면 창광 느낌)으로 만든다.
2. **광고 단어 금지.** 프롬프트에 cinematic, dramatic, moody, epic, film still을 쓰지 않는다. 대신 실제 촬영 조건을 쓴다: `documentary footage, Sony FX3, 35/50mm, f/2–2.8, ISO 1250, 1/50s`.
3. **질감 보존 지시.** `keep real skin pores, hair, glove/fabric creases, natural sensor noise, slightly uneven real-world light`, `no skin smoothing, no HDR, no glow, no over-sharpening`.
4. **최소 수정.** 원본 사진을 한 번만 수정한다. AI 결과를 다시 AI로 돌리는 횟수를 줄여야 플라스틱 질감이 쌓이지 않는다.
5. **영상 움직임은 작게.** 관절 각도 변화는 10~20° 이내, 카메라는 `slight natural handheld micro-movement`. 큰 동작은 실제 영상을 움직임 참고(`video_references`)로 넣는다.
6. **후반 통일.** 모든 AI 컷과 실제 컷에 같은 그레인(35mm, 강도 낮게), 180° 셔터 모션블러, 약한 비네팅을 입혀 질감을 하나로 맞춘다.
7. **사용 길이.** AI 컷은 컷당 0.75~2초. 손·얼굴 클로즈업이 2초를 넘으면 흐름이 보이기 시작한다.

## 기준 이미지 (채택본, Higgsfield 생성 기록에 저장됨)

| 컷 | 채택 job ID (GPT Image 2.6, 2k high) | 원본 | 남은 수정 |
|---|---|---|---|
| A 무릎 수기 평가 | `4500ef86-7fb3-40f9-ac55-b6604de3d315` | 사진 14 (media `30a9f104…`) | 가슴 로고가 "R소포츠재활센터"로 틀림 → 원본 로고 크롭으로 덮기(트래킹). 명찰 비움 ✔ |
| B Keiser 데이터 | `1598f1ca-f14b-4e4b-9988-9505688fc3a5` | 사진 59 (media `1c010593…`) | 화면 라벨 일부 틀림 → 원본 화면으로 코너 핀 교체(원래 계획) |
| C 스텝 지도 | `61698b50-1e75-4fb9-9c87-4d7f14a42b1f` | 사진 15 (media `6ff89acb…`) | 전체가 약간 회색 → 노출 +0.3 |

움직임 참고용 실제 영상: V4 포스플레이트 SL-CMJ → Higgsfield media `b0219938-cbf7-4a3a-918f-f261e06b9e75`(1080×1920, 59.94fps H.264 변환본).

폐기한 시안(참고): 어두운 1차 `c5161c0e…`, `1370c020…`, `faef68ec…` / 밝은 2차 `9c1fdfd2…`, `25ed460c…`, `92ad4db6…`.

---

## SHOT A — 무릎 수기 평가 (00:00.00–00:01.50)

- 참조 파일: `start_image` = job `c5161c0e…`(ref A). 원본 사진 14는 손 위치 대조용.
- 참조 이미지 역할: 첫 프레임 고정(구도·손 위치·조명).
- 생성 길이: 5초 / 사용: 1.5초(약 1.0–2.5초 구간).
- 카메라: ECU 측면, 85mm 느낌, 아주 느린 푸시인.
- 조명: 카메라 왼쪽 측면 키, 무릎 윤곽 림, 배경 차콜.
- 인물 행동: 치료사가 무릎 위·아래를 잡은 채 무릎을 약 10~15° 천천히 펴 내렸다 다시 굽힘. 손가락이 피부 위에서 살짝 압을 바꾼다. 회원은 정지, 호흡만.
- 장비: 없음.

```
Cinematic close-up continuing exactly from the start frame. A Korean physical therapist in white nitrile gloves keeps one hand on the distal thigh just above the knee and the other hand cupping the upper calf just below the knee. Over five seconds he slowly and smoothly extends the patient's flexed knee by about 10 to 15 degrees and then gently returns it, a controlled passive range-of-motion examination. The fingers subtly adjust pressure on the skin; the hands never leave their positions. The patient lies still, only natural breathing. Camera: locked side angle with a very slow push-in of about five percent, 85mm lens look, shallow depth of field on the gloved hands and knee. Lighting stays constant: soft directional key from camera-left, rim light on the knee contour, deep charcoal background, warm amber skin highlights, subtle film grain. Realistic skin texture and leg hair, anatomically correct knee and hand movement.
No added or changed text, numbers or logos. No extra fingers or hands. No limb or joint deformation. No morphing of faces. No camera shake. No sudden lighting changes. No sparkles, lens flares or CGI effects.
```

- 생성 후 검수: 손가락 5개 유지 / 손이 무릎에서 미끄러지지 않는가 / 무릎이 과신전·이상 굴곡 없이 움직이는가 / 슬개골 위치가 자연스러운가 / 가슴 로고가 흐르지 않는가(흐르면 해당 구간을 디포커스) / 명찰 빈칸 유지.
- Premiere 연결: 0프레임 블랙 4f → 컷 인. 1.2s부터 다음 컷 B1의 UI 틱을 J컷으로 미리 깔아준다.

## SHOT B1 — Keiser 출력 데이터 확인 (00:01.50–00:02.25)

- 참조 파일: `start_image` = job `1370c020…`(ref B). 화면 합성용 원본 = 사진 59.
- 참조 이미지 역할: 첫 프레임 고정. **화면 내용은 AI 결과를 쓰지 않는다.**
- 생성 길이: 5초 / 사용: 0.75초.
- 카메라: OTS, 무릎(전경)→화면 랙 포커스.
- 인물 행동: 치료사 검지가 화면의 Power 링 근처로 다가가 멈춤. 회원 무릎은 정지.
- 장비 동작: 기계 정지(동작 중 프레임 변형 방지).

```
Cinematic over-the-shoulder shot continuing exactly from the start frame. The athlete sits still on the black Keiser pneumatic leg-extension machine; the machine does not move. The physical therapist's index finger moves slowly toward the upper part of the vertical display and stops just in front of it, as if explaining the result. Focus pulls smoothly from the athlete's knee in the foreground to the display and fingertip. The display content stays frozen and unchanged for the whole shot. Dim room, cool glow from the screen on the fingertip and knees, warm amber glint on the brass air cylinder, deep charcoal rubber floor with white speckles, subtle film grain.
No added or changed text, numbers or logos. No extra fingers or hands. Equipment keeps its exact shape throughout. No camera shake. No sudden lighting changes. No sparkles, lens flares or CGI effects.
```

- 생성 후 검수: 레그 익스텐션 프레임·실린더·패드 모양 유지 / 손가락 수 / 화면 테두리가 직사각형 유지(코너 핀 추적 가능해야 함).
- Premiere 연결: **화면을 사진 59의 실제 디스플레이로 교체** — 원본 사진에서 화면만 크롭 → Corner Pin(또는 After Effects Mocha 트래킹) → 밝기 +10%, 약한 글로우. 실제 수치(526 W, 4.89 rad/s, 13 kg per side, Set 01, Reps L10/R09)만 보이게 하고 새 숫자를 만들지 않는다. B2와 하드컷.

## SHOT B2 — 포스플레이트 단일하지 점프 (00:02.25–00:03.00) — **AI 생성 없음**

- 소스: 실제 영상 V4 `V20260703_170745000…MOV`, 0.95–1.70s 구간.
- 처리: 60fps → 24fps 타임라인에서 50% 속도(Optical Flow 불필요, 프레임 블렌딩 끔). 착지 프레임(≈1.30s)을 음악 비트에 맞춤.
- 화면 배치(택1): ① 16:9 전체에 세로 영상을 확대 크롭(무릎~플레이트) ② **B1과 좌우 2분할**(왼쪽 Keiser 화면, 오른쪽 점프) — 인수인계의 Split Screen 원칙과 맞고 세로 원본 손실이 적어 권장.
- 색보정: 배경 창문 반전 글자 영역을 -1.5 stop 비네팅으로 눌러 읽히지 않게. 차콜/스틸 블루 LUT 공통 적용.
- Motion Echo(선택): 1.00–1.30s 체공 구간에서 4프레임 간격 잔상 3장, 불투명도 60/40/20%. 데이터처럼 보이는 선·숫자는 넣지 않는다.

## SHOT C — 스텝 운동 지도 (00:03.00–00:05.00)

- 참조 파일: `start_image` = job `faef68ec…`(ref C). 원본 사진 15는 손·발 위치 대조용.
- 생성 길이: 5초 / 사용: 2.0초.
- 카메라: 미디엄, 왼쪽→오른쪽 느린 슬라이드(약 10cm 느낌), 35mm.
- 인물 행동: 회원이 스텝 위 앞발에 체중을 실으며 천천히 스텝업(무릎이 두 번째 발가락 방향으로 정렬). 치료사는 한 손을 대퇴 원위부 앞, 한 손을 정강이에 둔 채 무릎이 안쪽으로 무너지지 않게 가볍게 안내하고 회원 얼굴을 올려다보며 짧게 말한다.

```
Cinematic medium shot continuing exactly from the start frame. A young Korean man in a black t-shirt slowly performs a controlled step-up onto the black aerobic step platform with the front foot, shifting his weight forward while his knee stays aligned over the second toe. A Korean physical therapist in a white polo kneels beside him, keeping one hand on the front of the distal thigh and the other hand on the shin, gently guiding knee alignment without pulling; he looks up and gives a brief verbal cue, the athlete nods once. Realistic, unhurried rehabilitation pace, anatomically correct hip, knee and ankle movement, both feet stay in contact with the step and turf as in the start frame. Camera: slow lateral slide from left to right, 35mm lens look, shallow depth of field on the hands and knee. Lighting constant: directional key from camera-right, rim light on the therapist's shoulder and the athlete's leg, darker background, desaturated equipment colors, warm amber skin highlights, subtle film grain.
No added or changed text, numbers or logos. No extra fingers or hands. No limb or joint deformation. Equipment keeps its exact shape throughout. No morphing of faces. No camera shake. No sudden lighting changes. No sparkles, lens flares or CGI effects.
```

- 생성 후 검수: 무릎 외반(knee valgus)이나 비현실적 관절 각도 없음 / 치료사 손이 당기거나 들어 올리지 않음 / 스텝 박스 형태 유지 / 회원 얼굴 동일인 유지 / 등 로고 흐름(흐르면 디포커스).
- Premiere 연결: 3.80s부터 실제 로고 워드마크 페이드 인. 5.00s 음악 첫 드롭에 맞춰 다음 블록(EVALUATE)으로 하드컷.

---

## 다음 기준 이미지 (STEP 2 목록) — 원본 매칭과 방향

같은 2단계 방식(원본 사진 + 조명 참고)을 쓴다. 장면에 사람이 없는 원본은 **사람을 AI로 새로 넣어야 하므로** 생성 인물임을 기록하고 실제 회원으로 오인되지 않게 한다.

| 순서 | 장면 | 원본 | 사람 | 메모 |
|---|---|---|---|---|
| 1 | Keiser 출력 데이터 + 재활운동 | 사진 59 ✅ / 사진 61 | 실제 | 61은 Functional Trainer 미는 동작. 화면 234 W·3.59는 실제값 |
| 2 | 스텝 운동 지도 | 사진 15 ✅ | 실제 | — |
| 3 | 러닝 분석 | 사진 73 + 사진 6 | **AI 인물 추가 필요** | 모니터 속 경기 영상은 저작권 문제로 실제 분석 화면 녹화로 교체 |
| 4 | 무릎 재활 | 사진 14, 영상 V4 | 실제 | 나머지 영상 5개 확보 후 매치컷 지점 선정 |
| 5 | 어깨 재활 | 사진 61 | 실제(얼굴 잘림) | 어깨 재활 맥락이 맞는지 확인 필요 |
| 6 | 발목 재활 | **원본 없음** | — | 촬영 또는 기존 영상 5개 중 확인 |
| 7 | 척추 재활 | **원본 없음** | — | 촬영 필요 |
| 8 | 재평가 | 영상 V4(같은 검사 반복) | 실제 | 전후 수치는 실제 기록이 있을 때만 |
| 9 | 센터 와이드 | 사진 67, 80, 78 | 없음/소수 | 78(접수·로고)은 엔딩용 대칭 돌리인 |

### 추가로 필요한 실제 자료(우선순위)
1. 영상 V1·V2·V3·V5·V6 (10MB 이하로 압축 또는 분할) — 매치컷·Motion Echo 원본.
2. **실제 로고 원본 파일**(AI·PNG·SVG) — 오프닝 워드마크·엔딩.
3. Keiser 화면 **화면 녹화 또는 정면 사진**(숫자가 바뀌는 2~3초면 충분) — B1 합성 품질이 크게 오른다.
4. 포스플레이트 리포트 화면(V4 회원의 실제 결과) — 데이터 오버레이용. 없으면 데이터 그래픽을 생략한다.
5. 발목·척추 재활 장면 사진 또는 영상 각 1개 이상.
6. 출연 치료사·회원의 초상 사용 동의 여부.
