"""
认证相关API路由
包含登录、注册、token刷新等功能
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from datetime import datetime

from app.database import get_session
from app.models.user import User, UserRole, UserStatus
from app.schemas.auth import (
    UserLogin, UserRegister, TokenResponse, RefreshTokenRequest,
    PasswordChangeRequest, EmailVerificationRequest
)
from app.schemas.common import SuccessResponse
from app.utils.dependencies import (
    get_current_user, require_current_user, create_access_token, 
    create_refresh_token, verify_refresh_token
)


router = APIRouter()

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """加密密码"""
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
    """认证用户"""
    # 支持用户名或邮箱登录
    stmt = select(User).where(
        (User.username == username) | (User.email == username)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    """
    用户登录接口
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    """
    user = await authenticate_user(session, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户状态
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账号已被禁用"
        )
    
    # 更新登录统计
    user.last_login_at = datetime.utcnow()
    user.login_count += 1
    await session.commit()
    
    # 生成令牌
    token_data = create_access_token(user)
    refresh_token = create_refresh_token(user)
    
    return TokenResponse(
        access_token=token_data["access_token"],
        refresh_token=refresh_token,
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        expires_at=token_data["expires_at"],
        user_id=token_data["user_id"],
        username=token_data["username"],
        role=token_data["role"]
    )


@router.post("/register", response_model=SuccessResponse[TokenResponse], summary="用户注册")
async def register(
    register_data: UserRegister,
    session: AsyncSession = Depends(get_session)
):
    """用户注册接口"""
    # 检查密码确认
    if register_data.password != register_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码与确认密码不一致"
        )
    
    # 检查用户名是否已存在
    stmt = select(User).where(User.username == register_data.username)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    stmt = select(User).where(User.email == register_data.email)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建用户
    user = User(
        username=register_data.username,
        email=register_data.email,
        hashed_password=get_password_hash(register_data.password),
        full_name=register_data.full_name,
        phone=register_data.phone,
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    # 生成令牌
    token_data = create_access_token(user)
    refresh_token = create_refresh_token(user)
    
    token_response = TokenResponse(
        access_token=token_data["access_token"],
        refresh_token=refresh_token,
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        expires_at=token_data["expires_at"],
        user_id=token_data["user_id"],
        username=token_data["username"],
        role=token_data["role"]
    )
    
    return SuccessResponse.create(
        message="注册成功",
        data=token_response
    )


@router.post("/refresh", response_model=TokenResponse, summary="刷新令牌")
async def refresh_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session)
):
    """刷新访问令牌"""
    user = await verify_refresh_token(request.refresh_token, session)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    # 检查用户状态
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账号已被禁用"
        )
    
    # 生成新的访问令牌
    token_data = create_access_token(user)
    new_refresh_token = create_refresh_token(user)
    
    return TokenResponse(
        access_token=token_data["access_token"],
        refresh_token=new_refresh_token,
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        expires_at=token_data["expires_at"],
        user_id=token_data["user_id"],
        username=token_data["username"],
        role=token_data["role"]
    )


@router.post("/logout", response_model=SuccessResponse, summary="用户登出")
async def logout(
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """用户登出接口"""
    # TODO: 实现登出逻辑（可以将token加入黑名单）
    return SuccessResponse.create(message="登出成功")


@router.get("/me", summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(require_current_user)
):
    """获取当前登录用户的信息"""
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "full_name": current_user.full_name,
        "avatar_url": current_user.avatar_url,
        "bio": current_user.bio,
        "phone": current_user.phone,
        "is_email_verified": current_user.is_email_verified,
        "is_phone_verified": current_user.is_phone_verified,
        "status": current_user.status,
        "last_login_at": current_user.last_login_at,
        "login_count": current_user.login_count,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }

@router.post("/change-password", response_model=SuccessResponse, summary="修改密码")
async def change_password(
    request: PasswordChangeRequest,
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """修改密码"""
    # 检查当前密码
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 检查新密码确认
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码与确认密码不一致"
        )
    
    # 更新密码
    current_user.hashed_password = get_password_hash(request.new_password)
    current_user.updated_at = datetime.utcnow()
    
    await session.commit()
    
    return SuccessResponse.create(message="密码修改成功")