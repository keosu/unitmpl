"""
聊天相关数据模型
包含聊天室、消息、AI对话等
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from ..models.chat import ChatRoomType, MessageType, MessageStatus


class ChatRoomCreate(BaseModel):
    """创建聊天室请求"""
    name: Optional[str] = Field(default=None, max_length=100, description="聊天室名称")
    description: Optional[str] = Field(default=None, description="聊天室描述")
    room_type: ChatRoomType = Field(description="聊天室类型")
    case_id: Optional[str] = Field(default=None, description="关联案例ID")
    participants: List[str] = Field(default_factory=list, description="参与者ID列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "案例咨询聊天",
                "description": "关于合同纠纷的咨询",
                "room_type": "consultation",
                "case_id": "123e4567-e89b-12d3-a456-426614174000",
                "participants": ["user_id_1", "lawyer_id_1"]
            }
        }


class ChatRoomResponse(BaseModel):
    """聊天室响应"""
    id: str = Field(description="聊天室ID")
    name: Optional[str] = Field(description="聊天室名称")
    description: Optional[str] = Field(description="聊天室描述")
    room_type: ChatRoomType = Field(description="聊天室类型")
    case_id: Optional[str] = Field(description="关联案例ID")
    participants: List[str] = Field(description="参与者ID列表")
    is_active: bool = Field(description="是否活跃")
    is_archived: bool = Field(description="是否已归档")
    last_message_at: Optional[datetime] = Field(description="最后消息时间")
    created_at: datetime = Field(description="创建时间")
    created_by: str = Field(description="创建者ID")
    
    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    """创建消息请求"""
    content: str = Field(description="消息内容")
    message_type: MessageType = Field(default=MessageType.TEXT, description="消息类型")
    reply_to_id: Optional[str] = Field(default=None, description="回复消息ID")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="消息元数据")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "您好，我想咨询一个合同纠纷的问题",
                "message_type": "text",
                "reply_to_id": None,
                "metadata": None
            }
        }


class MessageResponse(BaseModel):
    """消息响应"""
    id: str = Field(description="消息ID")
    chat_room_id: str = Field(description="聊天室ID")
    sender_id: Optional[str] = Field(description="发送者ID")
    content: str = Field(description="消息内容")
    message_type: MessageType = Field(description="消息类型")
    metadata: Optional[Dict[str, Any]] = Field(description="消息元数据")
    reply_to_id: Optional[str] = Field(description="回复消息ID")
    status: MessageStatus = Field(description="消息状态")
    is_edited: bool = Field(description="是否已编辑")
    edited_at: Optional[datetime] = Field(description="编辑时间")
    is_ai_message: bool = Field(description="是否为AI消息")
    ai_model: Optional[str] = Field(description="AI模型")
    ai_confidence: Optional[float] = Field(description="AI置信度")
    file_url: Optional[str] = Field(description="文件URL")
    file_name: Optional[str] = Field(description="文件名")
    file_size: Optional[int] = Field(description="文件大小")
    file_type: Optional[str] = Field(description="文件类型")
    created_at: datetime = Field(description="创建时间")
    
    class Config:
        from_attributes = True


class AIConversationCreate(BaseModel):
    """创建AI对话请求"""
    title: Optional[str] = Field(default=None, max_length=200, description="对话标题")
    ai_model: str = Field(default="gpt-3.5-turbo", description="AI模型")
    system_prompt: Optional[str] = Field(default=None, description="系统提示词")
    max_tokens: Optional[int] = Field(default=None, description="最大token数")
    temperature: Optional[float] = Field(default=0.7, description="温度参数")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "法律咨询对话",
                "ai_model": "gpt-3.5-turbo",
                "system_prompt": "你是一个专业的法律顾问助手",
                "max_tokens": 2000,
                "temperature": 0.7
            }
        }


class AIConversationResponse(BaseModel):
    """AI对话响应"""
    id: str = Field(description="对话ID")
    user_id: Optional[str] = Field(description="用户ID")
    session_id: str = Field(description="会话ID")
    title: Optional[str] = Field(description="对话标题")
    ai_model: str = Field(description="AI模型")
    system_prompt: Optional[str] = Field(description="系统提示词")
    max_tokens: Optional[int] = Field(description="最大token数")
    temperature: Optional[float] = Field(description="温度参数")
    message_count: int = Field(description="消息数量")
    total_tokens_used: int = Field(description="总token使用量")
    total_cost: Optional[float] = Field(description="总费用")
    is_active: bool = Field(description="是否活跃")
    last_activity_at: Optional[datetime] = Field(description="最后活动时间")
    created_at: datetime = Field(description="创建时间")
    
    class Config:
        from_attributes = True


class ChatMessageRequest(BaseModel):
    """聊天消息请求（与前端mock API兼容）"""
    message: str = Field(description="用户消息")
    context: Optional[Dict[str, Any]] = Field(default=None, description="上下文信息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "您好，我想咨询一个合同纠纷的问题",
                "context": {
                    "theme": "light",
                    "format": "markdown"
                }
            }
        }


class ChatMessageResponse(BaseModel):
    """聊天消息响应（与前端mock API兼容）"""
    success: bool = Field(description="是否成功")
    data: Dict[str, Any] = Field(description="响应数据")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "content": "您好！我是您的法律助手...",
                    "timestamp": "2024-01-01T12:00:00Z",
                    "format": "markdown",
                    "metadata": {}
                }
            }
        }


class MessageReactionCreate(BaseModel):
    """创建消息反应请求"""
    reaction_type: str = Field(description="反应类型")
    emoji: Optional[str] = Field(default=None, description="表情符号")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reaction_type": "like",
                "emoji": "👍"
            }
        }


class MessageReactionResponse(BaseModel):
    """消息反应响应"""
    id: str = Field(description="反应ID")
    message_id: str = Field(description="消息ID")
    user_id: str = Field(description="用户ID")
    reaction_type: str = Field(description="反应类型")
    emoji: Optional[str] = Field(description="表情符号")
    created_at: datetime = Field(description="创建时间")
    
    class Config:
        from_attributes = True


class ChatSettingsUpdate(BaseModel):
    """聊天设置更新请求"""
    enable_notifications: Optional[bool] = Field(default=None, description="启用通知")
    enable_sound: Optional[bool] = Field(default=None, description="启用声音")
    enable_desktop_notifications: Optional[bool] = Field(default=None, description="启用桌面通知")
    show_read_receipts: Optional[bool] = Field(default=None, description="显示已读回执")
    show_typing_indicator: Optional[bool] = Field(default=None, description="显示输入指示器")
    allow_stranger_messages: Optional[bool] = Field(default=None, description="允许陌生人消息")
    enable_ai_assistant: Optional[bool] = Field(default=None, description="启用AI助手")
    ai_response_style: Optional[str] = Field(default=None, description="AI回复风格")
    ai_auto_suggest: Optional[bool] = Field(default=None, description="AI自动建议")
    
    class Config:
        json_schema_extra = {
            "example": {
                "enable_notifications": True,
                "enable_sound": True,
                "show_read_receipts": True,
                "enable_ai_assistant": True,
                "ai_response_style": "professional"
            }
        }


class ChatSettingsResponse(BaseModel):
    """聊天设置响应"""
    enable_notifications: bool = Field(description="启用通知")
    enable_sound: bool = Field(description="启用声音")
    enable_desktop_notifications: bool = Field(description="启用桌面通知")
    show_read_receipts: bool = Field(description="显示已读回执")
    show_typing_indicator: bool = Field(description="显示输入指示器")
    allow_stranger_messages: bool = Field(description="允许陌生人消息")
    enable_ai_assistant: bool = Field(description="启用AI助手")
    ai_response_style: str = Field(description="AI回复风格")
    ai_auto_suggest: bool = Field(description="AI自动建议")
    
    class Config:
        from_attributes = True