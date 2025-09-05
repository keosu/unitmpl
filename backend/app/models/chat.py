"""
聊天数据模型
包含聊天室、消息、AI对话等
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, JSON
from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from .base import BaseModel


class ChatRoomType(str, Enum):
    """聊天室类型"""
    PRIVATE = "private"        # 私聊（用户-律师）
    AI_CHAT = "ai_chat"       # AI对话
    GROUP = "group"           # 群聊
    CONSULTATION = "consultation"  # 咨询
    CASE_DISCUSSION = "case_discussion"  # 案例讨论


class MessageType(str, Enum):
    """消息类型"""
    TEXT = "text"             # 文本消息
    IMAGE = "image"           # 图片
    FILE = "file"             # 文件
    AUDIO = "audio"           # 音频
    VIDEO = "video"           # 视频
    LOCATION = "location"     # 位置
    SYSTEM = "system"         # 系统消息
    AI_RESPONSE = "ai_response"  # AI回复
    MARKDOWN = "markdown"     # Markdown格式


class MessageStatus(str, Enum):
    """消息状态"""
    SENT = "sent"             # 已发送
    DELIVERED = "delivered"   # 已送达
    READ = "read"             # 已读
    FAILED = "failed"         # 发送失败


class ChatRoom(BaseModel, table=True):
    """聊天室模型"""
    __tablename__ = "chat_rooms"
    
    # 基本信息
    name: Optional[str] = Field(
        default=None)
    description: Optional[str] = Field(
        default=None)
    room_type: ChatRoomType = Field(default=ChatRoomType.PRIVATE)
    
    # 关联信息
    case_id: Optional[str] = Field(
        default=None,
        foreign_key="cases.id",
        index=True
    )
    
    # 参与者列表（存储用户ID）
    participants: Optional[str] = Field(
        default=None,
        description="参与者ID列表，JSON字符串格式"
    )
    
    # 聊天室设置
    is_active: bool = Field(default=True)
    is_archived: bool = Field(default=False)
    max_participants: Optional[int] = Field(default=None)
    
    # 最后活动
    last_message_at: Optional[datetime] = Field(default=None)
    last_message_id: Optional[str] = Field(default=None)
    
    # 创建者
    created_by: str = Field(foreign_key="users.id")
    
    # 关联关系
    case: Optional["Case"] = Relationship(back_populates="chat_room")
    creator: "User" = Relationship()
    messages: List["ChatMessage"] = Relationship(back_populates="chat_room")
    
    def add_participant(self, user_id: str) -> None:
        """添加参与者"""
        if user_id not in self.participants:
            self.participants.append(user_id)
    
    def remove_participant(self, user_id: str) -> None:
        """移除参与者"""
        if user_id in self.participants:
            self.participants.remove(user_id)
    
    def is_participant(self, user_id: str) -> bool:
        """检查是否为参与者"""
        return user_id in self.participants


class ChatMessage(BaseModel, table=True):
    """聊天消息模型"""
    __tablename__ = "chat_messages"
    
    # 关联信息
    chat_room_id: str = Field(foreign_key="chat_rooms.id", index=True)
    sender_id: Optional[str] = Field(
        default=None,
        foreign_key="users.id",
        index=True
    )
    
    # 消息内容
    content: str = Field()
    message_type: MessageType = Field(default=MessageType.TEXT)
    
    # 消息元数据（存储为JSON字符串）
    message_metadata: Optional[str] = Field(
        default=None,
        description="消息元数据JSON字符串"
    )
    
    # 回复信息
    reply_to_id: Optional[str] = Field(
        default=None,
        foreign_key="chat_messages.id"
    )
    thread_id: Optional[str] = Field(default=None)
    
    # 状态信息
    status: MessageStatus = Field(default=MessageStatus.SENT)
    is_edited: bool = Field(default=False)
    edited_at: Optional[datetime] = Field(default=None)
    
    # AI相关
    is_ai_message: bool = Field(default=False)
    ai_model: Optional[str] = Field(
        default=None)
    ai_confidence: Optional[float] = Field(default=None)
    
    # 文件信息（当消息类型为文件时）
    file_url: Optional[str] = Field(
        default=None)
    file_name: Optional[str] = Field(
        default=None)
    file_size: Optional[int] = Field(default=None)
    file_type: Optional[str] = Field(
        default=None)
    
    # 关联关系  
    chat_room: ChatRoom = Relationship(back_populates="messages")
    sender: Optional["User"] = Relationship()
    reply_to: Optional["ChatMessage"] = Relationship(
        sa_relationship_kwargs={"remote_side": "ChatMessage.id"}
    )
    
    def is_system_message(self) -> bool:
        """判断是否为系统消息"""
        return self.message_type == MessageType.SYSTEM
    
    def is_file_message(self) -> bool:
        """判断是否为文件消息"""
        return self.message_type in [
            MessageType.IMAGE, 
            MessageType.FILE, 
            MessageType.AUDIO, 
            MessageType.VIDEO
        ]


class MessageReaction(BaseModel, table=True):
    """消息反应（表情回应）"""
    __tablename__ = "message_reactions"
    
    message_id: str = Field(foreign_key="chat_messages.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    
    # 反应类型（emoji或自定义）
    reaction_type: str = Field()
    emoji: Optional[str] = Field(
        default=None)
    
    # 关联关系
    message: ChatMessage = Relationship(back_populates="reactions")
    user: "User" = Relationship()
    
    class Config:
        # 确保同一用户对同一消息的同一反应类型只能有一个
        table_args = (
            {"unique_together": ["message_id", "user_id", "reaction_type"]})


class AIConversation(BaseModel, table=True):
    """AI对话会话"""
    __tablename__ = "ai_conversations"
    
    # 用户信息
    user_id: Optional[str] = Field(
        default=None,
        foreign_key="users.id",
        index=True
    )
    
    # 会话信息
    session_id: str = Field(
        index=True)
    title: Optional[str] = Field(
        default=None)
    
    # AI配置
    ai_model: str = Field(
        default="gpt-3.5-turbo")
    system_prompt: Optional[str] = Field(
        default=None)
    max_tokens: Optional[int] = Field(default=None)
    temperature: Optional[float] = Field(default=0.7)
    
    # 统计信息
    message_count: int = Field(default=0)
    total_tokens_used: int = Field(default=0)
    total_cost: Optional[float] = Field(default=0.0)
    
    # 状态
    is_active: bool = Field(default=True)
    last_activity_at: Optional[datetime] = Field(default=None)
    
    # 关联关系
    user: Optional["User"] = Relationship()
    
    def increment_usage(self, tokens_used: int, cost: float = 0.0) -> None:
        """增加使用统计"""
        self.message_count += 1
        self.total_tokens_used += tokens_used
        self.total_cost = (self.total_cost or 0.0) + cost
        self.last_activity_at = datetime.utcnow()


class ChatSettings(BaseModel, table=True):
    """聊天设置"""
    __tablename__ = "chat_settings"
    
    user_id: str = Field(foreign_key="users.id", unique=True)
    
    # 通知设置
    enable_notifications: bool = Field(default=True)
    enable_sound: bool = Field(default=True)
    enable_desktop_notifications: bool = Field(default=True)
    
    # 隐私设置
    show_read_receipts: bool = Field(default=True)
    show_typing_indicator: bool = Field(default=True)
    allow_stranger_messages: bool = Field(default=False)
    
    # AI助手设置
    enable_ai_assistant: bool = Field(default=True)
    ai_response_style: str = Field(
        default="professional")
    ai_auto_suggest: bool = Field(default=True)
    
    # 关联关系
    user: "User" = Relationship()