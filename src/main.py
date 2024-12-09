import logging
import logging.config
from fastapi import FastAPI
from src.app.api.pose_analysis import router as pose_router
from src.app.config.settings import settings

# Configure Logging
logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# Include API routers
app.include_router(pose_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Personal Trainer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)