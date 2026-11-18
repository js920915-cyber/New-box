def pair(l, r):
    def ph(src, x, label, mark=''):
        m = f'<p class="mark">{mark}</p>' if mark else ''
        return (f'<div class="ph"><img src="../assets/photos/{src}" alt="" style="height:620px;left:{x}px;top:0">{m}'
                f'<div class="tagb"><p>{label}</p></div></div>')
    return f'<div class="pair2">{ph(*l)}{ph(*r)}</div>'

def drake(rows):
    out = ''
    for src, mk, txt, col in rows:
        out += (f'<div class="drow"><div class="dimg"><img src="../assets/photos/{src}" alt="" style="width:436px;left:0;top:0"></div>'
                f'<div class="dtxt"><p class="dmark" style="color:{col}">{mk}</p><p class="item">{txt}</p></div></div>')
    return f'<div class="drake">{out}</div>'

def bar(v, mx, w, color):
    if v == 0:
        return f'<div class="bline"><p class="bnum" style="color:{color}">0</p></div>'
    px = round(v / mx * w)
    return f'<div class="bline"><div class="bar" style="width:{px}px;background:{color}"></div><p class="bnum" style="color:{color}">{v}</p></div>'

BLUE, GRAY, RED = '#0879d8', '#9aa3ad', '#cc414a'

def item(label, a, b, mx, w, unit='', hot=False):
    ca = BLUE
    return (f'<div class="brow"><p class="blab">{label}</p>'
            + bar(a, mx, w, ca).replace(f'>{a}<', f'>{a}{unit}<')
            + bar(b, mx, w, GRAY).replace(f'>{b}<', f'>{b}{unit}<') + '</div>')

LEGEND = ('<div class="legend"><p class="note"><span style="color:#0879d8">■</span> 재훈련 그룹</p>'
          '<p class="note"><span style="color:#9aa3ad">■</span> 비교 그룹</p></div>')

