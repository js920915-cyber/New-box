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
        '<p class="key">바꾸기 전에<br>꼭 알아 둘 것</p>']),
    ('kind-answer center', [
        '<p class="note">먼저 답부터</p>', gap(20),
        '<h1 class="headline">바꾸기 전에<br><span class="accent">내 다리 힘과<br>몸 상태</span>부터</h1>', gap(72),
        '<p class="body">자세를 바꾸면 몸이 받는 부담도<br>함께 달라질 수 있어요</p>', gap(64),
        '<div class="box"><p class="body">지금 아프지 않고 편하게 달린다면<br><span class="strong">그대로 달려도 괜찮아요</span></p></div>']),
    ('kind-case center', [
        '<h1 class="headline"><span class="accent">부드럽게 착지</span>하는<br>연습을 했더니</h1>', gap(20),
        '<p class="note">착지 충격이 큰 초보 러너 · 2주 트레드밀 연습 · 1년 추적</p>', gap(32),
        '<div class="box" style="gap:6px"><p class="body">1년간 다친 사람 <span class="note">(비율)</span></p>'
        '<p class="key">화면 보며 연습한 그룹 <span class="accent">16%</span></p><p class="item">그냥 달린 그룹 38%</p></div>', gap(20),
        '<div class="box" style="gap:6px"><p class="body">그런데 종아리·아킬레스 부상 <span class="note">(보고 건수)</span></p>'
        '<p class="key">화면 보며 연습한 그룹 <span class="warn">10건</span></p><p class="item">그냥 달린 그룹 0건</p></div>', gap(36),
        '<p class="body">전체는 덜 다쳤지만, <span class="strong">다친 곳이 달랐어요</span></p>', gap(16),
        '<p class="cite">Chan et al., Am J Sports Med 2018</p>']),
    ('kind-why center', [
        '<h1 class="headline">착지가 바뀌면<br>일하는 곳도<br><span class="accent">달라질 수 있어요</span></h1>', gap(48),
        '<p class="body">평소 뒤꿈치로 디디다가<br>발 앞쪽으로 바꾸면</p>', gap(24),
        '<div class="box"><p class="body">바꾼 직후 무릎 앞쪽 부담은 줄고<br><span class="strong warn">발목·종아리 쪽 부담</span>은 커질 수 있어요</p></div>', gap(28),
        '<p class="note">여러 연구를 모은 리뷰 결과예요 · 근거는 아직 제한적</p>', gap(10),
        '<p class="cite">Anderson et al., Sports Med 2020</p>']),
    ('kind-check center', [
        '<h1 class="headline">바꾸기 전<br><span class="accent">확인할 것</span></h1>', gap(40),
        '<div class="box" style="gap:12px"><p class="item accent">내가 돌아볼 것</p>'
        '<p class="body">☐ 최근 달리는 양을 늘렸나요?</p>'
        '<p class="body">☐ 달릴 때나 다음 날<br>반복해서 불편한 곳이 있나요?</p></div>', gap(24),
        '<div class="box" style="gap:12px"><p class="item accent">전문가가 봐 줄 것</p>'
        '<p class="body">다리 힘 · 움직임 · 착지</p>'
        '<p class="note">바꾸려는 자세를 내 몸이 버틸 수 있는지</p></div>']),
    ('kind-end center', [
        '<h1 class="headline">바꿀 땐 <span class="accent">조금씩</span></h1>', gap(24),
        '<p class="body">짧은 구간부터 바꾸고,<br>다음 날 몸의 반응을 보며 늘려요</p>', gap(32),
        slot(220), gap(24),
        '<p class="item">R스포츠재활센터는 이렇게 해요</p>', gap(12),
        '<p class="body">경력·거리 인터뷰 → 신체 평가 → 천천히 교정</p>', gap(24),
        '<div class="box"><p class="safety">통증이 있거나 부상이 반복된다면<br>자세보다 <span class="warn">원인 평가</span>가 먼저예요</p></div>', gap(20),
        '<p class="note">자세 바꿔 보려는 러닝 친구에게 보내 주세요</p>']),
]
