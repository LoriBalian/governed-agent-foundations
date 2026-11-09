# Final Project: A Governed Analytics Agent Team on Federated Data

BANA 690A AI Governance, Fall 2026. Released Nov 9, 2026. Teams: your five existing groups. Weight: 40% of the course grade. Assignment 4 is absorbed into this project; there are no further individual assignments after Assignment 3.


## 1. What you build

Your team builds a system of AI agents that answers business questions about a consortium's data across the four lenses of analytics, where the predictive model is trained by federated learning across the consortium's members, and where the whole system is governed the way this course has taught: policy as code, gates, and evidence.

The shape is fixed; the domain is yours.


| Component | What it is | What it must do |
|---|---|---|
| Consortium data | Three or more members (hospitals, insurers, branches, departments, stores) that cannot pool their data | Synthetic or public data partitioned across members with at least one non-IID skew (quantity, label, feature or concept). No real personal data. |
| Federated model | The predictive model, trained with FedAvg across the members | Compared against a centralized baseline and a local-only baseline; one skew experiment; a federation charter (JSON) with a gate; model card. The numpy engine from governed-fl-foundations is sufficient; Flower is optional. |
| Coordinator agent | Takes a business question, decomposes it, routes to the specialists, assembles the answer | Uses function calling (OpenAI) through the course loop; every tool call passes the policy; every decision is logged. |
| Descriptive specialist | What happened | Tools that compute KPIs, trends and per-member summaries without moving a member's raw rows to another member. |
| Diagnostic specialist | Why | Tools that compare segments and members, rank drivers, and explain a change. |
| Predictive specialist | What will happen | The federated model exposed as a tool with probabilities, bands and drivers, plus the model card facts (accuracy, floor, provenance). |
| Prescriptive specialist | What to do | Recommends actions under the policy; actions that change the world go through a human approval gate; some actions are forbidden outright. |
| Governance layer | The Part I payoff | Agent policy as code, federation charter and gate, audit log, model card and agent card, risk register, privacy analysis, evaluation gold set, CI pipeline with an evaluation gate. |


## 2. Technical requirements

1. Federated training of the predictive model across 3 or more simulated members with FedAvg, a centralized baseline and a local-only baseline, at least one non-IID experiment, and at least one defense or privacy control exercised (clipping, robust aggregation, secure aggregation or differential privacy) with its cost measured.
2. A federation charter (JSON) with a pre-check and a gate (global accuracy, per-member floor, gap, privacy control present), and the audit log and model card the gate produces. Reuse run_federation.py from governed-fl-foundations.
3. A coordinator agent plus four specialists (descriptive, diagnostic, predictive, prescriptive), built on the loop, policy, audit and planner modules from governed-agent-foundations. The planner is an OpenAI model with function calling; a scripted fallback planner is required so the system can be demonstrated without a key.
4. At least eight tools across the specialists, with schemas. At least two prescriptive actions, at least one of which requires human approval and at least one of which is forbidden for any agent.
5. An agent policy (JSON) with allow lists, approval list, forbidden list, data scope, budgets and the model floor; the pre-check must refuse an inconsistent policy or an unfit model.
6. A gold set of 20 or more questions with expected behavior (which tools, which lens, approval or refusal expected), including at least five adversarial cases (a prompt injection in data, a request for a forbidden action, an out-of-scope member, a budget overrun, a model-floor breach). An evaluation script scores the system against it.
7. A CI pipeline (GitHub Actions) that runs the unit tests, the policy and charter pre-checks, and the gold-set evaluation, and fails if the pass rate drops below a threshold you set and justify.
8. A five-minute demo video and a live demo of three questions: one that crosses lenses, one that ends in an approved action, one that ends in a refusal.


## 3. Governance package

1. Model card for the federated model (training members and sizes, charter, accuracy overall and per member, skew results, intended and prohibited uses).
2. Agent card for the system (purpose, allowed, gated and forbidden actions, scope and budgets, the model it relies on, evidence summary, open questions). Start from the Lab 4 generator.
3. Risk register with 10 or more items: likelihood, impact, owner, mitigation, and the NIST AI RMF function each maps to (Govern, Map, Measure, Manage).
4. Privacy analysis, one to two pages: what your federation protects and does not (Week 6: updates leak, members can poison, the coordinator sees), the control you implemented, and the residual risk.
5. Approval design, one page: every tool classified as read, analyze, write, act or never, with the reason; who approves, what they see, and the evidence you would need to automate any gate later.
6. Deployment and monitoring plan, one page: who reads the audit log and how often, which signals pull the agent (refusal rate, rubber-stamp rate, model floor), rollback.


