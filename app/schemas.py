from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.customer


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
from typing import List, Dict

class SubscriptionPlanBase(BaseModel):
    name: str
    description: str
    permission_ids: List[int]
    usage_limits: Dict[str, int]  # { "api1": 100, "api2": 50 }

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanOut(SubscriptionPlanBase):
    id: int
    class Config:
        from_attributes = True  # For Pydantic v2 (instead of orm_mode)

from datetime import datetime

class UserSubscriptionBase(BaseModel):
    user_id: int
    plan_id: int

class UserSubscriptionCreate(UserSubscriptionBase):
    pass

class UserSubscriptionOut(UserSubscriptionBase):
    id: int
    start_date: datetime
    class Config:
        from_attributes = True

class APIUsageBase(BaseModel):
    user_id: int
    api_name: str

class APIUsageOut(APIUsageBase):
    count: int
    class Config:
        from_attributes = True