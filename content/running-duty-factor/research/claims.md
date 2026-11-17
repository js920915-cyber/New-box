# 카드 문장 ↔ 원문 매핑 (러닝 듀티팩터)

원문 PDF: 대표 구글드라이브 "R스포츠재활센터 카드뉴스/2026-11-17_running-duty-factor" 01~09. 대본·토론: r-center-office `talk/2026-11-17-duty-factor-cardnews.md`.
1차 = 정독하며 매핑(2026-11-17, 윤서진 실장 + 고덕현 박사 교차 확인). 2차 = 카드 확정 후 원문 재대조.

| 카드 | 문장 | 근거 · 원문 위치 | 1차 | 2차 |
|---|---|---|---|---|
| 02 | DF = 한쪽 발 한 주기 중 접지 비율 | Lussiana 2019 Introduction / Patoz 2022 Front Methods(DF=tc/(tc+ts)) / Fiers 2025 Methods "Data analysis" | ✔ | ✔ |
| 02 | DF 낮다=공중에 오래, 높다=땅에 오래 | 정의에서 도출 / Lussiana 2019 Table 3(ta·tc) | ✔ | ✔ |
| 03 | 170spm, 접지 0.22초→약 31%, 0.28초→약 40% | 계산: 220×170÷1200=31.2, 280×170÷1200=39.7 (고박사 검산) | ✔ | ✔ |
| 03(캡션) | DF와 (다리 길이 보정) 케이던스 관련성 낮음 | Patoz 2022 Front Table 1 (r≈0.32) | ✔ | ✔ |
| 03(캡션) | 케이던스↑ 연구에서 DF도 함께 오른 경우 많음 | Patoz 2026 리뷰 "Empirical Evidence: Contextualizing Cadence-Related Load Changes" (p.9) | ✔ | ✔ |
| 04 | DF(%) ≈ 접촉시간(ms)×케이던스(spm)÷1200 | 정의(스트라이드 시간=120/케이던스 초) / Nijs 2023 식 1 | ✔ | ✔ |
| 05 | 115명 평균 9·11·13km/h 37.7·34.7·32.6% | Patoz 2022 Front Table 1 | ✔ | ✔ |
| 05 | 빨라질수록 DF 감소 | Patoz 2022 Front Table 1 / Lussiana 2019 Fig.1 | ✔ | ✔ |
| 06 | DF×케이던스 다섯 방향, 경계 없음 | van Oeveren 2021 "The dual-axis framework", Fig.7 (저자 '기대'로 서술) | ✔ | ✔ |
| 07 | 에너지 비용 유의한 차이 없음, 40명, 10~14km/h | Lussiana 2019 Results "EC"(P=0.556), Fig.2, Methods(54명 중 상·하위 20명) | ✔ | ✔ |
| 08 | "덜 위아래로 움직이세요" 지시로 DF↑ | Fiers 2025 Methods "Experimental protocol" | ✔ | ✔ |
| 08 | 낮아진 것: 최대 수직력, 고관절·무릎·발목 관절반력, 무릎·발목 신전 모멘트 / 높아진 것: 고관절 신전·굴곡 모멘트 | Fiers 2025 Results("inverse linear relationship ... except maximal extensor and flexor moments at the hip"), Abstract | ✔ | ✔ |
| 08 | 몸속 힘은 계산값 | Fiers 2025 Methods(Visual3D inverse dynamics), Limitations(대략적 추정) | ✔ | ✔ |
| 09 | DF로 나눈 비교에서 튀는 쪽이 에너지를 덜 쓴다는 결과 없음(2차에서 표현 수정) | Lussiana 2019 Results "EC" | ✔ | ✔ |
| 10 | 수치 변화 ≠ 개선, 통증 시 전문가 평가 | 안전 문장. Patoz 2026 리뷰 결론(증상·내성·기능으로 판단) | ✔ | ✔ |

주의: 카드에는 출처를 넣지 않고 caption.md에 넣는다. Patoz 2026 리뷰는 Fiers 고관절 신전 모멘트를 '감소'로 잘못 요약 — 카드는 원논문(증가)을 따름.

## 2차 검수 (2026-11-17, 카드 렌더 후)
고덕현 박사(Codex)가 exports/01~10.png를 직접 보고 대조. 반영: 02 제목에 '비율' 복원, 03 'DF는 그중 땅에 머무는 비율', 04 '양발', 06 '다리 길이 고려', 08 적용 범위(통증 없는 초보 여성 19명·한 번의 실험)·'최대 회전력', 09 '더 효율적이지 않았다' → '에너지를 덜 쓴다는 결과는 나오지 않았다'. 미반영: 06 두 축 도식 추가(New-box 규칙상 직접 그린 도식 금지 → 텍스트 유지). 숫자(31%·40%·35%·37.7/34.7/32.6%)는 고박사 재확인 일치.
