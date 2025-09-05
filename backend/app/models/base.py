"""
基础数据模型
包含所有模型的公共字段和方法
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import uuid


class BaseModel(SQLModel):
    """基础模型类，包含通用字段"""
    
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)
    
    class Config:
        """数据模型配置"""
        from_attributes = True