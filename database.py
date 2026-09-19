from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./scam_detector.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class AnalysisRecord(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    is_scam = Column(Boolean)
    confidence = Column(String)
    red_flags = Column(String)  # stored as comma-separated
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
