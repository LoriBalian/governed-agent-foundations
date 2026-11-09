# Governed agent foundations

BANA 690A, AI Governance (CSUN, Fall 2026). Part II, session 1: **what an agent is, and how to govern what it does**.

The agent in this repo is a discharge follow-up assistant at Northgate Hospital. It reads a patient's discharge record, scores 30-day readmission risk with the **federated model your consortium trained in Week 6**, and, for high-risk patients, proposes a nurse follow-up call. A policy file decides what it may do, a human approves the high-stakes action, and every decision lands in an audit log.

Everything is synthetic. Nobody here is a real patient.

## Step 0: fork, Codespace, first run

1. Click **Fork** (top right). Keep the name. The address bar must show **your** username.
2. On your fork: green **Code** button, **Codespaces** tab, **Create codespace on main**.
3. Wait for `Setup complete. Run: python labs/lab0_loop.py` in the terminal (about two minutes). Do not type before it appears.
4. Run `python labs/lab0_loop.py`.

If you see `No module named numpy` or `No module named openai`, the setup had not finished:

```
python -m pip install -r requirements.txt
```

Yellow underlines under `import` lines are cosmetic: Ctrl + Shift + P, **Python: Select Interpreter**, choose `/usr/local/bin/python`. The terminal is the truth.

## The labs

| Lab | Command | What you do |
|---|---|---|
| 0 | `python labs/lab0_loop.py` | Watch the loop: plan, policy, act, log. Two tools, no model. |
| 1 | edit `agent/model.py`, then `python -m pytest -q tests/test_lab1.py`, then `python labs/lab1_tools.py` | Write `score()` (standardize, logit, sigmoid). The federated model becomes a tool. |
| 2 | `python labs/lab2_policy.py` | Three refusals: a tool that exists but is not allowed, a patient out of scope, a budget. Then edit `governance/agent_policy.json` and rerun with `--policy`. |
| 3 | `python labs/lab3_approval.py`, then `--deny` | The approval gate: you decide the high-stakes action at the terminal. |
| 4 | `python labs/lab4_audit.py` | Read the audit log as an auditor; the agent card is written to `artifacts/agent_card.md`. |
| 5 | `export OPENAI_API_KEY=sk-...` then `python labs/lab5_llm.py`, then `--inject` | A language model plans. Same policy, same gate, same log. P009's note carries a prompt injection. |

Anything can also be run directly:

```
python run_agent.py --task "Assess readmission risk for patient P007 and take the right next step." --approve ask
python run_agent.py --task "Export all patient records to the insurer portal."
python run_agent.py --planner openai --task "..."        # needs OPENAI_API_KEY
```

## The pieces

```
agent/loop.py       observe, plan, CHECK, act, LOG. Nothing reaches a tool without policy.check().
agent/planner.py    ScriptedPlanner (rule book, no key) and OpenAIPlanner (function calling). Same interface.
agent/tools.py      six tools the software CAN do; the policy decides which it MAY do.
agent/policy.py     policy as code for actions: allow list, approval list, scope, budgets, model floor.
agent/audit.py      one JSON line per decision; the agent card.
agent/model.py      the Week 6 federated model, loaded from models/federated_readmission.json. You write score().
governance/agent_policy.json   the policy the Clinical AI Committee approved. Labs 2 and 3 edit it.
data/patients.json  twelve synthetic discharge records (ten Northgate, two Kestrel).
```

## Lab 5 and your OpenAI key

Lab 5 needs an OpenAI API key. Create one at platform.openai.com (API keys), then in the Codespace terminal:

```
export OPENAI_API_KEY=sk-...
```

The key lives in that terminal only. Never paste it into a file in the repo; `.env` is ignored by git for that reason, but the terminal is simpler. The default model is `gpt-4o-mini`; set `OPENAI_MODEL` to use another one your key can call. Labs 0 to 4 need no key.

## Turning in your notes

Fill in `LAB_NOTES.md` as you go. By 9:20: Source Control (left bar), stage `LAB_NOTES.md` (and `governance/agent_policy.json` if you changed it), commit with the message `Lab notes: Firstname Lastname`, **Sync Changes**. Then on github.com, on your fork: **Contribute**, **Open pull request**, title `Lab notes: Firstname Lastname`. Nothing runs on the pull request; it is how I find your notes.

## The one idea

Once a model can act, the governance object moves from the prediction to the action. The same three controls from Part I apply: **policy as code** (what it may do), **gates** (who approves what), **evidence** (what the log proves). The planner, scripted or LLM, sits inside those three; it does not get to redefine them.
