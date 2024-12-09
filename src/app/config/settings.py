from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI Personal Trainer"
    THRESHOLD_SPEED: float = 1.5
    THRESHOLD_SYMMETRY: float = 10.0
    DATABASE_URL: str = "sqlite:///./ai_trainer.db"
    LOGGING_LEVEL: str = "INFO"
    FEEDBACK_TEMPLATE_PATH: str = "src/ai_coaching/templates/feedback.json"

    class Config:
        env_file = ".env"

settings = Settings()