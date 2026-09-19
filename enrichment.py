from sqlalchemy.orm import Session
from database import AnalysisRecord

def count_duplicates(db: Session, message: str, exclude_id=None) -> int:
    query = db.query(AnalysisRecord).filter(AnalysisRecord.message == message.strip())
    if exclude_id:
        query = query.filter(AnalysisRecord.id != exclude_id)
    return query.count()

def compute_risk_score(confidence: str, policy_risk: str, is_scam: bool) -> int:
    if not is_scam:
        base = {"high": 5, "medium": 15, "low": 25, "unknown": 20}.get((confidence or "unknown").lower(), 20)
    else:
        base = {"high": 70, "medium": 55, "low": 40, "unknown": 50}.get((confidence or "unknown").lower(), 50)

    if policy_risk == "high":
        base += 25
    elif policy_risk == "low" and is_scam:
        base -= 15

    return max(0, min(100, base))
