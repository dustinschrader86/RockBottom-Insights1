from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, date
import httpx
import hashlib
import random
import re
from typing import Optional, Dict, Any

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
    role = Column(String, default="tester")
    tier = Column(String, default="Free")
    api_key = Column(String, unique=True)
    daily_limit = Column(Integer, default=3)
    scans_today = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class ScanRequest(BaseModel):
    address: Optional[str] = None
    text: Optional[str] = None
    chain: str = "ETH"

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
        raise HTTPException(status_code=429, detail="Free tier: 3 scans/day reached")
    user.scans_today += 1
    db.commit()

# Real Blockchain functions (shortened for deploy)
async def fetch_eth_data(address: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"https://api.etherscan.io/api?module=account&action=balance&address={address}")
            data = resp.json()
            balance = int(data.get("result", 0)) / 1e18
            return {"balance_eth": round(balance, 4)}
    except:
        return {"error": "Fetch failed"}

# ... (contract scan and other functions can be added later if needed)

@app.post("/scan-wallet")
async def scan_wallet(request: ScanRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    check_rate_limit(user, db)
    data = await fetch_eth_data(request.address or "")
    return {"address": request.address, "data": data, "risk_score": 6.5}

@app.post("/admin/create-user")
def create_user(username: str, password: str,