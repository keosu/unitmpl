"""
律师数据模型
包含律师专业信息、资质认证等
"""
from enum import Enum
from typing import Optional, List
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String, Text, Numeric, Date
from sqlalchemy.dialects.postgresql import ARRAY
from .base import BaseModel


class LawyerStatus(str, Enum):
    """律师状态"""
    PENDING = "pending"      # 待审核
    APPROVED = "approved"    # 已通过
    REJECTED = "rejected"    # 已拒绝
    SUSPENDED = "suspended"  # 暂停执业


class LawyerLevel(str, Enum):
    """律师级别"""
    JUNIOR = "junior"        # 初级律师
    INTERMEDIATE = "intermediate"  # 中级律师
    SENIOR = "senior"        # 高级律师
    PARTNER = "partner"      # 合伙人


class Lawyer(BaseModel, table=True):
    """律师模型"""
    __tablename__ = "lawyers"
    
    # 关联用户
    user_id: str = Field(foreign_key="users.id", unique=True)
    
    # 执业信息
    license_number: str = Field(
        index=True,
        unique=True)
    bar_association: str = Field()
    practice_start_date: date = Field()
    
    # 专业信息
    law_firm: Optional[str] = Field(
        default=None)
    position: Optional[str] = Field(
        default=None)
    level: LawyerLevel = Field(default=LawyerLevel.JUNIOR)
    
    # 专业领域
    specialties: Optional[str] = Field(
        default=None,
        description="专业领域，JSON字符串格式"
    )
    
    # 专业描述
    professional_summary: Optional[str] = Field(
        default=None)
    education_background: Optional[str] = Field(
        default=None)
    
    # 执业统计
    cases_handled: int = Field(default=0)
    success_rate: float = Field(default=0.0)
    average_rating: float = Field(default=0.0)
    total_reviews: int = Field(default=0)
    
    # 收费标准
    hourly_rate: Optional[float] = Field(
        default=None)
    consultation_fee: Optional[float] = Field(
        default=None)
    
    # 状态
    status: LawyerStatus = Field(default=LawyerStatus.PENDING)
    verified_at: Optional[datetime] = Field(default=None)
    
    # 可用性
    is_available: bool = Field(default=True)
    accepts_new_cases: bool = Field(default=True)
    
    # 关联关系
    user: "User" = Relationship(back_populates="lawyer_profile")
    certifications: List["LawyerCertification"] = Relationship(back_populates="lawyer")
    handled_cases: List["Case"] = Relationship(
        back_populates="lawyer",
        sa_relationship_kwargs={"foreign_keys": "Case.lawyer_id"}
    )
    
    def get_experience_years(self) -> int:
        """计算执业年限"""
        today = date.today()
        return (today - self.practice_start_date).days // 365


class LawyerSpecialty(BaseModel, table=True):
    """律师专业领域"""
    __tablename__ = "lawyer_specialties"
    
    name: str = Field(
        index=True,
        unique=True)
    name_en: Optional[str] = Field(
        default=None)
    description: Optional[str] = Field(
        default=None)
    parent_id: Optional[str] = Field(
        default=None,
        foreign_key="lawyer_specialties.id"
    )
    
    # 层级关系
    parent: Optional["LawyerSpecialty"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "LawyerSpecialty.id"}
    )
    children: List["LawyerSpecialty"] = Relationship(back_populates="parent")


class LawyerCertification(BaseModel, table=True):
    """律师认证资质"""
    __tablename__ = "lawyer_certifications"
    
    lawyer_id: str = Field(foreign_key="lawyers.id")
    
    # 证书信息
    name: str = Field()
    issuing_authority: str = Field()
    certificate_number: Optional[str] = Field(
        default=None)
    
    # 时间信息
    issued_date: date = Field()
    expiry_date: Optional[date] = Field(
        default=None)
    
    # 证书文件
    certificate_url: Optional[str] = Field(
        default=None)
    
    # 验证状态
    is_verified: bool = Field(default=False)
    verified_at: Optional[datetime] = Field(default=None)
    verified_by: Optional[str] = Field(
        default=None,
        foreign_key="users.id"
    )
    
    # 关联关系
    lawyer: Lawyer = Relationship(back_populates="certifications")
    verifier: Optional["User"] = Relationship()
    
    def is_expired(self) -> bool:
        """判断证书是否过期"""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date


class LawyerReview(BaseModel, table=True):
    """律师评价"""
    __tablename__ = "lawyer_reviews"
    
    lawyer_id: str = Field(foreign_key="lawyers.id")
    client_id: str = Field(foreign_key="users.id")
    case_id: Optional[str] = Field(
        default=None,
        foreign_key="cases.id"
    )
    
    # 评分 (1-5)
    rating: int = Field(ge=1, le=5)
    
    # 评价内容
    title: Optional[str] = Field(
        default=None)
    content: Optional[str] = Field(
        default=None)
    
    # 评价维度
    professionalism_rating: Optional[int] = Field(default=None, ge=1, le=5)
    communication_rating: Optional[int] = Field(default=None, ge=1, le=5)
    efficiency_rating: Optional[int] = Field(default=None, ge=1, le=5)
    
    # 状态
    is_anonymous: bool = Field(default=False)
    is_published: bool = Field(default=True)
    
    # 关联关系
    lawyer: Lawyer = Relationship()
    client: "User" = Relationship()
    case: Optional["Case"] = Relationship()