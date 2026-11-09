import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent import policy as P

POL = P.load_policy()


def fresh():
    return {"calls_made": 0, "patients_touched": set()}


def test_precheck_ok():
    assert P.precheck(POL) == []


def test_export_is_refused():
    assert P.check(POL, "export_records", {"destination": "x"}, fresh()).verdict == "refuse"


def test_override_is_forbidden_for_any_agent():
    assert P.check(POL, "discharge_override", {"patient_id": "P001"}, fresh()).verdict == "refuse"


def test_followup_needs_approval():
    assert P.check(POL, "schedule_followup", {"patient_id": "P007", "days": 3}, fresh()).verdict == "approval"


def test_scope_blocks_other_hospital():
    assert P.check(POL, "lookup_patient", {"patient_id": "P011"}, fresh()).verdict == "refuse"


def test_budget():
    st = fresh()
    st["calls_made"] = POL["max_tool_calls_per_task"]
    assert P.check(POL, "lookup_patient", {"patient_id": "P003"}, st).verdict == "refuse"
