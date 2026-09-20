from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from agent import create_scam_detector_agent, analyze_and_parse
from database import get_db, AnalysisRecord
from policy import evaluate_policy
from enrichment import count_duplicates, compute_risk_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = create_scam_detector_agent()

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/analyze")
def analyze(request: MessageRequest, db: Session = Depends(get_db)):
    result = analyze_and_parse(agent, request.message)
    policy_result = evaluate_policy(request.message)

    result["policy_risk"] = policy_result["policy_risk"]
    result["policy_rules_triggered"] = policy_result["policy_rules_triggered"]

    duplicate_count = count_duplicates(db, request.message)
    result["duplicate_count"] = duplicate_count

    risk_score = compute_risk_score(result.get("confidence"), result.get("policy_risk"), result.get("is_scam", False))
    result["risk_score"] = risk_score

    record = AnalysisRecord(
        message=request.message,
        is_scam=result.get("is_scam"),
        confidence=result.get("confidence"),
        red_flags=",".join(result.get("red_flags", [])),
        explanation=result.get("explanation", "")
    )
    db.add(record)
    db.commit()

    return result

@app.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    count = db.query(AnalysisRecord).delete()
    db.commit()
    return {"deleted": count}

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(20).all()
    return [
        {
            "id": r.id,
            "message": r.message,
            "is_scam": r.is_scam,
            "confidence": r.confidence,
            "red_flags": r.red_flags.split(",") if r.red_flags else [],
            "explanation": r.explanation,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]
