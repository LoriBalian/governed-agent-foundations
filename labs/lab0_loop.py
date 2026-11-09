"""
LAB 0 | The loop. One task, two tools, no model, no LLM.

The scripted planner reads a record and writes a care note. Watch the shape:
PLAN -> POLICY -> RESULT, every step, and a FINAL. Then open the audit log.
"""
from _common import loop, PL, P, notice

policy = P.load_policy()
problems = P.precheck(policy)
print("policy pre-check:", "ok" if not problems else problems)
loop.run_task("Look up patient P003 and write a care note summarizing the record.",
              PL.ScriptedPlanner(), policy, approve="ask")
notice([
    "The agent did not decide anything clinical. It observed, chose a tool, passed a policy check, acted, and wrote a line of evidence.",
    "Two tools ran: a read (lookup_patient) and a write (write_care_note). Both were on the allow list, so no human was asked.",
    "Open artifacts/agent_audit_log.jsonl: four lines for this task (task_start, two tool_allowed, task_end).",
    "The planner here is a rule book. In Lab 5 a language model takes its seat; the loop, the policy and the log do not change.",
])
