"""
用户相关数据模型
包含用户信息、偏好设置等
"""
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from ..models.user import UserRole, UserStatus


class UserCreate(BaseModel):
    """创建用户请求"""
    username: str = Field(min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(description="邮箱地址")
    password: str = Field(min_length=6, max_length=100, description="密码")
    full_name: Optional[str] = Field(default=None, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(default=None, description="手机号码")
    role: UserRole = Field(default=UserRole.USER, description="用户角色")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "newuser",
                "email": "user@example.com",
                "password": "password123",
                "full_name": "张三",
                "phone": "13800138000",
                "role": "user"
            }
        }


class UserUpdate(BaseModel):
    """更新用户信息请求"""
    full_name: Optional[str] = Field(default=None, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(default=None, description="手机号码")
    bio: Optional[str] = Field(default=None, max_length=500, description="个人简介")
    avatar_url: Optional[str] = Field(default=None, description="头像URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "张三",
                "phone": "13800138000",
                "bio": "这是我的个人简介",
                "avatar_url": "https://example.com/avatar.jpg"
            }
        }


class UserResponse(BaseModel):
    """用户信息响应"""
    id: str = Field(description="用户ID")
    username: str = Field(description="用户名")
    email: str = Field(description="邮箱地址")
    full_name: Optional[str] = Field(description="真实姓名")
    phone: Optional[str] = Field(description="手机号码")
    avatar_url: Optional[str] = Field(description="头像URL")
    bio: Optional[str] = Field(description="个人简介")
    role: UserRole = Field(description="用户角色")
    status: UserStatus = Field(description="用户状态")
    is_email_verified: bool = Field(description="邮箱是否已验证")
    is_phone_verified: bool = Field(description="手机是否已验证")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    last_login_at: Optional[datetime] = Field(description="最后登录时间")
    login_count: int = Field(description="登录次数")
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """用户详细资料"""
    id: str = Field(description="用户ID")
    username: str = Field(description="用户名")
    email: str = Field(description="邮箱地址")
    full_name: Optional[str] = Field(description="真实姓名")
    phone: Optional[str] = Field(description="手机号码")
    avatar_url: Optional[str] = Field(description="头像URL")
    bio: Optional[str] = Field(description="个人简介")
    role: UserRole = Field(description="用户角色")
    status: UserStatus = Field(description="用户状态")
    is_email_verified: bool = Field(description="邮箱是否已验证")
    is_phone_verified: bool = Field(description="手机是否已验证")
    created_at: datetime = Field(description="创建时间")
    last_login_at: Optional[datetime] = Field(description="最后登录时间")
    # 扩展信息
    preferences: Optional["UserPreferencesResponse"] = Field(description="用户偏好")
    is_lawyer: bool = Field(description="是否为律师")
    lawyer_profile: Optional["LawyerResponse"] = Field(description="律师资料")
    
    class Config:
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    """更新用户偏好请求"""
    theme: Optional[str] = Field(default=None, description="主题设置")
    language: Optional[str] = Field(default=None, description="语言设置")
    email_notifications: Optional[bool] = Field(default=None, description="邮件通知")
    sms_notifications: Optional[bool] = Field(default=None, description="短信通知")
    push_notifications: Optional[bool] = Field(default=None, description="推送通知")
    profile_public: Optional[bool] = Field(default=None, description="公开资料")
    show_online_status: Optional[bool] = Field(default=None, description="显示在线状态")
    
    class Config:
        json_schema_extra = {
            "example": {
                "theme": "dark",
                "language": "zh-cn",
                "email_notifications": True,
                "sms_notifications": False,
                "push_notifications": True,
                "profile_public": False,
                "show_online_status": True
            }
        }


class UserPreferencesResponse(BaseModel):
    """用户偏好响应"""
    theme: str = Field(description="主题设置")
    language: str = Field(description="语言设置")
    email_notifications: bool = Field(description="邮件通知")
    sms_notifications: bool = Field(description="短信通知")
    push_notifications: bool = Field(description="推送通知")
    profile_public: bool = Field(description="公开资料")
    show_online_status: bool = Field(description="显示在线状态")
    
    class Config:
        from_attributes = True


class UserListItem(BaseModel):
    """用户列表项"""
    id: str = Field(description="用户ID")
    username: str = Field(description="用户名")
    full_name: Optional[str] = Field(description="真实姓名")
    avatar_url: Optional[str] = Field(description="头像URL")
    role: UserRole = Field(description="用户角色")
    status: UserStatus = Field(description="用户状态")
    created_at: datetime = Field(description="创建时间")
    last_login_at: Optional[datetime] = Field(description="最后登录时间")
    
    class Config:
        from_attributes = True


class UserSearchParams(BaseModel):
    """用户搜索参数"""
    q: Optional[str] = Field(default=None, description="搜索关键词")
    role: Optional[UserRole] = Field(default=None, description="用户角色")
    status: Optional[UserStatus] = Field(default=None, description="用户状态")
    is_verified: Optional[bool] = Field(default=None, description="是否已验证")
    sort_by: str = Field(default="created_at", description="排序字段")
    sort_order: str = Field(default="desc", description="排序方向")


# 避免循环导入，在文件末尾导入
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .lawyer import LawyerResponse