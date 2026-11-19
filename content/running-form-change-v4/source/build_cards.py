def bar(v, mx, w, color):
    if v == 0:
        return f'<div class="bline"><p class="bnum" style="color:{color}">0</p></div>'
    px = round(v / mx * w)
    return f'<div class="bline"><div class="bar" style="width:{px}px;background:{color}"></div><p class="bnum" style="color:{color}">{v}</p></div>'

BLUE, GRAY = '#0879d8', '#9aa3ad'

def item(label, a, b, mx, w):
    return (f'<div class="brow"><p class="blab">{label}</p>' + bar(a, mx, w, BLUE) + bar(b, mx, w, GRAY) + '</div>')

LEGEND = ('<div class="legend"><p class="note"><span style="color:#0879d8">■</span> 연습한 그룹</p>'
          '<p class="note"><span style="color:#9aa3ad">■</span> 비교 그룹</p></div>')

CARDS = [
    ('kind-cover center', [
        '<h1 class="headline">러닝 자세 교정,<br>받으면 <span class="accent">무조건 좋을까?</span></h1>', gap(44),
        slot(620), gap(40),
        '<p class="key">효과는 있어요<br>그런데 <span class="accent">이면</span>이 있어요</p>']),
    ('kind-effect center', [
        '<h1 class="headline"><span class="accent">부드럽게 착지</span>하는<br>연습만 했는데</h1>', gap(36),
        '<p class="body">1년 동안 다친 사람이 더 적었어요</p>', gap(48),
        '<div class="bars" style="gap:30px">'
        '<div class="brow"><p class="blab">연습한 그룹 <span class="note">화면 보며 부드럽게</span></p>' + bar(16, 38, 700, BLUE).replace('class="bar"', 'class="bar bar80"', 1).replace('>16<', '>16%<') + '</div>'
        '<div class="brow"><p class="blab">비교 그룹 <span class="note">화면 없이 달리기</span></p>' + bar(38, 38, 700, GRAY).replace('class="bar"', 'class="bar bar80"', 1).replace('>38<', '>38%<') + '</div></div>', gap(44),
        '<p class="note">두 그룹 모두 2주 동안 트레드밀 8번<br>끝까지 추적한 초보 러너 320명 기준</p>', gap(10),
        '<p class="cite">Chan et al., Am J Sports Med 2018</p>']),
    ('kind-flip center', [
        '<h1 class="headline">그런데<br><span class="warn">종아리·아킬레스</span>는</h1>', gap(28), LEGEND, gap(20),
        '<div class="bars">' + item('무릎 앞쪽 통증', 4, 18, 23, 640) + item('족저근막염(발바닥)', 2, 23, 23, 640)
        + item('아킬레스건염', 5, 0, 23, 640) + item('종아리 근육 손상', 5, 0, 23, 640) + '</div>', gap(20),
        '<p class="note">보고 건수 · 부위별 통계 비교는 하지 않았어요</p>']),
    ('kind-why center', [
        '<h1 class="headline">왜 그랬을까?</h1>', gap(36),
        '<div class="box"><p class="item accent">연구진의 해석</p>'
        '<p class="body">착지 방식이 바뀌면서<br>발목을 아래로 미는 종아리 근육<br>부담이 커졌을 수 있어요</p>'
        '<p class="note">실제 착지 변화는 재지 않았어요</p></div>', gap(20),
        '<div class="box"><p class="item accent">다른 연구들에서도</p>'
        '<p class="body">뒤꿈치 → 발 앞·중간 착지로 바로 바꾸면<br><span class="strong">무릎 앞 부담은 낮고</span><br><span class="strong warn">발목을 미는 힘은 컸어요</span></p>'
        '<p class="note">근거는 아직 제한적이에요</p></div>', gap(20),
        '<p class="cite">Chan et al. 2018 · Anderson et al., Sports Med 2020</p>']),
    ('kind-so center', [
        '<h1 class="headline">착지를 바꾸면<br>부담이 가는 곳이<br><span class="accent">달라질 수 있어요</span></h1>', gap(48),
        '<p class="item">그래서 자세는 천천히 바꾸고</p>', gap(16),
        '<p class="body">바꾼 뒤 새로 일하게 된 곳이<br>버티는지 보며 양을 늘려요</p>', gap(40),
        '<div class="box"><p class="body">예) 발 앞쪽으로 디디게 됐다면<br><span class="strong">종아리·아킬레스</span>를 살피기</p></div>', gap(40),
        '<p class="note">리뷰 연구진도 몸이 감당할 수 있는지 보며<br>서서히 바꿔야 한다고 봤어요 (Anderson 2020)</p>']),
    ('kind-center center', [
        '<h1 class="headline">좋은 자세 교정에는<br><span class="accent">순서</span>가 있어요</h1>', gap(36),
        slot(300), gap(32),
        '<div class="list" style="gap:12px"><p class="chk">① 러닝 경력·거리 인터뷰</p>'
        '<p class="chk">② 신체 평가</p><p class="chk">③ 천천히 교정</p></div>', gap(32),
        '<div class="box"><p class="safety">통증이 있거나 부상이 반복된다면<br>자세보다 <span class="warn">원인 평가</span>가 먼저예요</p></div>', gap(24),
        '<p class="note">자세 바꿔 보려는 러닝 친구에게 보내 주세요</p>']),
]
