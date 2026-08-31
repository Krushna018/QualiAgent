
from __future__ import annotations
from collections import defaultdict
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, classification_report

def evaluate_binary(labels, predictions):
    p, r, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="binary", zero_division=0
    )
    return {"precision": p, "recall": r, "f1": f1}

def evaluate_multiclass(labels, predictions):
    return classification_report(labels, predictions, output_dict=True, zero_division=0)

def agreement_rate(a, b):
    if len(a) != len(b):
        raise ValueError("Sequences must have equal length")
    return sum(x == y for x, y in zip(a,b)) / max(len(a), 1)
