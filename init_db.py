from app.database import engine
from app.models import Base

# Create all tables using the synchronous engine
Base.metadata.create_all(bind=engine)

print("✅ Database initialized successfully.")
