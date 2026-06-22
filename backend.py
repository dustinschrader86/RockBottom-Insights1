from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, date
import hashlib
import random
from typing import Optional

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./rockbottom.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    tier = Column(String, default="Free")
    api_key = Column(String, unique=True)
    daily_limit = Column(Integer, default=3)
    scans_today = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class ScanRequest(BaseModel):
    address: Optional[str] = None

app = FastAPI(title="Rockbottom Insights")

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user(credentials=Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user = db.query(User).filter(User.api_key == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user

def check_rate_limit(user: User, db: Session):
    today = date.today()
    if user.last_reset.date() < today:
        user.scans_today = 0
        user.last_reset = datetime.utcnow()
        db.commit()
    
    if user.tier == "Free" and user.scans_today >= 3:
        raise HTTPException(status_code=429, detail="Free tier limit reached (3 scans/day)")
    user.scans_today += 1
    db.commit()

@app.post("/scan-wallet")
def scan_wallet(request: ScanRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    check_rate_limit(user, db)
    return {"address": request.address, "risk_score": 6.5, "message": "Scan complete"}

@app.post("/admin/create-user")
def create_user(username: str, password: str, tier: str = "Pro-Tier", db: Session = Depends(get_db)):
    api_key = f"rb-{username}-{random.randint(1000,9999)}"
    new_user = User(
        username=username,
        hashed_password=hash_password(password),
        tier=tier,
        api_key=api_key
    )
    db.add(new_user)
    db.commit()
    return {"api_key": api_key}

def seed_admin():
    db = SessionLocal()
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(username="admin", hashed_password=hash_password("rockbottom2026"), tier="Ultra-Tier", api_key="rb-admin-2026")
        db.add(admin)
        db.commit()
        print("Admin created")
    db.close()

seed_admin()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)