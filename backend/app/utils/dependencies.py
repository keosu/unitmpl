"""
依赖注入工具
包含认证、权限检查等通用依赖
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from datetime import datetime

from app.database import get_session
from app.models.user import User, UserRole
from app.config import settings

# JWT认证
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> Optional[User]:
    """
    获取当前登录用户
    支持可选认证，如果没有token则返回None
    """
    if not credentials:
        return None
    
    try:
        # 解码JWT token
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        # 从数据库获取用户
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        return user
        
    except jwt.PyJWTError:
        return None


async def require_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    获取当前登录用户（必须登录）
    如果未登录或token无效，抛出401错误
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证信息",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # 解码JWT token
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证信息",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # 检查token是否过期
        exp = payload.get("exp")
        if exp is None or datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="认证信息已过期",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # 从数据库获取用户
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证信息",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_admin(
    current_user: User = Depends(require_current_user)
) -> User:
    """
    要求管理员权限
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


async def require_lawyer(
    current_user: User = Depends(require_current_user)
) -> User:
    """
    要求律师权限
    """
    if not current_user.is_lawyer():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要律师权限"
        )
    return current_user


async def require_admin_or_lawyer(
    current_user: User = Depends(require_current_user)
) -> User:
    """
    要求管理员或律师权限
    """
    if not current_user.can_access_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员或律师权限"
        )
    return current_user


def create_access_token(user: User) -> dict:
    """
    创建访问令牌
    """
    from datetime import timedelta
    import uuid
    
    # 计算过期时间
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    # 创建JWT payload
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role.value,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp(),
        "jti": str(uuid.uuid4())  # JWT ID
    }
    
    # 生成token
    access_token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "expires_at": expire,
        "user_id": str(user.id),
        "username": user.username,
        "role": user.role.value
    }


def create_refresh_token(user: User) -> str:
    """
    创建刷新令牌
    """
    from datetime import timedelta
    import uuid
    
    # 计算过期时间
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    # 创建JWT payload
    payload = {
        "sub": str(user.id),
        "type": "refresh",
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp(),
        "jti": str(uuid.uuid4())
    }
    
    # 生成token
    refresh_token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return refresh_token


async def verify_refresh_token(
    refresh_token: str,
    session: AsyncSession
) -> Optional[User]:
    """
    验证刷新令牌并返回用户
    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        # 检查token类型
        if payload.get("type") != "refresh":
            return None
            
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        # 从数据库获取用户
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        return user
        
    except jwt.PyJWTError:
        return None