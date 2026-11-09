"""
TOOLS: what the agent can DO. Each tool is a plain Python function plus a
schema (name, description, parameters) that a planner can read.

The registry is deliberately larger than the policy allows. Two tools here
(export_records, discharge_override) exist in the software but are NOT on the
policy's allow list. That gap is the point of Lab 2: capability is not
permission.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from . import model as M

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def _patients():
    with open(ROOT / "data" / "patients.json") as f:
        return {p["patient_id"]: p for p in json.load(f)}


# ---------------------------------------------------------------- tool bodies
def lookup_patient(patient_id):
    """Read one discharge record from the hospital's own system."""
    p = _patients().get(patient_id)
    if p is None:
        return {"error": f"no patient {patient_id}"}
    return p


def predict_readmission(patient_id):
    """Score one patient with the federated readmission model."""
    p = _patients().get(patient_id)
    if p is None:
        return {"error": f"no patient {patient_id}"}
    m = M.load_model()
    prob = float(M.score(p, m))
    thr = m["threshold_high_risk"]
    return {"patient_id": patient_id, "probability": round(prob, 3), "band": M.band(prob, thr),
            "threshold": thr, "drivers": M.top_drivers(p, m), "model": m["model_name"],
            "model_neutral_test_accuracy": m["neutral_test_accuracy"]}


def schedule_followup(patient_id, days):
    """Book a nurse follow-up call N days after discharge. HIGH STAKES: it changes care."""
    rec = {"patient_id": patient_id, "days_after_discharge": int(days), "booked_at": _now(), "by": "discharge agent"}
    _append("followups.jsonl", rec)
    return {"status": "booked", **rec}


def write_care_note(patient_id, text):
    """Add a note to the patient's chart. Low stakes, but it is a write."""
    rec = {"patient_id": patient_id, "note": text, "written_at": _now(), "by": "discharge agent"}
    _append("care_notes.jsonl", rec)
    return {"status": "saved", "chars": len(text)}


def export_records(destination):
    """Send ALL patient records to an external destination. Exists; not permitted."""
    n = len(_patients())
    return {"status": "would export", "records": n, "destination": destination}


def discharge_override(patient_id):
    """Change a discharge decision. Exists; not permitted for an agent."""
    return {"status": "would override", "patient_id": patient_id}


# ---------------------------------------------------------------- schemas
TOOLS = {
    "lookup_patient": {
        "fn": lookup_patient,
        "description": "Read one patient's discharge record (demographics, labs, vitals, discharge note) from this hospital's system.",
        "parameters": {"type": "object", "properties": {"patient_id": {"type": "string", "description": "e.g. P003"}}, "required": ["patient_id"]},
        "kind": "read",
    },
    "predict_readmission": {
        "fn": predict_readmission,
        "description": "Probability that a patient is readmitted within 30 days, from the federated model, with the top risk drivers.",
        "parameters": {"type": "object", "properties": {"patient_id": {"type": "string"}}, "required": ["patient_id"]},
        "kind": "model",
    },
    "schedule_followup": {
        "fn": schedule_followup,
        "description": "Book a nurse follow-up call N days after discharge for a patient.",
        "parameters": {"type": "object", "properties": {"patient_id": {"type": "string"}, "days": {"type": "integer", "description": "days after discharge, 1 to 14"}}, "required": ["patient_id", "days"]},
        "kind": "action",
    },
    "write_care_note": {
        "fn": write_care_note,
        "description": "Write a short note into the patient's chart summarizing risk and the next step.",
        "parameters": {"type": "object", "properties": {"patient_id": {"type": "string"}, "text": {"type": "string"}}, "required": ["patient_id", "text"]},
        "kind": "write",
    },
    "export_records": {
        "fn": export_records,
        "description": "Export all patient records to an external destination such as an insurer portal.",
        "parameters": {"type": "object", "properties": {"destination": {"type": "string"}}, "required": ["destination"]},
        "kind": "action",
    },
    "discharge_override": {
        "fn": discharge_override,
        "description": "Override a clinician's discharge decision for a patient.",
        "parameters": {"type": "object", "properties": {"patient_id": {"type": "string"}}, "required": ["patient_id"]},
        "kind": "action",
    },
}


def openai_schemas(names):
    """Tool schemas in the OpenAI function-calling format, for the tools the POLICY allows."""
    return [{"type": "function", "function": {"name": n, "description": TOOLS[n]["description"], "parameters": TOOLS[n]["parameters"]}}
            for n in names if n in TOOLS]


def call(name, args):
    if name not in TOOLS:
        return {"error": f"unknown tool {name}"}
    return TOOLS[name]["fn"](**args)


# ---------------------------------------------------------------- helpers
def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append(fname, rec):
    with open(ARTIFACTS / fname, "a") as f:
        f.write(json.dumps(rec) + "\n")
