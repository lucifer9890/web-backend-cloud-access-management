from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.auth import get_current_user
from app.database import get_db
from app import models
from app.routes.usage_logs import check_usage_limit, track_usage

router = APIRouter(prefix="/cloud", tags=["Cloud APIs"])

def check_access(user: models.User, api_name: str, db: Session):
    # Verify user has a subscription
    sub = db.query(models.UserSubscription).filter_by(user_id=user.id).first()
    if not sub:
        raise HTTPException(status_code=403, detail="No subscription")

    # Check permission
    if api_name not in sub.plan.usage_limits:
        raise HTTPException(status_code=403, detail="API not allowed")

    # Check usage limit
    limits = sub.plan.usage_limits
    usage = db.query(models.APIUsage).filter_by(user_id=user.id, api_name=api_name).first()
    count = usage.count if usage else 0

    if count >= limits[api_name]:
        raise HTTPException(status_code=429, detail="API limit exceeded")

    # All checks passed, increment usage
    if usage:
        usage.count += 1
    else:
        usage = models.APIUsage(user_id=user.id, api_name=api_name, count=1)
        db.add(usage)
    db.commit()


@router.get("/api{n}")
def dummy_api(n: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_name = f"api{n}"
    if n < 1 or n > 6:
        raise HTTPException(status_code=404, detail="API not found")
    check_access(user, api_name, db)
    return {"message": f"You have accessed {api_name}"}
