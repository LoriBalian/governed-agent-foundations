"""
POLICY AS CODE for an agent: the charter idea from Week 6, applied to ACTIONS.

The policy answers four questions before any tool runs:
  1. Is this tool on the allow list at all?            (capability is not permission)
  2. Is this action high stakes? Then a human decides.  (approval gate)
  3. Is the agent inside its data scope and budgets?   (least privilege, call limits)
  4. Is the model it relies on still fit for use?      (the Week 6 model card, checked)

Every answer is written to the audit log by the loop (agent/audit.py).
"""
import json
from pathlib import Path

from . import model as M

ROOT = Path(__file__).resolve().parents[1]


def load_policy(path="governance/agent_policy.json"):
    with open(ROOT / path) as f:
        return json.load(f)


def precheck(policy):
    """Checks that run BEFORE the agent takes its first step. Returns a list of problems (empty = ok)."""
    problems = []
    for t in policy.get("approval_required", []):
        if t not in policy["allowed_tools"]:
            problems.append(f"approval_required lists {t} but it is not an allowed tool")
    for t in policy.get("forbidden_for_any_agent", []):
        if t in policy["allowed_tools"]:
            problems.append(f"{t} is forbidden for any agent but appears in allowed_tools")
    if policy["max_tool_calls_per_task"] < 1:
        problems.append("max_tool_calls_per_task must be at least 1")
    m = M.load_model(policy["model"]["path"])
    if m["neutral_test_accuracy"] < policy["model"]["min_neutral_test_accuracy"]:
        problems.append(f"model accuracy {m['neutral_test_accuracy']} is below the policy floor {policy['model']['min_neutral_test_accuracy']}")
    return problems


class Decision:
    def __init__(self, verdict, reason):
        self.verdict = verdict      # "allow" | "approval" | "refuse"
        self.reason = reason

    def __repr__(self):
        return f"{self.verdict}: {self.reason}"


def check(policy, name, args, state):
    """
    Decide about ONE proposed tool call.
    state: dict with calls_made (int) and patients_touched (set) for this task.
    """
    if name in policy.get("forbidden_for_any_agent", []):
        return Decision("refuse", f"{name} is forbidden for any agent by {policy['policy_name']}")
    if name not in policy["allowed_tools"]:
        return Decision("refuse", f"{name} is not on the allow list {policy['allowed_tools']}")
    if state["calls_made"] >= policy["max_tool_calls_per_task"]:
        return Decision("refuse", f"call budget exhausted: max_tool_calls_per_task = {policy['max_tool_calls_per_task']}")

    pid = args.get("patient_id")
    if pid is not None:
        touched = set(state["patients_touched"])
        if pid not in touched and len(touched) >= policy["max_patients_per_task"]:
            return Decision("refuse", f"max_patients_per_task = {policy['max_patients_per_task']}; already touched {sorted(touched)}")
        hosp = _hospital_of(pid)
        if hosp is None:
            return Decision("refuse", f"unknown patient {pid}")
        if hosp not in policy["data_scope"]["hospitals"]:
            return Decision("refuse", f"patient {pid} belongs to {hosp}; data scope is {policy['data_scope']['hospitals']}")

    if name in policy.get("approval_required", []):
        return Decision("approval", f"{name} is high stakes under {policy['policy_name']} v{policy['policy_version']}: a human must approve")
    return Decision("allow", f"on allow list; call {state['calls_made'] + 1} of {policy['max_tool_calls_per_task']}")


def _hospital_of(pid):
    with open(ROOT / "data" / "patients.json") as f:
        for p in json.load(f):
            if p["patient_id"] == pid:
                return p["hospital"]
    return None
