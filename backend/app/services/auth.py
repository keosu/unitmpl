"""
认证服务
处理用户认证、授权相关的业务逻辑
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import User
from app.utils.security import verify_password, create_access_token, create_refresh_token
from app.utils.exceptions import InvalidCredentialsError


class AuthService:
    """认证服务类"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def authenticate_user(
        self, 
        username: str, 
        password: str
    ) -> Optional[User]:
        """验证用户凭据"""
        # 查询用户（支持用户名或邮箱登录）
        statement = select(User).where(
            (User.username == username) | (User.email == username)
        )
        result = await self.session.exec(statement)
        user = result.first()
        
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        # 更新登录统计
        user.last_login_at = datetime.utcnow()
        user.login_count += 1
        
        # 保存更新
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    async def create_access_token(self, user_id: str) -> str:
        """创建访问令牌"""
        data = {"sub": str(user_id), "type": "access"}
        return create_access_token(data)
    
    async def create_refresh_token(self, user_id: str) -> str:
        """创建刷新令牌"""
        return create_refresh_token(str(user_id))
    
    async def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None
    ) -> User:
        """注册新用户"""
        # TODO: 实现用户注册逻辑
        # 1. 检查用户名和邮箱是否已存在
        # 2. 创建新用户
        # 3. 发送验证邮件
        pass
    
    async def verify_email(self, token: str) -> bool:
        """验证邮箱"""
        # TODO: 实现邮箱验证逻辑
        pass
    
    async def reset_password(self, email: str) -> bool:
        """重置密码"""
        # TODO: 实现密码重置逻辑
        pass