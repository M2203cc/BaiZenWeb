from fastapi import FastAPI
from .euka_api_video import router as video_router

app = FastAPI()
app.include_router(video_router, prefix="/api/content-analysis") 