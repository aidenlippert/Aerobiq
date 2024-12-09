from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    exercises = relationship("Exercise", back_populates="owner")

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    exercise_type = Column(String(50), nullable=False)
    duration = Column(Float, nullable=False)  # in minutes
    calories_burned = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="exercises")