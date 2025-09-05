"""
Pydantic 数据模型（Schemas）
用于API请求和响应的数据验证
"""
from .auth import *
from .user import *
from .lawyer import *
from .case import *
from .chat import *
from .common import *

__all__ = [
    # 认证相关
    "UserLogin", "UserRegister", "TokenResponse", "RefreshTokenRequest",
    "PasswordResetRequest", "PasswordResetConfirm",
    
    # 用户相关
    "UserCreate", "UserUpdate", "UserResponse", "UserProfile",
    "UserPreferencesUpdate", "UserPreferencesResponse",
    
    # 律师相关
    "LawyerCreate", "LawyerUpdate", "LawyerResponse", "LawyerProfile",
    "LawyerReviewCreate", "LawyerReviewResponse",
    
    # 案例相关
    "CaseCreate", "CaseUpdate", "CaseResponse", "CaseListResponse",
    "CaseDocumentUpload", "CaseDocumentResponse",
    
    # 聊天相关
    "ChatRoomCreate", "ChatRoomResponse", "MessageCreate", "MessageResponse",
    "AIConversationCreate", "AIConversationResponse",
    
    # 通用
    "PaginationParams", "PaginatedResponse", "ErrorResponse", "SuccessResponse"
]