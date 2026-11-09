import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from agent import model as M


def _avg_patient(m):
    return {f: m["human_units_mean_sd"][f][0] for f in m["features"]}


def test_average_patient_scores_sigmoid_of_bias():
    m = M.load_model()
    p = M.score(_avg_patient(m), m)
    assert abs(p - M.sigmoid(m["bias"])) < 1e-9


def test_one_sd_more_prior_admissions_raises_risk():
    m = M.load_model()
    rec = _avg_patient(m)
    base = M.score(rec, m)
    rec["prior_admissions_12m"] += m["human_units_mean_sd"]["prior_admissions_12m"][1]
    assert M.score(rec, m) > base


def test_known_patient_p006_is_high_risk():
    import json
    m = M.load_model()
    pts = {p["patient_id"]: p for p in json.load(open(Path(__file__).resolve().parents[1] / "data" / "patients.json"))}
    p = M.score(pts["P006"], m)
    assert 0.85 < p < 0.95
    assert M.band(p, m["threshold_high_risk"]) == "HIGH"
