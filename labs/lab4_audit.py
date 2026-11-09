"""
LAB 4 | Evidence: read the audit log like an auditor, then write the agent card.
"""
from _common import A, P, M, notice

policy = P.load_policy()
entries = A.read_log(policy)
s = A.summarize(entries)
print("=" * 78)
print(f"AUDIT LOG  {policy['logging']['audit_log']}   ({len(entries)} events)")
print("=" * 78)
print(f"tasks run:            {s['tasks']}")
print(f"tool calls allowed:   {s['tool_calls_allowed']}   by tool: {s['by_tool']}")
print(f"refusals:             {len(s['refusals'])}")
for t, r in s["refusals"]:
    print(f"    {t:<20} {r}")
print(f"approvals:            {s['approvals']}")
print(f"planners used:        {s['planners']}")
print()
print("last 5 events:")
for e in entries[-5:]:
    keep = {k: v for k, v in e.items() if k in ("ts", "event", "tool", "outcome", "reason", "final")}
    print("   ", keep)

card = A.agent_card(policy, M.load_model(), s)
print(f"\nwrote {card.relative_to(A.ROOT)}  (open it: Ctrl + Shift + V for the preview)")
notice([
    "Every refusal and every approval of the night is here with a timestamp, the tool, the arguments and the reason. That is the auditor's view of the agent.",
    "The agent card sits next to the Week 6 model card: purpose, allowed and forbidden actions, scope, budgets, the model's accuracy floor, and the evidence so far.",
    "Two questions are left blank on the card on purpose. Answer them in your notes: who reads this log, and which approval could be automated later and on what evidence.",
])
