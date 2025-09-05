"""
用户数据模型
包含用户基本信息、角色权限等
"""
from enum import Enum
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String, Text
from .base import BaseModel


class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"        # 管理员
    LAWYER = "lawyer"      # 律师
    USER = "user"          # 普通用户


class UserStatus(str, Enum):
    """用户状态枚举"""
    ACTIVE = "active"      # 正常
    INACTIVE = "inactive"  # 未激活
    SUSPENDED = "suspended" # 停用
    BANNED = "banned"      # 封禁


class User(BaseModel, table=True):
    """用户模型"""
    __tablename__ = "users"
    
    # 基本信息
    username: str = Field(
        index=True, 
        unique=True, 
        min_length=3, 
        max_length=50
    )
    email: str = Field(
        index=True, 
        unique=True
    )
    phone: Optional[str] = Field(
        default=None,
        index=True
    )
    
    # 认证信息
    hashed_password: str = Field()
    is_email_verified: bool = Field(default=False)
    is_phone_verified: bool = Field(default=False)
    
    # 个人资料
    full_name: Optional[str] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    
    # 系统字段
    role: UserRole = Field(default=UserRole.USER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    
    # 登录统计
    last_login_at: Optional[datetime] = Field(default=None)
    login_count: int = Field(default=0)
    
    # 关联关系
    lawyer_profile: Optional["Lawyer"] = Relationship(back_populates="user")
    sent_messages: List["ChatMessage"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "ChatMessage.sender_id"}
    )
    owned_cases: List["Case"] = Relationship(
        back_populates="client",
        sa_relationship_kwargs={"foreign_keys": "Case.client_id"}
    )
    
    def is_lawyer(self) -> bool:
        """判断是否为律师"""
        return self.role == UserRole.LAWYER
    
    def is_admin(self) -> bool:
        """判断是否为管理员"""
        return self.role == UserRole.ADMIN
    
    def can_access_admin(self) -> bool:
        """判断是否可以访问管理功能"""
        return self.role in [UserRole.ADMIN, UserRole.LAWYER]


class UserPreferences(BaseModel, table=True):
    """用户偏好设置"""
    __tablename__ = "user_preferences"
    
    user_id: str = Field(foreign_key="users.id", unique=True)
    
    # 界面设置
    theme: str = Field(default="light")  # light, dark, auto
    language: str = Field(default="zh-cn")  # zh-cn, en-us
    
    # 通知设置
    email_notifications: bool = Field(default=True)
    sms_notifications: bool = Field(default=False)
    push_notifications: bool = Field(default=True)
    
    # 隐私设置
    profile_public: bool = Field(default=False)
    show_online_status: bool = Field(default=True)
    
    # 关联关系
    user: User = Relationship()


class UserSession(BaseModel, table=True):
    """用户会话记录"""
    __tablename__ = "user_sessions"
    
    user_id: str = Field(foreign_key="users.id", index=True)
    session_token: str = Field(index=True, unique=True)
    device_info: Optional[str] = Field(default=None)
    ip_address: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(default=None)
    expires_at: datetime = Field()
    
    # 关联关系
    user: User = Relationship()