"""
数据模型包
"""
from .base import BaseModel
from .user import User, UserRole
from .lawyer import Lawyer, LawyerSpecialty, LawyerCertification
from .case import Case, CaseStatus, CaseType, CaseDocument
from .chat import ChatRoom, ChatMessage, MessageType, AIConversation, MessageReaction, ChatSettings

__all__ = [
    "BaseModel",
    "User",
    "UserRole", 
    "Lawyer",
    "LawyerSpecialty",
    "LawyerCertification",
    "Case",
    "CaseStatus",
    "CaseType",
    "CaseDocument",
    "ChatRoom",
    "ChatMessage",
    "MessageType",
    "AIConversation",
    "MessageReaction",
    "ChatSettings",
]