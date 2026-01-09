from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import crops, animals, flowers, statistics

# 数据库初始化（开发环境）
if settings.AUTO_CREATE_TABLES:
    from app.db.init_db import init_db
    init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="大噜农场展示系统 API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(crops.router, prefix=f"{settings.API_V1_PREFIX}/crops", tags=["粮食管理"])
app.include_router(animals.router, prefix=f"{settings.API_V1_PREFIX}/animals", tags=["动物管理"])
app.include_router(flowers.router, prefix=f"{settings.API_V1_PREFIX}/flowers", tags=["花卉管理"])
app.include_router(statistics.router, prefix=f"{settings.API_V1_PREFIX}/statistics", tags=["统计数据"])


@app.get("/")
def root():
    """根路径"""
    return {
        "message": "大噜农场展示系统 API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs",
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"}
