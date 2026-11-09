"""
THE MODEL TOOL: the readmission model trained by the federation in Week 6.

models/federated_readmission.json holds what the coordinator published after
the Lab 7 clean run: 24 weights, one bias, the feature names, the human-unit
mean and sd agreed by the consortium, and the model card facts (accuracy on
the neutral test set, per hospital). No patient record is in that file.

The agent never trains anything. It USES this model as one tool among several.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_model(path="models/federated_readmission.json"):
    with open(ROOT / path) as f:
        return json.load(f)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def standardize(record, m):
    """Human units in, z-scores out, in the model's feature order."""
    return np.array([(float(record[f]) - m["human_units_mean_sd"][f][0]) / m["human_units_mean_sd"][f][1]
                     for f in m["features"]])


def score(record, m):
    """
    LAB 1: you write this function.

    Return the probability (a float between 0 and 1) that this patient is
    readmitted within 30 days, using the federated model m.

    Three steps, exactly as in Week 6:
      1. z = standardize(record, m)                     one z-score per feature
      2. logit = z dot weights + bias                   (m["weights"], m["bias"])
      3. probability = sigmoid(logit)

    Hint: np.array(m["weights"]) turns the list into a vector; use z @ w.
    """
    raise NotImplementedError("Lab 1: implement score() in agent/model.py")


def top_drivers(record, m, k=3):
    """The k features pushing this patient's risk up the most (weight times z-score)."""
    z = standardize(record, m)
    w = np.array(m["weights"])
    contrib = w * z
    order = np.argsort(-contrib)[:k]
    return [{"feature": m["features"][i], "value": record[m["features"][i]], "push": round(float(contrib[i]), 3)} for i in order]


def band(p, threshold):
    if p >= threshold:
        return "HIGH"
    if p >= threshold - 0.2:
        return "MEDIUM"
    return "LOW"
