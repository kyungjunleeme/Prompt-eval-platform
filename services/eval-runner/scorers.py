from typing import Dict

def exact_score(pred: str, gold: str) -> float:
    return 1.0 if pred.strip() == (gold or "").strip() else 0.0

def rubric_score(pred: str, ref: str) -> Dict[str, float]:
    # placeholder rubric scorer
    return {"accuracy": 0.7, "policy": 1.0, "clarity": 0.8, "total": 0.82}
