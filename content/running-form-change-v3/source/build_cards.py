def pair(l, r):
    def ph(src, x, label, mark=''):
        m = f'<p class="mark">{mark}</p>' if mark else ''
        return (f'<div class="ph"><img src="../assets/photos/{src}" alt="" style="height:620px;left:{x}px;top:0">{m}'
                + (f'<div class="tagb"><p>{label}</p></div>' if label else '') + '</div>')
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
        '<h1 class="headline">착지를 다르게 하니까<br>부상을 <span class="accent">덜 당해?</span></h1>', gap(44),
        pair(('m_knee_ok.jpg', -266, ''), ('m_calf_pain.jpg', -494, '')), gap(40),
        '<p class="key">초보 러너의 착지 재훈련,<br><span class="accent">1년 추적 연구</span></p>']),
    ('kind-answer center', [
        '<h1 class="headline">결론부터 말하면</h1>', gap(40),
        '<div class="box"><p class="key">덜 다쳤어요</p>'
        '<p class="body">1년 동안 부상을 보고한 비율<br><span class="strong">재훈련 16%</span> · 비교 38%</p></div>', gap(20),
        '<div class="box" style="background:#f3f4f6"><p class="key">그런데 <span class="warn">종아리·아킬레스</span>는</p>'
        '<p class="body">재훈련 그룹에서만 보고됐어요<br><span class="strong">각 5건</span> · 비교 그룹 0건</p></div>', gap(40),
        '<p class="item">착지를 바꿀 거라면<br><span class="accent">종아리 보강부터, 천천히</span></p>', gap(28),
        '<p class="note">달리기 2년 미만 · 착지 충격이 큰<br>초보 러너가 참가한 연구예요</p>']),
    ('kind-who', [
        '<h1 class="headline">누가 참가했을까?</h1>', gap(24),
        '<div class="list" style="gap:8px"><p class="chk">✔ 달리기 시작한 지 2년 미만</p>'
        '<p class="chk">✔ 최근 6개월 동안 부상 없음</p>'
        '<p class="chk">✔ 착지 충격의 기울기가 큰 사람</p></div>', gap(28),
        '<div class="box" style="padding:26px 30px 20px;gap:8px"><p class="item accent">수직 평균 부하율 (VALR)</p>'
        '<p class="body">발이 땅에 닿은 직후, 위로 받는 힘이<br>얼마나 <span class="strong">빠르게</span> 커지는지 나타내요</p>'
        '<div class="photo" style="width:790px;height:409px;border-radius:0;background:transparent"><img src="../assets/photos/valr_graph.png" alt="수직 지면반력 그래프와 VALR 기울기" style="width:790px;left:0;top:0"></div></div>', gap(20),
        '<p class="note">워치로는 알 수 없어요 · 이 연구의 참가 조건이에요</p>', gap(10),
        '<p class="cite">Chan et al., Am J Sports Med 2018 · 그래프는 이해를 돕는 예시</p>']),
    ('kind-how center', [
        '<h1 class="headline">어떻게 진행했을까?</h1>', gap(32),
        '<p class="body">참가자 390명을 <span class="strong">무작위로</span> 두 그룹으로</p>', gap(32),
        '<div class="box"><p class="item accent">재훈련 그룹</p>'
        '<p class="body">화면에 뜬 착지 충격 그래프를 보며<br><span class="strong">“더 부드럽게 착지하세요”</span><br>2주 동안 8번 · 15분 → 30분</p>'
        '<p class="body strong">자세는 따로 가르치지 않았어요</p></div>', gap(20),
        '<div class="box" style="background:#f3f4f6"><p class="item">비교 그룹</p><p class="body">같은 시간, 트레드밀에서 그냥 달리기</p></div>', gap(32),
        '<p class="key">↓</p><p class="body">그 뒤 <span class="strong">1년 동안</span> 누가 다치는지 지켜봤어요</p>']),
    ('kind-res1 center', [
        '<h1 class="headline">1년 동안<br><span class="accent">덜 다쳤어요</span></h1>', gap(36),
        '<p class="body">2주 재훈련 직후, 착지할 때 힘이 커지는<br>속도(VALR·VILR)가 낮아졌고,</p>', gap(40),
        '<p class="item">1년 동안 부상을 보고한 비율도<br>더 낮았어요</p>', gap(28),
        '<div class="bars" style="gap:30px">'
        '<div class="brow"><p class="blab">재훈련 그룹</p>' + bar(16, 38, 700, BLUE).replace('class="bar"','class="bar bar80"',1).replace('>16<', '>16%<') + '</div>'
        '<div class="brow"><p class="blab">비교 그룹</p>' + bar(38, 38, 700, GRAY).replace('class="bar"','class="bar bar80"',1).replace('>38<', '>38%<') + '</div></div>', gap(40),
        '<p class="note">이 연구에 참여한 초보 러너 · 끝까지 추적한 320명 기준</p>']),
    ('kind-res2 center', [
        '<h1 class="headline">그런데<br><span class="warn">다친 부위</span>를 보면</h1>', gap(28), LEGEND, gap(20),
        '<div class="bars">' + item('무릎 앞쪽 통증', 4, 18, 23, 640) + item('족저근막염(발바닥)', 2, 23, 23, 640)
        + item('아킬레스건염', 5, 0, 23, 640, hot=True)
        + item('종아리 근육 손상', 5, 0, 23, 640, hot=True) + '</div>', gap(24),
        '<p class="note">그룹별 보고 건수 · 부위별 통계 비교는 하지 않았어요</p>']),
    ('kind-why', [
        '<h1 class="headline">왜 다친 곳이<br><span class="accent">달랐을까?</span></h1>', gap(24),
        '<div class="box"><p class="item">연구진의 생각</p>'
        '<p class="body">착지 방식이 바뀌면서 종아리 부담이<br>커졌을 수 있다고 봤어요</p>'
        '<p class="note">다만 실제로 착지가 어떻게 바뀌었는지는<br>재지 않았어요</p></div>', gap(16),
        '<div class="box"><p class="item">다른 연구들을 모아 보면</p>'
        '<p class="body">뒤꿈치 → 앞·중간발 착지로 바로 바꾸면</p>'
        '<p class="body"><span class="strong">무릎 앞 관절 부담은 낮고</span><br><span class="strong warn">발목을 아래로 미는 힘은 커지는</span> 쪽이었어요</p>'
        '<p class="note">연구가 많지 않아 근거는 아직 제한적이에요</p></div>', gap(20),
        '<p class="cite">Chan et al. 2018 · Anderson et al., Sports Med 2020</p>']),
    ('kind-shift', [
        '<h1 class="headline">착지 방식에 따라<br>부위별 부담이<br><span class="accent">달라질 수 있어요</span></h1>', gap(40),
        drake([('m_no.jpg', '✕', '영상 속 자세<br>바로 따라 하기', '#cc414a'), ('m_yes.jpg', '○', '내 몸이<br>준비됐는지<br>먼저 확인하기', '#0879d8')]), gap(36),
        '<p class="note">리뷰 연구진도 근육·힘줄이 버틸 수 있는지 보면서<br>착지는 천천히 바꿀 필요가 있다고 봤어요<br>(Anderson 2020)</p>']),
    ('kind-calf', [
        '<p class="note">센터의 제안</p>', gap(12),
        '<h1 class="headline">착지를 바꿀 거면<br><span class="accent">종아리 보강</span>부터!</h1>', gap(24),
        '<p class="body">앞·중간발 착지로 바꾸면<br>종아리가 할 일이 늘어날 수 있어요</p>', gap(24),
        photo('s08_assess.jpg', 300, 888, 0, -292, '한 발 뒤꿈치 들기를 하는 회원과 횟수를 세는 트레이너'), gap(28),
        '<div class="box" style="gap:10px">'
        '<p class="item">① 한 발 뒤꿈치 들기 <span class="note">무릎 펴고</span></p>'
        '<p class="item">② 무릎 굽혀 뒤꿈치 들기 <span class="note">깊은 종아리</span></p>'
        '</div>', gap(20),
        '<p class="note">센터에서 제안하는 운동이에요. 이 논문들은 이 운동으로<br>부상이 줄어드는지는 보지 않았어요. 통증이 있다면<br>운동 전에 평가부터 받으세요</p>']),
    ('kind-checklist center', [
        '<h1 class="headline">착지 바꾸기 전<br><span class="accent">체크리스트</span></h1>', gap(36),
        '<div class="list" style="gap:18px;align-items:flex-start">'
        '<p class="chk" style="text-align:left">☐ 왜 바꾸는지 목적이 있나요?</p>'
        '<p class="chk" style="text-align:left">☐ 최근 달리는 양을 갑자기 늘리진 않았나요?</p>'
        '<p class="chk" style="text-align:left">☐ 종아리 보강 운동을 하고 있나요?</p>'
        '<p class="chk" style="text-align:left">☐ 한 번에 하나, 짧은 구간부터 바꾸나요?</p>'
        '<p class="chk" style="text-align:left">☐ 바꾼 뒤 종아리·아킬레스를 살피나요?</p></div>', gap(36),
        '<div class="box"><p class="safety">통증이 있거나 부상이 반복된다면<br>자세보다 <span class="warn">원인 평가</span>가 먼저예요</p></div>', gap(28),
        '<p class="item">착지 바꿔 보려는 러닝 친구에게<br>보내 주세요</p>', gap(16),
        '<p class="note">센터의 제안 · 연구로 효과를 검증한 목록은 아니에요</p>']),
]
