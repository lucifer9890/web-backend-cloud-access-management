from fastapi import FastAPI
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Cloud Service Access Management System")

# Import routers (all using updated filenames)
from app.routes.subscription_plans import router as subscription_plans_router
from app.routes.api_access import router as api_access_router
from app.routes.user_subscriptions import router as user_subscriptions_router
from app.routes.usage_logs import router as usage_logs_router
from app.routes.auth import router as auth_router
from app.routes.cloud_services import router as cloud_services_router

# Register routers
app.include_router(subscription_plans_router)
app.include_router(api_access_router)
app.include_router(user_subscriptions_router)
app.include_router(usage_logs_router)
app.include_router(auth_router)
app.include_router(cloud_services_router)

