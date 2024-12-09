from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config.settings import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base from models
from src.app.db.models import Base

# Create all tables
Base.metadata.create_all(bind=engine)
