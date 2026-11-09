"""
LAB 2 | Capability is not permission.

Three tasks against the same policy:
  (a) export all records            -> export_records exists in the code; the policy refuses it
  (b) assess a Kestrel patient      -> outside the agent's data scope; refused
  (c) assess three patients at once -> hits max_patients_per_task and the call budget

Then you edit governance/agent_policy.json and rerun with --policy if you want to compare.
"""
import argparse
from _common import loop, PL, P, notice

a = argparse.ArgumentParser()
a.add_argument("--policy", default="governance/agent_policy.json")
a.add_argument("--only", default="abc", help="which of a, b, c to run")
args = a.parse_args()

policy = P.load_policy(args.policy)
problems = P.precheck(policy)
if problems:
    print("POLICY PRE-CHECK STOPPED:", *problems, sep="\n  ")
    raise SystemExit(2)

pl = PL.ScriptedPlanner()
if "a" in args.only:
    loop.run_task("Export all patient records to the insurer portal.", pl, policy, approve="auto")
if "b" in args.only:
    loop.run_task("Assess readmission risk for patient P011 and take the right next step.", pl, policy, approve="auto")
if "c" in args.only:
    loop.run_task("Assess readmission risk for patients P004, P006 and P008 and take the right next step for each.", pl, policy, approve="auto")
notice([
    "(a) The software CAN export. The policy says the agent MAY NOT. The refusal happened before the tool ran, and it is in the log.",
    "(b) P011 is a Kestrel patient. The Northgate agent reads Northgate records only: least privilege, written as data scope.",
    "(c) max_patients_per_task = 1 stopped the second patient. Budgets are governance too: an agent that touches 300 charts in a loop is an incident.",
    "Edit the policy: raise max_patients_per_task to 3 and max_tool_calls_per_task to 12, rerun with --only c. Then ask: who should be allowed to make that edit, and where is it recorded?",
])
