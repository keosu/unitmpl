"""
通用数据模型
包含分页、响应格式等通用结构
"""
from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    size: int = Field(default=20, ge=1, le=100, description="每页大小")
    
    def get_offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应格式"""
    items: List[T] = Field(description="数据列表")
    total: int = Field(description="总数量")
    page: int = Field(description="当前页码")
    size: int = Field(description="每页大小")
    pages: int = Field(description="总页数")
    has_next: bool = Field(description="是否有下一页")
    has_prev: bool = Field(description="是否有上一页")
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[T]":
        """创建分页响应"""
        pages = (total + size - 1) // size  # 向上取整
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


class SuccessResponse(BaseModel, Generic[T]):
    """成功响应格式"""
    success: bool = Field(default=True)
    message: str = Field(description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(cls, message: str = "操作成功", data: Optional[T] = None) -> "SuccessResponse[T]":
        """创建成功响应"""
        return cls(message=message, data=data)


class ErrorResponse(BaseModel):
    """错误响应格式"""
    success: bool = Field(default=False)
    error_code: str = Field(description="错误代码")
    message: str = Field(description="错误消息")
    details: Optional[Dict[str, Any]] = Field(default=None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(
        cls,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> "ErrorResponse":
        """创建错误响应"""
        return cls(
            error_code=error_code,
            message=message,
            details=details
        )


class SearchParams(BaseModel):
    """搜索参数"""
    q: Optional[str] = Field(default=None, description="搜索关键词")
    sort_by: Optional[str] = Field(default="created_at", description="排序字段")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="排序方向")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="过滤条件")


class FileUploadResponse(BaseModel):
    """文件上传响应"""
    filename: str = Field(description="文件名")
    original_filename: str = Field(description="原始文件名")
    file_path: str = Field(description="文件路径")
    file_size: int = Field(description="文件大小（字节）")
    file_type: str = Field(description="文件类型")
    upload_url: str = Field(description="访问URL")


class ValidationErrorDetail(BaseModel):
    """验证错误详情"""
    field: str = Field(description="错误字段")
    message: str = Field(description="错误消息")
    value: Any = Field(description="错误值")


class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(description="健康状态")
    app_name: str = Field(description="应用名称")
    version: str = Field(description="应用版本")
    timestamp: float = Field(description="时间戳")
    components: Dict[str, str] = Field(description="组件状态")