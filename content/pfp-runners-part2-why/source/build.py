"""PFP 2탄 추가 카드 1장(병인: 무릎 앞 통증은 왜 생길까). 사용자가 2탄 세트에 직접 합친다.
디자인·CSS는 pfp-runners-part2/source/build.py와 같다. 사용: python3 content/pfp-runners-part2-why/source/build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'pfp-runners-part2/source'))
import build as part2  # noqa: E402

part2.write_cards([part2.WHY_CARD], HERE)
