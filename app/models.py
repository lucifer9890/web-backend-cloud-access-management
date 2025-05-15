from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
import enum


# Role Enum
class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer)

    # Later relationships can be added here
    # subscription = relationship("Subscription", back_populates="user")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    endpoint = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, default="general")

from sqlalchemy import JSON

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String, default="general")

    # Store a list of allowed permission IDs
    permission_ids = Column(JSON, nullable=False)

    # Usage limits like { "api1": 100, "api2": 50 }
    usage_limits = Column(JSON, nullable=False)

from sqlalchemy import DateTime
from datetime import datetime

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    plan = relationship("SubscriptionPlan")

class APIUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    api_name = Column(String, nullable=False)
    count = Column(Integer, default=0)

    user = relationship("User")
