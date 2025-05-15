from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/usage-logs", tags=["Usage Logs"])

# Track API call
@router.post("/", response_model=schemas.APIUsageOut)
def track_usage(usage: schemas.APIUsageBase, db: Session = Depends(get_db)):
    record = db.query(models.APIUsage).filter_by(user_id=usage.user_id, api_name=usage.api_name).first()
    if record:
        record.count += 1
    else:
        record = models.APIUsage(**usage.dict(), count=1)
        db.add(record)
    db.commit()
    db.refresh(record)
    return record

# Check limit
@router.get("/check/{user_id}/{api_name}")
def check_usage_limit(user_id: int, api_name: str, db: Session = Depends(get_db)):
    # Get user subscription
    subscription = db.query(models.UserSubscription).filter_by(user_id=user_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found.")
    
    # Get usage limits from plan
    limits = subscription.plan.usage_limits
    max_calls = limits.get(api_name)
    if max_calls is None:
        raise HTTPException(status_code=403, detail="API not allowed for this plan.")
    
    # Get usage count
    record = db.query(models.APIUsage).filter_by(user_id=user_id, api_name=api_name).first()
    count = record.count if record else 0
    
    if count >= max_calls:
        raise HTTPException(status_code=429, detail="API limit exceeded.")

    return {"message": "Allowed", "usage": count, "remaining": max_calls - count}
