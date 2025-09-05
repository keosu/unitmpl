"""
案例数据模型
包含法律案例、文档、状态跟踪等
"""
from enum import Enum
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String, Text, Numeric, Date
from sqlalchemy.dialects.postgresql import ARRAY
from .base import BaseModel


class CaseStatus(str, Enum):
    """案例状态"""
    DRAFT = "draft"              # 草稿
    SUBMITTED = "submitted"      # 已提交
    UNDER_REVIEW = "under_review" # 审核中
    ASSIGNED = "assigned"        # 已分配律师
    IN_PROGRESS = "in_progress"  # 进行中
    WAITING_CLIENT = "waiting_client"  # 等待客户
    WAITING_COURT = "waiting_court"    # 等待法院
    COMPLETED = "completed"      # 已完成
    CLOSED = "closed"           # 已关闭
    CANCELLED = "cancelled"     # 已取消


class CasePriority(str, Enum):
    """案例优先级"""
    LOW = "low"           # 低
    MEDIUM = "medium"     # 中
    HIGH = "high"         # 高
    URGENT = "urgent"     # 紧急


class CaseType(str, Enum):
    """案例类型"""
    CIVIL = "civil"                    # 民事
    CRIMINAL = "criminal"              # 刑事
    ADMINISTRATIVE = "administrative"   # 行政
    ECONOMIC = "economic"              # 经济
    LABOR = "labor"                    # 劳动
    FAMILY = "family"                  # 婚姻家庭
    PROPERTY = "property"              # 房产
    INTELLECTUAL = "intellectual"       # 知识产权
    ENVIRONMENTAL = "environmental"     # 环境
    OTHER = "other"                    # 其他


class Case(BaseModel, table=True):
    """案例模型"""
    __tablename__ = "cases"
    
    # 基本信息
    case_number: str = Field(
        index=True,
        unique=True)
    title: str = Field()
    description: str = Field()
    
    # 分类信息
    case_type: CaseType = Field(index=True)
    category: Optional[str] = Field(
        default=None)
    tags: Optional[str] = Field(
        default=None,
        description="标签，JSON字符串格式"
    )
    
    # 关联人员
    client_id: str = Field(foreign_key="users.id", index=True)
    lawyer_id: Optional[str] = Field(
        default=None,
        foreign_key="lawyers.id",
        index=True
    )
    
    # 状态信息
    status: CaseStatus = Field(default=CaseStatus.DRAFT, index=True)
    priority: CasePriority = Field(default=CasePriority.MEDIUM)
    
    # 时间信息
    incident_date: Optional[date] = Field(
        default=None)
    deadline: Optional[date] = Field(
        default=None)
    assigned_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    
    # 费用信息
    estimated_fee: Optional[Decimal] = Field(
        default=None)
    actual_fee: Optional[Decimal] = Field(
        default=None)
    consultation_fee: Optional[Decimal] = Field(
        default=None)
    
    # 案例详情
    legal_issues: Optional[str] = Field(
        default=None)
    client_goals: Optional[str] = Field(
        default=None)
    case_notes: Optional[str] = Field(
        default=None)
    
    # 结果信息
    outcome: Optional[str] = Field(
        default=None)
    is_successful: Optional[bool] = Field(default=None)
    
    # 隐私设置
    is_confidential: bool = Field(default=True)
    is_public: bool = Field(default=False)
    
    # 关联关系
    client: "User" = Relationship()
    lawyer: Optional["Lawyer"] = Relationship()
    documents: List["CaseDocument"] = Relationship(back_populates="case")
    updates: List["CaseUpdate"] = Relationship(back_populates="case")
    chat_room: Optional["ChatRoom"] = Relationship(back_populates="case")
    
    def get_duration_days(self) -> Optional[int]:
        """获取案例持续天数"""
        if not self.completed_at:
            return None
        start_date = self.assigned_at or self.created_at
        return (self.completed_at - start_date).days


class CaseDocument(BaseModel, table=True):
    """案例文档"""
    __tablename__ = "case_documents"
    
    case_id: str = Field(foreign_key="cases.id", index=True)
    
    # 文档信息
    filename: str = Field()
    original_filename: str = Field()
    file_path: str = Field()
    file_size: int = Field()  # 字节
    file_type: str = Field()
    mime_type: str = Field()
    
    # 分类信息
    document_type: str = Field(
        
    )  # evidence, contract, court_document, etc.
    description: Optional[str] = Field(
        default=None)
    
    # 上传信息
    uploaded_by: str = Field(foreign_key="users.id")
    
    # 访问控制
    is_public: bool = Field(default=False)
    access_level: str = Field(
        default="private")
    
    # 关联关系
    case: Case = Relationship(back_populates="documents")
    uploader: "User" = Relationship()


class CaseUpdate(BaseModel, table=True):
    """案例更新记录"""
    __tablename__ = "case_updates"
    
    case_id: str = Field(foreign_key="cases.id", index=True)
    
    # 更新信息
    title: str = Field()
    content: str = Field()
    update_type: str = Field(
        default="general")
    
    # 状态变更
    old_status: Optional[CaseStatus] = Field(default=None)
    new_status: Optional[CaseStatus] = Field(default=None)
    
    # 操作人
    updated_by: str = Field(foreign_key="users.id")
    
    # 可见性
    is_visible_to_client: bool = Field(default=True)
    
    # 关联关系
    case: Case = Relationship(back_populates="updates")
    updater: "User" = Relationship()


class CaseTemplate(BaseModel, table=True):
    """案例模板"""
    __tablename__ = "case_templates"
    
    # 模板信息
    name: str = Field()
    description: Optional[str] = Field(
        default=None)
    case_type: CaseType = Field()
    
    # 模板内容
    title_template: str = Field()
    description_template: str = Field()
    required_documents: Optional[str] = Field(
        default=None,
        description="必需文档，JSON字符串格式"
    )
    
    # 使用统计
    usage_count: int = Field(default=0)
    
    # 创建者
    created_by: str = Field(foreign_key="users.id")
    
    # 关联关系
    creator: "User" = Relationship()