"""
LAB 3 | The approval gate: a human decides the high-stakes action.

P007 is HIGH risk. The agent proposes schedule_followup. Under the policy that
tool needs a human. Run once and approve (y), run again and reject (n), then
read both in the audit log.

  python labs/lab3_approval.py            (you answer y or n at the prompt)
  python labs/lab3_approval.py --deny     (scripted rejection, for comparison)
"""
import argparse
from _common import loop, PL, P, notice

a = argparse.ArgumentParser()
a.add_argument("--deny", action="store_true")
a.add_argument("--auto", action="store_true")
args = a.parse_args()
mode = "deny" if args.deny else ("auto" if args.auto else "ask")

policy = P.load_policy()
loop.run_task("Assess readmission risk for patient P007 and take the right next step.", PL.ScriptedPlanner(), policy, approve=mode)
notice([
    "The agent did the analysis (lookup, predict) alone and stopped at the first action that changes care. That boundary is the policy's approval_required list.",
    "Approved: the call is booked and the log says approved, by whom (mode), for which arguments. Rejected: nothing ran, and the log says so too.",
    "A gate that a human always clicks through is theater. The nurse needs the drivers on the screen to make a real decision; that is why predict_readmission returns them.",
    "Edit: remove schedule_followup from approval_required and rerun. It books without asking. Put it back. Which of YOUR final project's actions belong on that list?",
])
