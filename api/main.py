from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.euka_api_video import router as video_router
from api.euka_api_brand import router as brand_router

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(video_router, prefix="/api/content-analysis")
app.include_router(brand_router, prefix="/api/content-analysis") 