BLUE, HIP, ANK = '#0879d8', '#d5dbe2', '#8d96a0'
STACK_H = 450


def column(label, hip, knee, ank):
    """관절별 일 기여도 누적막대 (위 엉덩이 · 가운데 무릎 · 아래 발목), 높이는 %에 비례"""
    seg = lambda v, name, bg, fg: (f'<div class="seg" style="height:{round(STACK_H * v / 100)}px;background:{bg}">'
                                   f'<p style="color:{fg}">{name} {v}%</p></div>')
    return (f'<div class="scol"><div class="sbar">'
            + seg(hip, '엉덩이', HIP, '#3d434b') + seg(knee, '무릎', BLUE, '#fff') + seg(ank, '발목', ANK, '#fff')
            + f'</div><p class="slab">{label}</p></div>')


def pslot(tag):
    return (f'<div class="pslot"><p class="note">사진 자리</p>'
            f'<div class="tagb"><p>{tag}</p></div></div>')


def ex(name, cond):
    return (f'<div class="trow"><div class="tslot"><p class="note">사진 자리</p></div>'
            f'<div class="ttxt"><p class="item">{name}</p><p class="note">{cond}</p></div></div>')


CARDS = [
    ('kind-cover center', [
        '<h1 class="headline">LSI 90% 넘었으면,<br><span class="accent">무릎도 돌아온 걸까?</span></h1>', gap(44),
        slot(600), gap(40),
        '<p class="key">숫자는 통과해도<br>무릎은 <span class="accent">아직</span>일 수 있어요</p>']),
    ('kind-sum center', [
        '<h1 class="headline">LSI는 <span class="accent">출발점</span>이에요</h1>', gap(52),
        '<div class="box"><p class="item accent">① 근력 LSI를 넘겨도</p>'
        '<p class="body">점프할 때<br>수술한 무릎은 <span class="strong">덜 쓰일 수 있어요</span></p></div>', gap(28),
        '<div class="box"><p class="item accent">② 그래서 움직임을 봐요</p>'
        '<p class="body">무릎이 실제로 일하는지</p></div>', gap(28),
        '<div class="box"><p class="item accent">③ quad를 따로 채워요</p>'
        '<p class="body">무릎이 일하게 만드는 운동으로</p></div>']),
    ('kind-guide center', [
        '<h1 class="headline">Aspetar 가이드라인은<br><span class="accent">숫자 + 움직임</span>을 봐요</h1>', gap(44),
        '<div class="box"><p class="item accent">근력 LSI</p>'
        '<p class="body">달리기 복귀 80% 초과<br>피봇 종목 복귀 100% (등속성 60°/s)</p></div>', gap(20),
        '<div class="box"><p class="item accent">점프할 때 관절의 움직임</p>'
        '<p class="body">엉덩이·무릎·발목의<br>모멘트·각도·일(work)까지<br><span class="strong">정상으로 돌리기</span></p></div>', gap(28),
        '<p class="cite">Kotsifaki R et al., Br J Sports Med 2023</p>']),
    ('kind-graph center', [
        '<h1 class="headline">근력 LSI 94%,<br>점프할 때 무릎 일은<br><span class="accent">반대쪽의 75%</span></h1>', gap(28),
        '<p class="body">싱글 레그 수직점프 · 밀어낼 때 관절별 일 비중</p>', gap(30),
        '<div class="stack">' + column('수술한 쪽', 36, 29, 35) + column('반대쪽', 30, 34, 36)
        + column('부상 없는 사람', 32, 34, 34) + '</div>', gap(26),
        '<p class="cite">Kotsifaki A et al., BJSM 2022 · Fig. 2A 재구성</p>']),
    ('kind-sls center', [
        '<h1 class="headline">싱글 레그 스쿼트,<br>재건한 무릎은 <span class="accent">덜 굽혀요</span></h1>', gap(36),
        '<div class="pair2">' + pslot('A 무릎 굽히고 몸통 세움') + pslot('B 무릎 덜 굽히고 몸통 숙임') + '</div>', gap(32),
        '<div class="list" style="gap:10px">'
        '<p class="body">부상 없는 사람보다<br>knee extensor 모멘트가 <span class="strong">낮았어요</span></p>'
        '<p class="body">몸통을 앞으로 숙이고 옆으로 더 기울였어요</p>'
        '<p class="note">몸통 변화는 햄스트링 이식 그룹 · 사진은 재현 시범</p></div>', gap(12),
        '<p class="cite">Bell et al., Am J Sports Med 2014</p>']),
    ('kind-ex center', [
        '<h1 class="headline">quad에 <span class="accent">부하를 주는</span><br>운동 3가지</h1>', gap(32),
        '<div class="trio">'
        + ex('앉아서 무릎 펴기', '수술 4주~ · 90°→45° 범위<br>앞무릎 통증 보며')
        + ex('뒤꿈치 받친 스쿼트', '몸통은 세우고<br>무릎은 앞으로')
        + ex('스플릿 스쿼트', '지지대 잡고<br>앞무릎이 발끝 쪽으로')
        + '</div>', gap(20),
        '<p class="cite">Aspetar 2023 · Straub & Powers 2024 · ③은 원리 적용 예시</p>']),
    ('kind-lecture center', [
        '<h1 class="headline">보다 더 정확하고<br>객관적으로 배울 수 있는<br><span class="accent">기회!</span></h1>', gap(24),
        '<div class="box"><p class="item accent">사전 웨비나 · Zoom</p>'
        '<p class="body">1차 12/7(월) 21:00 Andreas Bjerregaard<br>2차 12/9(수) 21:00 조인혁</p>'
        '<p class="note">1강좌 1만원 · 2강좌 2만원 · 영어 강의+통역</p></div>', gap(16),
        '<div class="box"><p class="item accent">본 워크숍 2027.02.28 ~ 03.01</p>'
        '<p class="body">Criteria Based ACL Rehab Workshop<br><span class="strong">얼리버드 20% (11/30까지)</span></p>'
        '<p class="note">웨비나 수강료는 워크숍 등록 시 차감해드립니다</p></div>', gap(16),
        '<p class="body strong">신청: 프로필 링크 @rsports_center</p>']),
]
