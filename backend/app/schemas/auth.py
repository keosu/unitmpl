"""
认证相关数据模型
包含登录、注册、令牌等
"""
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str = Field(min_length=3, max_length=50, description="用户名或邮箱")
    password: str = Field(min_length=6, max_length=100, description="密码")
    remember_me: bool = Field(default=False, description="记住我")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com",
                "password": "password123",
                "remember_me": False
            }
        }


class UserRegister(BaseModel):
    """用户注册请求"""
    username: str = Field(
        min_length=3, 
        max_length=50, 
        pattern="^[a-zA-Z0-9_-]+$",
        description="用户名"
    )
    email: EmailStr = Field(description="邮箱地址")
    password: str = Field(
        min_length=6, 
        max_length=100, 
        description="密码"
    )
    confirm_password: str = Field(
        min_length=6, 
        max_length=100, 
        description="确认密码"
    )
    full_name: Optional[str] = Field(
        default=None, 
        max_length=100, 
        description="真实姓名"
    )
    phone: Optional[str] = Field(
        default=None, 
        pattern="^1[3-9]\\d{9}$", 
        description="手机号码"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "newuser",
                "email": "user@example.com",
                "password": "password123",
                "confirm_password": "password123",
                "full_name": "张三",
                "phone": "13800138000"
            }
        }


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str = Field(description="访问令牌")
    refresh_token: str = Field(description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(description="过期时间（秒）")
    expires_at: datetime = Field(description="过期时间")
    user_id: str = Field(description="用户ID")
    username: str = Field(description="用户名")
    role: str = Field(description="用户角色")


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str = Field(description="刷新令牌")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            }
        }


class PasswordResetRequest(BaseModel):
    """密码重置请求"""
    email: EmailStr = Field(description="邮箱地址")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class PasswordResetConfirm(BaseModel):
    """密码重置确认"""
    reset_token: str = Field(description="重置令牌")
    new_password: str = Field(
        min_length=6, 
        max_length=100, 
        description="新密码"
    )
    confirm_password: str = Field(
        min_length=6, 
        max_length=100, 
        description="确认新密码"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "reset_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        }


class PasswordChangeRequest(BaseModel):
    """修改密码请求"""
    current_password: str = Field(description="当前密码")
    new_password: str = Field(
        min_length=6, 
        max_length=100, 
        description="新密码"
    )
    confirm_password: str = Field(
        min_length=6, 
        max_length=100, 
        description="确认新密码"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        }


class EmailVerificationRequest(BaseModel):
    """邮箱验证请求"""
    verification_token: str = Field(description="验证令牌")
    
    class Config:
        json_schema_extra = {
            "example": {
                "verification_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            }
        }


class ResendVerificationRequest(BaseModel):
    """重发验证邮件请求"""
    email: EmailStr = Field(description="邮箱地址")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }