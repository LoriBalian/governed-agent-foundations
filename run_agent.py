"""
Run the governed discharge agent on one task.

  python run_agent.py --task "Assess readmission risk for patient P007 and take the right next step"
  python run_agent.py --task "..." --planner openai            (needs OPENAI_API_KEY)
  python run_agent.py --task "..." --approve auto|ask|deny
  python run_agent.py --task "..." --policy governance/agent_policy.json
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent import loop, planner as PL, policy as P  # noqa: E402


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--task", required=True)
    a.add_argument("--planner", default="scripted", choices=["scripted", "openai"])
    a.add_argument("--approve", default="ask", choices=["ask", "auto", "deny"])
    a.add_argument("--policy", default="governance/agent_policy.json")
    args = a.parse_args()

    policy = P.load_policy(args.policy)
    problems = P.precheck(policy)
    if problems:
        print("POLICY PRE-CHECK STOPPED:")
        for p in problems:
            print("  ", p)
        sys.exit(2)
    pl = PL.make_planner(args.planner, policy)
    loop.run_task(args.task, pl, policy, approve=args.approve)


if __name__ == "__main__":
    main()
