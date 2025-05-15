from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel
from app.routes.auth import admin_required

router = APIRouter(prefix="/api-access", tags=["API Access"])

# Pydantic Schema
class PermissionCreate(BaseModel):
    name: str
    endpoint: str
    description: str

class PermissionOut(PermissionCreate):
    id: int
    class Config:
        orm_mode = True

# Create Permission
@router.post("/", response_model=PermissionOut)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db), user: models.User = Depends(admin_required)):
    existing = db.query(models.Permission).filter(models.Permission.name == permission.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission name already exists.")
    new_perm = models.Permission(**permission.dict())
    db.add(new_perm)
    db.commit()
    db.refresh(new_perm)
    return new_perm

# Update Permission
@router.put("/{permission_id}", response_model=PermissionOut)
def update_permission(permission_id: int, data: PermissionCreate, db: Session = Depends(get_db), user: models.User = Depends(admin_required)):
    perm = db.query(models.Permission).get(permission_id)
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found.")
    for key, value in data.dict().items():
        setattr(perm, key, value)
    db.commit()
    db.refresh(perm)
    return perm

# Delete Permission
@router.delete("/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db),user: models.User = Depends(admin_required)):
    perm = db.query(models.Permission).get(permission_id)
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found.")
    db.delete(perm)
    db.commit()
    return {"message": "Permission deleted successfully"}


@router.get("/list")
def list_permissions(db: Session = Depends(get_db)):
    return db.query(models.Permission).all()
