"""
LAB 1 | Give the agent the federated model as a tool.

You write score() in agent/model.py (three lines: standardize, logit, sigmoid).
Then the test, then this lab: the agent assesses a LOW-risk and a HIGH-risk patient.
"""
import sys
from _common import loop, PL, P, M, notice

try:
    m = M.load_model()
    p = M.score({f: M.load_model()["human_units_mean_sd"][f][0] for f in m["features"]}, m)
    print(f"sanity check: an average patient scores {p:.3f} (should equal sigmoid(bias) = {M.sigmoid(m['bias']):.3f})")
except NotImplementedError as e:
    print("Lab 1 is not done yet:", e)
    print("Open agent/model.py, replace the raise line in score(), save, then: python -m pytest -q tests/test_lab1.py")
    sys.exit(1)

policy = P.load_policy()
loop.run_task("Assess readmission risk for patient P003 and take the right next step.", PL.ScriptedPlanner(), policy, approve="auto")
loop.run_task("Assess readmission risk for patient P006 and take the right next step.", PL.ScriptedPlanner(), policy, approve="auto")
notice([
    "P003 came back LOW: the agent wrote a note and stopped. P006 came back HIGH: the agent proposed schedule_followup, a high-stakes action.",
    "Tonight approve=auto said yes for you. Lab 3 puts a human in that seat.",
    "The model is the Week 6 federation's model (neutral test accuracy 0.806). The agent is a consumer of the model card, not its author.",
    "drivers shows which standardized features pushed the risk up: the explanation the nurse reads before calling.",
])
