# 소재 목록 — ACL 홉 거리 vs 무릎 일 (2026-10-26, 2차)

2차 수정에서 사용자 지시(“글보다는 논문에 나와있는 사진들을 주로 사용”, 03·04 논문 그림, 02 논문 제목, 05 논문 내용)에 따라 논문·가이드라인 원문 그림을 잘라 넣었다. 원문 PDF는 사용자 제공본이며 저장소에 넣지 않았다. 자르기는 `source/paper_figures.py`(원문 PDF 경로를 인자로 실행)로 재현한다. 그림 내용은 바꾸지 않았고, 강조 테두리는 카드 HTML에서 그림 위에 얹은 별도 도형이다(PPTX에서도 따로 지울 수 있음).

| 파일 (assets/paper/) | 카드 | 원문 위치 | 권리 표기(원문) | 처리 |
|---|---|---|---|---|
| k2022-title.png | 02 | Kotsifaki A 2022, 1쪽 제목·저자 | © Author(s) 2021, No commercial re-use | 400dpi 렌더 크롭 |
| k2022-fig3-propulsion.png | 03 | 같은 논문 Figure 3(6쪽) 도약 패널 | 위와 같음 | PDF 내장 원본 그림에서 착지 패널 잘라냄. 무릎 띠에 빨간 테두리 |
| k2022-fig2-propulsion.png | 04 | 같은 논문 Figure 2(5쪽) 위쪽 도약 패널 | 위와 같음 | PDF 내장 원본 그림에서 착지 패널 잘라냄. 무릎 바이올린에 빨간 테두리 |
| g2023-box5-rts.png | 05 | Kotsifaki R 2023, Box 5 Return to sport 머리글(508쪽) | CC BY-NC 4.0 | 400dpi 렌더 크롭 |
| g2023-box5-jumping.png | 05 | 같은 Box 5 Jumping biomechanics 항목 | CC BY-NC 4.0 | 400dpi 렌더 크롭(사이 항목 생략) |
| g2023-header.png | 06 | 같은 가이드라인 1쪽 제목·저자(OPEN ACCESS 로고 제외) | CC BY-NC 4.0 | 400dpi 렌더 크롭. Andreas Bjerregaard에 파란 테두리(pdftotext 글자 좌표) |
| boxes.json | — | 강조 테두리 좌표·그림 크기 | — | paper_figures.py가 생성 |

## 사용권 주의 (게시 전 확인 필요)
- 두 원문 모두 **상업적 재사용 금지**(2022 논문: “No commercial re-use”, 2023 가이드라인: CC BY-NC 4.0). 프로젝트 기본 규칙도 논문 Figure는 CC BY 원문일 때만 허용한다.
- 센터 인스타그램·유료 강의 홍보는 상업적 이용으로 볼 수 있다. 사용자 지시로 넣었으며, 게시 전 BMJ(RightsLink) 이용 허락 또는 저자 측 허락을 받는 것을 권한다. 허락이 어려우면 1차 시안(수치로 다시 그린 그래프, 커밋 596348e)으로 되돌릴 수 있다.
- CC BY-NC 저작자 표시: 캡션 끝 “그림:” 줄 + 카드의 “논문 Figure 2/3”, “Kotsifaki 등 · Br J Sports Med 2022”, “Aspetar ACL 가이드라인” 표기.

## 사진 자리 (사용자 사진 필요)
| 카드 | 위치 | 내용 |
|---|---|---|
| 01 | 888×680 (x96, y360) | 한국인 성인 선수, 한 발 멀리뛰기, 옆에서 전신, 도약 직후 공중 장면(손은 골반 — 연구 프로토콜과 같음) |
| 06 | 272×320 (x96, y741) | Andreas Bjerregaard 승인 프로필 사진 |

## 찾았지만 쓰지 않은 것
- 외부 사진(Openverse): 인도 유소년 트리플 홉 연작(CC BY 3.0, 미성년·다른 검사), Jumping Sideways(CC BY-SA 4.0, 다른 동작), Bronson Xerri(CC0, 실명 프로 선수) → 제외.
- 가이드라인 인포그래픽(Figure 1): ‘점프 역학’ 항목 없음, 카드 크기에서 판독 불가 → 제외.
- 강사 프로필 인터넷 사진: 사용권 불명 → 승인본 대기.

## 기타
- Noto Sans KR VF(templates/fonts), RCardnews W500~W850: SIL OFL 1.1.
- AI 생성 이미지 없음.