## 4. Milestones and grading (40 points)


| Due | Milestone | Turned in | Points |
|---|---|---|---|
| Nov 16, in class | Proposal | Two pages (template in section 6). A 30-minute studio at the end of the Nov 16 session is for finishing it. | 4 |
| Nov 23, in class | Build check-in | Team repo with the federation running (FedAvg vs centralized, one skew) and at least one specialist answering a question through the loop. Feedback, not points. | 0 |
| Nov 30, in class | Governance checkpoint and peer review | Draft agent policy, risk register, model card and agent card, gold set draft. Demo to another team using the rubric; written peer feedback. | 4 |
| Dec 7, in class | Presentation | 15 minutes per team: live demo of three questions, architecture, federation results, governance highlights, then questions. | 6 |
| Dec 11, 11:59 PM | Final submission | Repository (code, CI, evaluation), demo video (5 min), governance package, individual contribution statements. | Technical 14, governance package 8, individual 4 |

Technical implementation (14): federation and charter 4; coordinator and specialists 6; CI, gold set and evaluation 4. Governance package (8): the six documents in section 3, graded on specificity to your system, not on length. Individual contribution and peer evaluation (4): each student's contribution statement, the commit history, and the peer forms.


## 5. Rubric highlights


| Area | Full credit looks like | Partial credit looks like |
|---|---|---|
| Federation | Three baselines reported per member; a skew that changes a conclusion; a defense whose cost is measured; the gate makes a decision on evidence | Federation runs; one accuracy number; no per-member view; no skew |
| Agents | The coordinator routes to the right specialist, answers cross-lens questions, and the predictive tool carries the model card facts; scripted fallback works | A single agent with tools; the LLM answers without tools; no fallback |
| Governance of actions | Every tool classified; the approval gate shows decision material; a forbidden action is refused and logged; budgets and scope hold under the adversarial cases | An allow list only; approvals that are never rejected; injection case not tested |
| Evidence and CI | Audit log reconstructs any run; cards are specific; the pipeline fails on a gold-set regression you can demonstrate | Logs exist but no one can read them; a card that repeats the policy file; CI runs tests only |
| Presentation | Three live questions including a refusal and an approval; the team can explain every number | A recorded demo only; numbers nobody can explain |


## 6. Proposal template (two pages, due Nov 16)

1. Consortium and domain: who the members are, why they cannot pool data, what the business questions are (five, at least one per lens and one that crosses lenses).
2. Data and partition plan: source (synthetic or public), size per member, the skew you will introduce and why it is realistic.
3. The model: target variable, features, the prediction's business use, the prohibited uses.
4. The agents: the coordinator's routing logic in one paragraph; each specialist's tools in a table (tool, verb, read/analyze/write/act/never, approval yes or no).
5. The policy sketch: allow list, approval list, forbidden list, scope, budgets, model floor.
6. Risks you already see: five items for the register.
7. Team roles: one owner per specialist, one for governance and CI; everyone on the coordinator.
8. Repository link (the team repo, created from a fork of governed-agent-foundations, with the fl/ engine copied in).


## 7. Rules

- Use the course repos as the starter: governed-agent-foundations (loop, policy, audit, planner, agent card) and governed-fl-foundations (world, model, federation, aggregators, charter, gate, model card). Replacing them with a framework (Flower, LangGraph, CrewAI) is allowed if the governance layer still does what section 2 requires.
- AI assistants may be used for coding and drafting and must be disclosed; every team member must be able to explain every artifact in the demo and in the questions after it.
- OpenAI keys live in environment variables or Codespaces secrets, never in the repository. A committed key is a governance failure and costs points.
- No real personal data. Synthetic generators or public datasets with documented provenance.
- Individual contribution statements are required and are checked against the commit history.


> **Start from what exists** The repo you forked tonight already has the loop, the policy, the approval gate, the audit log and the agent card. The federation you ran in Week 6 already has the charter, the gate and the model card. The project is the integration of what you have built, around a domain you choose and questions you write.
