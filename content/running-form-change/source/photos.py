# 사진 설정 — build.py가 읽는다. 값이 None이면 '사진 넣는 자리'(촬영 안내 포함).
# PHOTOS[key] = (파일, 창 높이, 이미지 폭, 창 기준 x, 창 기준 y, 대체 텍스트) 또는 None
PHOTOS = {
    'cover': ('running-styles_ChrisHunkeler_ccbysa20.jpg', 700, 1000, -56, -40, '발가락 신발을 신은 남자와 쿠션화를 신은 여자가 나란히 달리는 모습'),
    'crowd': ('paris-marathon-2007_gadl_ccbysa20.jpg', 560, 960, -60, -160, '센강변 도로를 각자 다른 자세로 달리는 마라톤 참가자들'),
    'heel': ('heel-strike_PetarMilosevic_ccbysa40.jpg', 580, 960, -36, -50, '뒤꿈치부터 닿으려는 러너의 다리 옆모습'),
    'ostrich': ('ostrich_JorgeLascar_ccby20.jpg', 640, 1150, -216, -124, '흙길을 달리는 타조 세 마리 뒷모습'),
    'clinic': None,
}
SLOTS = {
    'clinic': (640, '센터에서 상담·평가받는 러너<br>트레이너와 함께 · 초상 사용 동의'),
}
MAP_W, MAP_H, MAP_PHOTO, MAP_SLOT, MAP_SLOT_TOP, MAP_TAGS = 288, 700, None, '', (0, 0), []
