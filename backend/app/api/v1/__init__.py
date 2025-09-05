"""
API v1 路由集合
统一管理所有v1版本的API路由
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .lawyers import router as lawyers_router
from .cases import router as cases_router
from .chat import router as chat_router


api_router = APIRouter()

# 注册所有路由
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["认证"]
)

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["用户管理"]
)

api_router.include_router(
    lawyers_router,
    prefix="/lawyers",
    tags=["律师管理"]
)

api_router.include_router(
    cases_router,
    prefix="/cases",
    tags=["案例管理"]
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["聊天服务"]
)