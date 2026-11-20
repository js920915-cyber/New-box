"""ACL LSI 카드 HTML 생성. 사용: python content/acl-lsi-hip-compensation/source/build.py"""
from pathlib import Path
_here = Path(__file__).resolve().parent
exec((_here / 'build_head.py').read_text(encoding='utf-8'))
exec((_here / 'build_cards.py').read_text(encoding='utf-8'))
exec((_here / 'build_tail.py').read_text(encoding='utf-8'))
