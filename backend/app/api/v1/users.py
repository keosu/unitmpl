"""
用户管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

# TODO: 实现用户相关API
@router.get("/")
async def list_users():
    """获取用户列表"""
    pass

@router.get("/{user_id}")  
async def get_user():
    """获取用户详情"""
    pass

@router.put("/{user_id}")
async def update_user():
    """更新用户信息"""
    pass