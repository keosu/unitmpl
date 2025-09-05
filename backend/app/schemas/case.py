"""
案例相关数据模型
包含案例信息、文档、更新记录等
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from ..models.case import CaseStatus, CasePriority, CaseType


class CaseCreate(BaseModel):
    """创建案例请求"""
    title: str = Field(max_length=200, description="案例标题")
    description: str = Field(description="案例描述")
    case_type: CaseType = Field(description="案例类型")
    category: Optional[str] = Field(default=None, description="案例分类")
    tags: List[str] = Field(default_factory=list, description="标签")
    priority: CasePriority = Field(default=CasePriority.MEDIUM, description="优先级")
    incident_date: Optional[date] = Field(default=None, description="事发日期")
    deadline: Optional[date] = Field(default=None, description="截止日期")
    legal_issues: Optional[str] = Field(default=None, description="法律问题")
    client_goals: Optional[str] = Field(default=None, description="客户目标")
    case_notes: Optional[str] = Field(default=None, description="案例备注")
    estimated_fee: Optional[Decimal] = Field(default=None, description="预估费用")
    is_confidential: bool = Field(default=True, description="是否机密")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "合同纠纷案例",
                "description": "涉及供应商合同违约的纠纷案例",
                "case_type": "civil",
                "category": "合同纠纷",
                "tags": ["合同", "违约", "赔偿"],
                "priority": "high",
                "incident_date": "2024-01-15",
                "deadline": "2024-03-15",
                "legal_issues": "供应商未按约定交货",
                "client_goals": "要求供应商赔偿损失",
                "estimated_fee": 10000.00
            }
        }


class CaseUpdate(BaseModel):
    """更新案例请求"""
    title: Optional[str] = Field(default=None, max_length=200, description="案例标题")
    description: Optional[str] = Field(default=None, description="案例描述")
    category: Optional[str] = Field(default=None, description="案例分类")
    tags: Optional[List[str]] = Field(default=None, description="标签")
    status: Optional[CaseStatus] = Field(default=None, description="案例状态")
    priority: Optional[CasePriority] = Field(default=None, description="优先级")
    lawyer_id: Optional[str] = Field(default=None, description="指定律师ID")
    deadline: Optional[date] = Field(default=None, description="截止日期")
    legal_issues: Optional[str] = Field(default=None, description="法律问题")
    client_goals: Optional[str] = Field(default=None, description="客户目标")
    case_notes: Optional[str] = Field(default=None, description="案例备注")
    estimated_fee: Optional[Decimal] = Field(default=None, description="预估费用")
    actual_fee: Optional[Decimal] = Field(default=None, description="实际费用")
    outcome: Optional[str] = Field(default=None, description="案例结果")
    is_successful: Optional[bool] = Field(default=None, description="是否成功")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_progress",
                "lawyer_id": "123e4567-e89b-12d3-a456-426614174000",
                "priority": "high",
                "case_notes": "已收集相关证据材料"
            }
        }


class CaseResponse(BaseModel):
    """案例信息响应"""
    id: str = Field(description="案例ID")
    case_number: str = Field(description="案例编号")
    title: str = Field(description="案例标题")
    description: str = Field(description="案例描述")
    case_type: CaseType = Field(description="案例类型")
    category: Optional[str] = Field(description="案例分类")
    tags: List[str] = Field(description="标签")
    client_id: str = Field(description="客户ID")
    lawyer_id: Optional[str] = Field(description="律师ID")
    status: CaseStatus = Field(description="案例状态")
    priority: CasePriority = Field(description="优先级")
    incident_date: Optional[date] = Field(description="事发日期")
    deadline: Optional[date] = Field(description="截止日期")
    assigned_at: Optional[datetime] = Field(description="分配时间")
    completed_at: Optional[datetime] = Field(description="完成时间")
    estimated_fee: Optional[Decimal] = Field(description="预估费用")
    actual_fee: Optional[Decimal] = Field(description="实际费用")
    consultation_fee: Optional[Decimal] = Field(description="咨询费")
    legal_issues: Optional[str] = Field(description="法律问题")
    client_goals: Optional[str] = Field(description="客户目标")
    case_notes: Optional[str] = Field(description="案例备注")
    outcome: Optional[str] = Field(description="案例结果")
    is_successful: Optional[bool] = Field(description="是否成功")
    is_confidential: bool = Field(description="是否机密")
    is_public: bool = Field(description="是否公开")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    duration_days: Optional[int] = Field(description="持续天数")
    
    class Config:
        from_attributes = True


class CaseListItem(BaseModel):
    """案例列表项"""
    id: str = Field(description="案例ID")
    case_number: str = Field(description="案例编号")
    title: str = Field(description="案例标题")
    case_type: CaseType = Field(description="案例类型")
    status: CaseStatus = Field(description="案例状态")
    priority: CasePriority = Field(description="优先级")
    client_name: Optional[str] = Field(description="客户姓名")
    lawyer_name: Optional[str] = Field(description="律师姓名")
    deadline: Optional[date] = Field(description="截止日期")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    
    class Config:
        from_attributes = True


class CaseDetailResponse(BaseModel):
    """案例详细信息响应"""
    id: str = Field(description="案例ID")
    case_number: str = Field(description="案例编号")
    title: str = Field(description="案例标题")
    description: str = Field(description="案例描述")
    case_type: CaseType = Field(description="案例类型")
    category: Optional[str] = Field(description="案例分类")
    tags: List[str] = Field(description="标签")
    status: CaseStatus = Field(description="案例状态")
    priority: CasePriority = Field(description="优先级")
    incident_date: Optional[date] = Field(description="事发日期")
    deadline: Optional[date] = Field(description="截止日期")
    legal_issues: Optional[str] = Field(description="法律问题")
    client_goals: Optional[str] = Field(description="客户目标")
    case_notes: Optional[str] = Field(description="案例备注")
    outcome: Optional[str] = Field(description="案例结果")
    is_successful: Optional[bool] = Field(description="是否成功")
    estimated_fee: Optional[Decimal] = Field(description="预估费用")
    actual_fee: Optional[Decimal] = Field(description="实际费用")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    # 关联信息
    client: "UserResponse" = Field(description="客户信息")
    lawyer: Optional["LawyerResponse"] = Field(description="律师信息")
    documents: List["CaseDocumentResponse"] = Field(description="案例文档")
    updates: List["CaseUpdateResponse"] = Field(description="更新记录")
    
    class Config:
        from_attributes = True


class CaseSearchParams(BaseModel):
    """案例搜索参数"""
    q: Optional[str] = Field(default=None, description="搜索关键词")
    case_type: Optional[CaseType] = Field(default=None, description="案例类型")
    status: Optional[CaseStatus] = Field(default=None, description="案例状态")
    priority: Optional[CasePriority] = Field(default=None, description="优先级")
    client_id: Optional[str] = Field(default=None, description="客户ID")
    lawyer_id: Optional[str] = Field(default=None, description="律师ID")
    start_date: Optional[date] = Field(default=None, description="开始日期")
    end_date: Optional[date] = Field(default=None, description="结束日期")
    tags: Optional[List[str]] = Field(default=None, description="标签")
    sort_by: str = Field(default="created_at", description="排序字段")
    sort_order: str = Field(default="desc", description="排序方向")


class CaseDocumentUpload(BaseModel):
    """案例文档上传请求"""
    filename: str = Field(description="文件名")
    document_type: str = Field(description="文档类型")
    description: Optional[str] = Field(default=None, description="文档描述")
    is_public: bool = Field(default=False, description="是否公开")
    access_level: str = Field(default="private", description="访问级别")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "contract.pdf",
                "document_type": "contract",
                "description": "购销合同原件",
                "is_public": False,
                "access_level": "private"
            }
        }


class CaseDocumentResponse(BaseModel):
    """案例文档响应"""
    id: str = Field(description="文档ID")
    case_id: str = Field(description="案例ID")
    filename: str = Field(description="文件名")
    original_filename: str = Field(description="原始文件名")
    file_path: str = Field(description="文件路径")
    file_size: int = Field(description="文件大小")
    file_type: str = Field(description="文件类型")
    mime_type: str = Field(description="MIME类型")
    document_type: str = Field(description="文档类型")
    description: Optional[str] = Field(description="文档描述")
    uploaded_by: str = Field(description="上传者ID")
    is_public: bool = Field(description="是否公开")
    access_level: str = Field(description="访问级别")
    created_at: datetime = Field(description="创建时间")
    uploader_name: Optional[str] = Field(description="上传者姓名")
    
    class Config:
        from_attributes = True


class CaseUpdateCreate(BaseModel):
    """创建案例更新请求"""
    title: str = Field(max_length=200, description="更新标题")
    content: str = Field(description="更新内容")
    update_type: str = Field(default="general", description="更新类型")
    new_status: Optional[CaseStatus] = Field(default=None, description="新状态")
    is_visible_to_client: bool = Field(default=True, description="客户是否可见")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "收集证据材料",
                "content": "已收集到相关的合同文件和邮件往来记录",
                "update_type": "progress",
                "new_status": "in_progress",
                "is_visible_to_client": True
            }
        }


class CaseUpdateResponse(BaseModel):
    """案例更新响应"""
    id: str = Field(description="更新ID")
    case_id: str = Field(description="案例ID")
    title: str = Field(description="更新标题")
    content: str = Field(description="更新内容")
    update_type: str = Field(description="更新类型")
    old_status: Optional[CaseStatus] = Field(description="旧状态")
    new_status: Optional[CaseStatus] = Field(description="新状态")
    updated_by: str = Field(description="更新人ID")
    is_visible_to_client: bool = Field(description="客户是否可见")
    created_at: datetime = Field(description="创建时间")
    updater_name: Optional[str] = Field(description="更新人姓名")
    
    class Config:
        from_attributes = True


class CaseTemplateCreate(BaseModel):
    """创建案例模板请求"""
    name: str = Field(max_length=100, description="模板名称")
    description: Optional[str] = Field(default=None, description="模板描述")
    case_type: CaseType = Field(description="案例类型")
    title_template: str = Field(description="标题模板")
    description_template: str = Field(description="描述模板")
    required_documents: List[str] = Field(default_factory=list, description="必需文档")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "合同纠纷模板",
                "description": "用于合同纠纷类案例的标准模板",
                "case_type": "civil",
                "title_template": "{合同类型}纠纷案例",
                "description_template": "涉及{当事人}的{合同类型}纠纷",
                "required_documents": ["合同原件", "违约证据", "损失清单"]
            }
        }


class CaseTemplateResponse(BaseModel):
    """案例模板响应"""
    id: str = Field(description="模板ID")
    name: str = Field(description="模板名称")
    description: Optional[str] = Field(description="模板描述")
    case_type: CaseType = Field(description="案例类型")
    title_template: str = Field(description="标题模板")
    description_template: str = Field(description="描述模板")
    required_documents: List[str] = Field(description="必需文档")
    usage_count: int = Field(description="使用次数")
    created_by: str = Field(description="创建者ID")
    created_at: datetime = Field(description="创建时间")
    creator_name: Optional[str] = Field(description="创建者姓名")
    
    class Config:
        from_attributes = True


# 避免循环导入
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserResponse
    from .lawyer import LawyerResponse