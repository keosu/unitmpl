"""
FastAPI 应用主入口
包含应用配置、中间件、路由注册等
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import time
import logging

from app.config import settings
from app.database import create_db_and_tables, close_db
from app.utils.exceptions import setup_exception_handlers
from app.api.v1 import api_router


# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动法律咨询应用API服务...")
    
    # 创建数据库表
    await create_db_and_tables()
    logger.info("✅ 数据库初始化完成")
    
    yield
    
    # 关闭时执行
    logger.info("🔄 正在关闭API服务...")
    await close_db()
    logger.info("✅ 数据库连接已关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="专业的法律咨询服务平台API",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan
)


# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加可信主机中间件（生产环境）
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.yourdomain.com", "localhost"]
    )


# 请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间到响应头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:.4f}")
    return response


# 静态文件服务（用于文件上传）
app.mount("/static", StaticFiles(directory="uploads"), name="static")


# 注册API路由
app.include_router(api_router, prefix="/api/v1")


# 设置异常处理器
setup_exception_handlers(app)


# 健康检查端点
@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "timestamp": time.time()
    }


# 根路径
@app.get("/", tags=["首页"])
async def root():
    """API根路径"""
    return {
        "message": f"欢迎使用{settings.app_name}",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else "文档已禁用",
        "health_check": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )