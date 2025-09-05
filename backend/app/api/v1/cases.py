"""
案例管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

# TODO: 实现案例相关API
@router.get("/")
async def list_cases():
    """获取案例列表"""
    pass

@router.post("/")
async def create_case():
    """创建新案例"""
    pass

@router.get("/{case_id}")
async def get_case():
    """获取案例详情"""
    pass