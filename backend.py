# In User model, add tier
class User(Base):
    # ... existing fields ...
    tier = Column(String, default="Free")  # Free, Pro-Tier, Ultra-Tier

# Update rate limit check
def check_rate_limit(user: User, db: Session):
    today = date.today()
    if user.last_reset.date() < today:
        user.scans_today = 0
        user.last_reset = datetime.utcnow()
        db.commit()
    
    if user.tier == "Free" and user.scans_today >= 3:
        raise HTTPException(status_code=429, detail="Free tier limit: 3 scans/day")
    # Pro and Ultra are unlimited
    user.scans_today += 1
    db.commit()
    return True