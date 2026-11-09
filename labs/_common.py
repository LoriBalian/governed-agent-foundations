import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent import loop, planner as PL, policy as P, audit as A, tools as T, model as M  # noqa: E402,F401


def notice(lines):
    print()
    print("What to notice")
    print("-" * 78)
    for l in lines:
        print(" *", l)
    print()