CARDS = [
    ('kind-cover center', [
        '<h1 class="headline">러닝 자세를<br>바꿨더니 <span class="accent">생긴 일</span></h1>', gap(44),
        pair(('m_knee_ok.jpg', -266, '무릎: 우린 덜 다쳤대'), ('m_calf_pain.jpg', -494, '종아리: …우린 더?')), gap(40),
        '<p class="key">초보 러너 <span class="accent">1년 추적 연구</span></p>']),
    ('kind-who', [
        '<h1 class="headline">누가 참가했을까?</h1>', gap(36),
        '<div class="list" style="gap:10px"><p class="chk">✔ 달리기 시작한 지 <span class="accent">2년 미만</span></p>'
        '<p class="chk">✔ 최근 6개월 동안 <span class="accent">부상 없음</span></p>'
        '<p class="chk">✔ 착지할 때 힘이 <span class="accent">‘확’</span> 실리는 사람</p></div>', gap(36),
        '<div class="box"><p class="item accent">수직 평균 부하율 (VALR)</p>'
        '<p class="body">발이 땅에 닿은 직후, 위로 받는 힘이<br>얼마나 <span class="strong">빠르게</span> 커지는지 나타내요.<br>같은 몸무게라도 ‘확’ 커지는 사람,<br>‘천천히’ 커지는 사람이 있어요.</p>'
        '<p class="body">이 연구는 평소 속도에서<br><span class="strong accent">VALR 70 BW/s 이상</span>인 사람만 참가</p></div>', gap(24),
        '<p class="note">실험실 힘 측정 트레드밀로 쟀어요. 워치의 접지 시간이나<br>상하 움직임만으로는 해당 여부를 알 수 없어요.<br>부상 위험 기준이 아니라 이 연구의 참가 조건이에요.</p>', gap(16),
        '<p class="cite">Chan et al., Am J Sports Med 2018</p>']),
    ('kind-how center', [
        '<h1 class="headline">어떻게 실험했을까?</h1>', gap(32),
        '<p class="body">참가자 390명을 <span class="strong">무작위로</span> 두 그룹으로</p>', gap(32),
        '<div class="box"><p class="item accent">재훈련 그룹</p>'
        '<p class="body">화면에 뜬 착지 충격 그래프를 보며<br><span class="strong">“더 부드럽게 착지하세요”</span><br>2주 동안 8번 · 15분 → 30분</p>'
        '<p class="body strong accent">특정 자세는 가르치지 않았어요</p></div>', gap(20),
        '<div class="box" style="background:#f3f4f6"><p class="item">비교 그룹</p><p class="body">같은 시간, 트레드밀에서 그냥 달리기</p></div>', gap(32),
        '<p class="key">↓</p><p class="body">그 뒤 <span class="strong">1년 동안</span> 누가 다치는지 지켜봤어요</p>']),
    ('kind-res1 center', [
        '<h1 class="headline">충격은 줄었고,<br>다친 사람도 <span class="accent">적었어요</span></h1>', gap(36),
        '<p class="body">재훈련 그룹은 착지 충격<br>(VALR·VILR)이 크게 줄었어요</p>', gap(48),
        '<p class="item">1년 동안 부상을 겪은 비율</p>', gap(28),
        '<div class="bars" style="gap:30px">'
        '<div class="brow"><p class="blab">재훈련 그룹</p>' + bar(16, 38, 700, BLUE).replace('class="bar"','class="bar bar80"',1).replace('>16<', '>16%<') + '</div>'
        '<div class="brow"><p class="blab">비교 그룹</p>' + bar(38, 38, 700, GRAY).replace('class="bar"','class="bar bar80"',1).replace('>38<', '>38%<') + '</div></div>', gap(40),
        '<p class="note">끝까지 추적한 320명 기준</p>']),
    ('kind-res2 center', [
        '<h1 class="headline">그런데<br>부위별로 보면</h1>', gap(28), LEGEND, gap(20),
        '<div class="bars">' + item('무릎 앞쪽 통증', 4, 18, 23, 640) + item('족저근막염(발바닥)', 2, 23, 23, 640)
        + item('<span class="warn">아킬레스건염</span>', 5, 0, 23, 640, hot=True)
        + item('<span class="warn">종아리 근육 손상</span>', 5, 0, 23, 640, hot=True) + '</div>', gap(24),
        '<p class="note">보고된 부상 건수 · 부위별로는 통계 비교를 하지 않았어요</p>']),
    ('kind-why', [
        '<h1 class="headline">착지 방식에 따라<br>부담이 <span class="accent">달라질까?</span></h1>', gap(24),
        '<div class="box"><p class="item accent">이 연구진의 해석</p>'
        '<p class="body">부드럽게 착지하려고 착지 방식을<br>바꾸면서 종아리 근육 부담이<br>커졌을 가능성</p>'
        '<p class="note">실제 착지 변화는 측정하지 않았어요</p></div>', gap(16),
        '<div class="box"><p class="item accent">다른 연구를 모은 리뷰</p>'
        '<p class="body">뒤꿈치 → 앞·중간발 착지로 바로 바꾸면</p>'
        '<p class="body"><span class="strong">무릎 앞 관절의 누적 부담은 낮고</span><br><span class="strong warn">발목을 아래로 미는 회전력은 큰</span> 경향</p>'
        '<p class="note">근거 수준: 제한적</p></div>', gap(20),
        '<p class="cite">Chan et al. 2018 · Anderson et al., Sports Med 2020</p>']),
    ('kind-shift', [
        '<h1 class="headline">한쪽 부담이 줄면<br><span class="warn">다른 쪽 부담</span>이<br>커질 수 있어요</h1>', gap(40),
drake([('m_no.jpg', '✕', '영상 속 자세<br>바로 따라 하기', '#cc414a'), ('m_yes.jpg', '○', '내 몸이<br>준비됐는지<br>먼저 확인하기', '#0879d8')]), gap(36),
        '<p class="note">리뷰 연구진은 근육과 힘줄이 부하를 얼마나<br>감당할 수 있는지 고려하며, 착지 방식은<br>서서히 바꿀 필요가 있다고 봤어요 (Anderson 2020)</p>']),
    ('kind-check center', [
        '<p class="note">센터의 제안</p>', gap(16),
        '<h1 class="headline">바꾸기 전<br><span class="accent">확인할 것</span></h1>', gap(36),
        '<div class="box" style="gap:22px">'
        '<div class="pair"><p class="item accent">① 왜 바꾸나요?</p><p class="body">목적, 무엇으로 좋아졌다고 판단할지</p></div>'
        '<div class="pair"><p class="item accent">② 지금 얼마나 달리나요?</p><p class="body">주간 거리·경력·최근 늘린 양·속도·신발</p></div>'
        '<div class="pair"><p class="item accent">③ 늘어날 부담을 받을 몸인가요?</p><p class="body">부상 이력, 종아리 등 근력</p></div>'
        '<div class="pair"><p class="item accent">④ 한 번에 하나, 천천히</p><p class="body">통증·피로 반응을 보며</p></div></div>']),
    ('kind-sum center', [
        '<h1 class="headline">자세는 <span class="accent">신중하게</span>,<br>내 몸에 맞게</h1>', gap(40),
        '<p class="item">이 연구를 그대로 내게<br>적용하면 안 되는 이유</p>', gap(20),
        '<div class="list" style="gap:8px"><p class="body">초보·착지 충격이 큰 러너만 참가</p>'
        '<p class="body">실험실 트레드밀에서 훈련</p><p class="body">실제 착지 변화는 측정하지 않음</p></div>', gap(64),
        '<div class="box"><p class="safety">통증이 있거나 부상이 반복된다면<br>자세보다 <span class="warn">원인 평가</span>가 먼저예요</p></div>']),
]
