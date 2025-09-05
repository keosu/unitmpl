"""
律师管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

# TODO: 实现律师相关API
@router.get("/")
async def list_lawyers():
    """获取律师列表"""
    pass

@router.get("/{lawyer_id}")
async def get_lawyer():
    """获取律师详情"""
    pass

@router.post("/")
async def create_lawyer_profile():
    """创建律师档案"""
    pass