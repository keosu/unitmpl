"""
律师相关数据模型
包含律师信息、专业领域、评价等
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from ..models.lawyer import LawyerStatus, LawyerLevel


class LawyerCreate(BaseModel):
    """创建律师资料请求"""
    license_number: str = Field(description="执业证号")
    bar_association: str = Field(description="律师协会")
    practice_start_date: date = Field(description="执业开始日期")
    law_firm: Optional[str] = Field(default=None, description="律师事务所")
    position: Optional[str] = Field(default=None, description="职位")
    level: LawyerLevel = Field(default=LawyerLevel.JUNIOR, description="律师级别")
    specialties: List[str] = Field(default_factory=list, description="专业领域")
    professional_summary: Optional[str] = Field(default=None, description="专业总结")
    education_background: Optional[str] = Field(default=None, description="教育背景")
    hourly_rate: Optional[Decimal] = Field(default=None, description="小时费率")
    consultation_fee: Optional[Decimal] = Field(default=None, description="咨询费")
    
    class Config:
        json_schema_extra = {
            "example": {
                "license_number": "A20240001",
                "bar_association": "北京市律师协会",
                "practice_start_date": "2020-01-01",
                "law_firm": "XX律师事务所",
                "position": "合伙人",
                "level": "senior",
                "specialties": ["合同纠纷", "公司法务"],
                "professional_summary": "专注于企业法务领域...",
                "education_background": "中国政法大学法学硕士",
                "hourly_rate": 500.00,
                "consultation_fee": 200.00
            }
        }


class LawyerUpdate(BaseModel):
    """更新律师信息请求"""
    law_firm: Optional[str] = Field(default=None, description="律师事务所")
    position: Optional[str] = Field(default=None, description="职位")
    level: Optional[LawyerLevel] = Field(default=None, description="律师级别")
    specialties: Optional[List[str]] = Field(default=None, description="专业领域")
    professional_summary: Optional[str] = Field(default=None, description="专业总结")
    education_background: Optional[str] = Field(default=None, description="教育背景")
    hourly_rate: Optional[Decimal] = Field(default=None, description="小时费率")
    consultation_fee: Optional[Decimal] = Field(default=None, description="咨询费")
    is_available: Optional[bool] = Field(default=None, description="是否可用")
    accepts_new_cases: Optional[bool] = Field(default=None, description="是否接受新案例")
    
    class Config:
        json_schema_extra = {
            "example": {
                "law_firm": "新律师事务所",
                "position": "高级合伙人",
                "level": "partner",
                "specialties": ["合同纠纷", "公司法务", "知识产权"],
                "hourly_rate": 600.00,
                "is_available": True
            }
        }


class LawyerResponse(BaseModel):
    """律师信息响应"""
    id: str = Field(description="律师ID")
    user_id: str = Field(description="用户ID")
    license_number: str = Field(description="执业证号")
    bar_association: str = Field(description="律师协会")
    practice_start_date: date = Field(description="执业开始日期")
    law_firm: Optional[str] = Field(description="律师事务所")
    position: Optional[str] = Field(description="职位")
    level: LawyerLevel = Field(description="律师级别")
    specialties: List[str] = Field(description="专业领域")
    professional_summary: Optional[str] = Field(description="专业总结")
    education_background: Optional[str] = Field(description="教育背景")
    cases_handled: int = Field(description="处理案例数")
    success_rate: float = Field(description="成功率")
    average_rating: float = Field(description="平均评分")
    total_reviews: int = Field(description="总评价数")
    hourly_rate: Optional[Decimal] = Field(description="小时费率")
    consultation_fee: Optional[Decimal] = Field(description="咨询费")
    status: LawyerStatus = Field(description="律师状态")
    verified_at: Optional[datetime] = Field(description="验证时间")
    is_available: bool = Field(description="是否可用")
    accepts_new_cases: bool = Field(description="是否接受新案例")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    # 扩展信息
    experience_years: int = Field(description="执业年限")
    
    class Config:
        from_attributes = True


class LawyerProfile(BaseModel):
    """律师详细资料"""
    id: str = Field(description="律师ID")
    user_id: str = Field(description="用户ID")
    license_number: str = Field(description="执业证号")
    bar_association: str = Field(description="律师协会")
    practice_start_date: date = Field(description="执业开始日期")
    law_firm: Optional[str] = Field(description="律师事务所")
    position: Optional[str] = Field(description="职位")
    level: LawyerLevel = Field(description="律师级别")
    specialties: List[str] = Field(description="专业领域")
    professional_summary: Optional[str] = Field(description="专业总结")
    education_background: Optional[str] = Field(description="教育背景")
    cases_handled: int = Field(description="处理案例数")
    success_rate: float = Field(description="成功率")
    average_rating: float = Field(description="平均评分")
    total_reviews: int = Field(description="总评价数")
    hourly_rate: Optional[Decimal] = Field(description="小时费率")
    consultation_fee: Optional[Decimal] = Field(description="咨询费")
    status: LawyerStatus = Field(description="律师状态")
    is_available: bool = Field(description="是否可用")
    accepts_new_cases: bool = Field(description="是否接受新案例")
    experience_years: int = Field(description="执业年限")
    # 关联信息
    user: "UserResponse" = Field(description="用户信息")
    certifications: List["LawyerCertificationResponse"] = Field(description="认证资质")
    recent_reviews: List["LawyerReviewResponse"] = Field(description="最近评价")
    
    class Config:
        from_attributes = True


class LawyerListItem(BaseModel):
    """律师列表项"""
    id: str = Field(description="律师ID")
    user_id: str = Field(description="用户ID")
    full_name: Optional[str] = Field(description="姓名")
    avatar_url: Optional[str] = Field(description="头像")
    law_firm: Optional[str] = Field(description="律师事务所")
    position: Optional[str] = Field(description="职位")
    level: LawyerLevel = Field(description="律师级别")
    specialties: List[str] = Field(description="专业领域")
    average_rating: float = Field(description="平均评分")
    total_reviews: int = Field(description="总评价数")
    consultation_fee: Optional[Decimal] = Field(description="咨询费")
    is_available: bool = Field(description="是否可用")
    experience_years: int = Field(description="执业年限")
    
    class Config:
        from_attributes = True


class LawyerSearchParams(BaseModel):
    """律师搜索参数"""
    q: Optional[str] = Field(default=None, description="搜索关键词")
    specialty: Optional[str] = Field(default=None, description="专业领域")
    level: Optional[LawyerLevel] = Field(default=None, description="律师级别")
    status: Optional[LawyerStatus] = Field(default=None, description="律师状态")
    is_available: Optional[bool] = Field(default=None, description="是否可用")
    min_rating: Optional[float] = Field(default=None, description="最低评分")
    max_consultation_fee: Optional[Decimal] = Field(default=None, description="最高咨询费")
    sort_by: str = Field(default="average_rating", description="排序字段")
    sort_order: str = Field(default="desc", description="排序方向")


class LawyerReviewCreate(BaseModel):
    """创建律师评价请求"""
    rating: int = Field(ge=1, le=5, description="总体评分")
    title: Optional[str] = Field(default=None, max_length=200, description="评价标题")
    content: Optional[str] = Field(default=None, description="评价内容")
    professionalism_rating: Optional[int] = Field(default=None, ge=1, le=5, description="专业性评分")
    communication_rating: Optional[int] = Field(default=None, ge=1, le=5, description="沟通评分")
    efficiency_rating: Optional[int] = Field(default=None, ge=1, le=5, description="效率评分")
    is_anonymous: bool = Field(default=False, description="是否匿名")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "title": "专业且高效",
                "content": "律师非常专业，解决了我的问题",
                "professionalism_rating": 5,
                "communication_rating": 5,
                "efficiency_rating": 4,
                "is_anonymous": False
            }
        }


class LawyerReviewResponse(BaseModel):
    """律师评价响应"""
    id: str = Field(description="评价ID")
    lawyer_id: str = Field(description="律师ID")
    client_id: str = Field(description="客户ID")
    case_id: Optional[str] = Field(description="案例ID")
    rating: int = Field(description="总体评分")
    title: Optional[str] = Field(description="评价标题")
    content: Optional[str] = Field(description="评价内容")
    professionalism_rating: Optional[int] = Field(description="专业性评分")
    communication_rating: Optional[int] = Field(description="沟通评分")
    efficiency_rating: Optional[int] = Field(description="效率评分")
    is_anonymous: bool = Field(description="是否匿名")
    is_published: bool = Field(description="是否发布")
    created_at: datetime = Field(description="创建时间")
    # 客户信息（如果不是匿名）
    client_name: Optional[str] = Field(description="客户姓名")
    client_avatar: Optional[str] = Field(description="客户头像")
    
    class Config:
        from_attributes = True


class LawyerCertificationCreate(BaseModel):
    """创建律师认证请求"""
    name: str = Field(description="证书名称")
    issuing_authority: str = Field(description="颁发机构")
    certificate_number: Optional[str] = Field(default=None, description="证书编号")
    issued_date: date = Field(description="颁发日期")
    expiry_date: Optional[date] = Field(default=None, description="过期日期")
    certificate_url: Optional[str] = Field(default=None, description="证书文件URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "高级企业法务师",
                "issuing_authority": "中国企业法务管理协会",
                "certificate_number": "CERT2024001",
                "issued_date": "2024-01-01",
                "expiry_date": "2027-01-01",
                "certificate_url": "https://example.com/cert.pdf"
            }
        }


class LawyerCertificationResponse(BaseModel):
    """律师认证响应"""
    id: str = Field(description="认证ID")
    lawyer_id: str = Field(description="律师ID")
    name: str = Field(description="证书名称")
    issuing_authority: str = Field(description="颁发机构")
    certificate_number: Optional[str] = Field(description="证书编号")
    issued_date: date = Field(description="颁发日期")
    expiry_date: Optional[date] = Field(description="过期日期")
    certificate_url: Optional[str] = Field(description="证书文件URL")
    is_verified: bool = Field(description="是否已验证")
    verified_at: Optional[datetime] = Field(description="验证时间")
    created_at: datetime = Field(description="创建时间")
    
    class Config:
        from_attributes = True


class LawyerSpecialtyResponse(BaseModel):
    """律师专业领域响应"""
    id: str = Field(description="专业领域ID")
    name: str = Field(description="专业领域名称")
    name_en: Optional[str] = Field(description="英文名称")
    description: Optional[str] = Field(description="描述")
    parent_id: Optional[str] = Field(description="父级ID")
    
    class Config:
        from_attributes = True


# 避免循环导入
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserResponse