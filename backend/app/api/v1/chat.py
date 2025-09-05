"""
聊天服务API路由
包含AI聊天、实时消息等功能
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import asyncio
import random
from typing import Optional, List
from datetime import datetime

from app.database import get_session
from app.models import User, ChatRoom, ChatMessage, AIConversation
from app.schemas.chat import (
    ChatMessageRequest, ChatMessageResponse, ChatRoomCreate, ChatRoomResponse,
    MessageCreate, MessageResponse, AIConversationCreate, AIConversationResponse,
    ChatSettingsUpdate, ChatSettingsResponse
)
from app.schemas.common import PaginatedResponse, SuccessResponse
from app.utils.dependencies import get_current_user, require_current_user

router = APIRouter()

# Mock数据 - 与前端保持一致
MOCK_REPLIES = [
    "感谢您的咨询。根据您描述的情况，这确实是一个需要仔细分析的法律问题。",
    "从法律角度来看，您遇到的问题涉及多个法律条文。建议我们先梳理一下相关证据。",
    "这类案件在实践中比较常见，通常有以下几种处理方式...",
    "您提到的合同条款确实存在一些问题，我建议从以下几个方面来分析..."
]

MARKDOWN_REPLIES = [
    """# 法律建议总结

## 您的问题分析

根据您提供的信息，我建议从以下几个方面来处理：

### 1. 合同条款审查
- **核心条款**：仔细检查争议条款的具体内容
- **违约责任**：明确双方的违约责任和赔偿标准
- **履行期限**：确认合同履行的时间要求

### 2. 证据收集
```
重要文件清单：
✓ 原始合同文件
✓ 往来邮件记录  
✓ 付款凭证
✓ 交付证明
```

### 3. 法律依据

> 根据《合同法》第107条规定："当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"

| 处理方式 | 适用情况 | 预期效果 |
|---------|---------|----------|
| 协商解决 | 争议较小 | 快速、成本低 |
| 调解 | 双方有合作意愿 | 维护关系 |
| 仲裁 | 合同有仲裁条款 | 专业、效率高 |
| 诉讼 | 其他方式无效 | 强制执行 |

**下一步建议**：
1. 整理完整的证据材料
2. 评估各种解决方案的可行性
3. 制定具体的维权策略

如需进一步咨询，请随时联系我。""",
    
    """## 🏛️ 诉讼流程指南

### 民事诉讼的基本步骤

#### 第一阶段：起诉准备
1. **起诉条件确认**
   - 原告是与本案有直接利害关系的公民、法人
   - 有明确的被告
   - 有具体的诉讼请求和事实、理由
   - 属于人民法院受理民事诉讼的范围

2. **材料准备**
   ```markdown
   必备材料：
   - 起诉状（一式两份）
   - 身份证明文件
   - 证据材料清单
   - 代理人委托书（如有）
   ```

#### 第二阶段：法院受理
- **时间**：法院应在7日内决定是否受理
- **费用**：根据诉讼标的额缴纳案件受理费
- **流程**：
  1. 提交材料
  2. 法院审查
  3. 缴费通知
  4. 正式立案

#### 第三阶段：庭审程序

> **注意**：简易程序审理期限为3个月，普通程序为6个月

**庭审要点**：
- 📋 充分准备答辩材料
- 🎯 突出核心争议焦点
- 📝 注意法庭纪律
- 💼 配合法官调查

有什么具体问题需要我详细解答吗？"""
]

@router.post("/message", response_model=ChatMessageResponse, summary="发送聊天消息")
async def send_message(
    request: ChatMessageRequest,
    current_user: Optional[User] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    发送聊天消息并获取AI回复
    
    与前端的mock数据API保持一致的接口格式：
    - 支持主题感知回复
    - 支持Markdown格式响应
    - 模拟延迟以提供真实体验
    """
    try:
        # 模拟处理延迟
        await asyncio.sleep(1.5)
        
        # 获取上下文信息
        context = request.context or {}
        theme = context.get("theme", "light")
        
        # 基于消息内容选择回复类型
        message_lower = request.message.lower()
        
        # 检查是否需要Markdown回复
        markdown_keywords = ["详细", "分析", "流程", "步骤", "总结", "建议", "指南", "如何", "怎么"]
        use_markdown = any(keyword in message_lower for keyword in markdown_keywords)
        
        if use_markdown:
            content = random.choice(MARKDOWN_REPLIES)
            format_type = "markdown"
        else:
            content = random.choice(MOCK_REPLIES)
            format_type = "text"
        
        # 构造响应数据
        response_data = {
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "format": format_type,
            "metadata": {
                "ai_model": "legal-assistant-v1",
                "confidence": round(random.uniform(0.85, 0.98), 2),
                "theme": theme,
                "processing_time_ms": random.randint(800, 1500)
            }
        }
        
        # 如果用户已登录，记录到数据库
        if current_user:
            # TODO: 保存消息到数据库
            pass
        
        return ChatMessageResponse(
            success=True,
            data=response_data
        )
        
    except Exception as e:
        # 返回错误信息
        error_response = {
            "content": "抱歉，我现在遇到了一些技术问题，请稍后再试。如果问题持续存在，请联系技术支持。",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "format": "text",
            "metadata": {
                "error": True,
                "error_type": "service_unavailable"
            }
        }
        
        return ChatMessageResponse(
            success=False,
            data=error_response
        )

@router.get("/rooms", response_model=PaginatedResponse[ChatRoomResponse], summary="获取聊天室列表")
async def list_chat_rooms(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """获取当前用户的聊天室列表"""
    # 查询用户参与的聊天室
    stmt = (
        select(ChatRoom)
        .where(ChatRoom.participants.contains([str(current_user.id)]))
        .order_by(desc(ChatRoom.last_message_at))
        .offset((page - 1) * size)
        .limit(size)
    )
    
    result = await session.execute(stmt)
    rooms = result.scalars().all()
    
    # 获取总数
    count_stmt = (
        select(ChatRoom)
        .where(ChatRoom.participants.contains([str(current_user.id)]))
    )
    count_result = await session.execute(count_stmt)
    total = len(count_result.scalars().all())
    
    return PaginatedResponse.create(
        items=[ChatRoomResponse.from_orm(room) for room in rooms],
        total=total,
        page=page,
        size=size
    )

@router.post("/rooms", response_model=SuccessResponse[ChatRoomResponse], summary="创建聊天室")
async def create_chat_room(
    room_data: ChatRoomCreate,
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """创建新的聊天室"""
    # 创建聊天室
    room = ChatRoom(
        name=room_data.name,
        description=room_data.description,
        room_type=room_data.room_type,
        case_id=room_data.case_id,
        participants=room_data.participants + [str(current_user.id)],
        created_by=current_user.id
    )
    
    session.add(room)
    await session.commit()
    await session.refresh(room)
    
    return SuccessResponse.create(
        message="聊天室创建成功",
        data=ChatRoomResponse.from_orm(room)
    )

@router.get("/rooms/{room_id}/messages", response_model=PaginatedResponse[MessageResponse], summary="获取聊天记录")
async def get_messages(
    room_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """获取指定聊天室的消息记录"""
    # 验证用户是否有权限访问该聊天室
    room_stmt = select(ChatRoom).where(ChatRoom.id == room_id)
    room_result = await session.execute(room_stmt)
    room = room_result.scalar_one_or_none()
    
    if not room or str(current_user.id) not in room.participants:
        raise HTTPException(status_code=403, detail="无权限访问该聊天室")
    
    # 查询消息
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_room_id == room_id)
        .order_by(desc(ChatMessage.created_at))
        .offset((page - 1) * size)
        .limit(size)
    )
    
    result = await session.execute(stmt)
    messages = result.scalars().all()
    
    # 获取总数
    count_stmt = select(ChatMessage).where(ChatMessage.chat_room_id == room_id)
    count_result = await session.execute(count_stmt)
    total = len(count_result.scalars().all())
    
    return PaginatedResponse.create(
        items=[MessageResponse.from_orm(msg) for msg in reversed(messages)],
        total=total,
        page=page,
        size=size
    )

@router.post("/ai/conversation", response_model=SuccessResponse[AIConversationResponse], summary="创建AI对话")
async def create_ai_conversation(
    conversation_data: AIConversationCreate,
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """创建新的AI对话会话"""
    import uuid
    
    conversation = AIConversation(
        user_id=current_user.id,
        session_id=str(uuid.uuid4()),
        title=conversation_data.title,
        ai_model=conversation_data.ai_model,
        system_prompt=conversation_data.system_prompt,
        max_tokens=conversation_data.max_tokens,
        temperature=conversation_data.temperature
    )
    
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    
    return SuccessResponse.create(
        message="AI对话创建成功",
        data=AIConversationResponse.from_orm(conversation)
    )

@router.get("/settings", response_model=ChatSettingsResponse, summary="获取聊天设置")
async def get_chat_settings(
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """获取用户的聊天设置"""
    # TODO: 实现聊天设置查询
    # 临时返回默认设置
    return ChatSettingsResponse(
        enable_notifications=True,
        enable_sound=True,
        enable_desktop_notifications=True,
        show_read_receipts=True,
        show_typing_indicator=True,
        allow_stranger_messages=False,
        enable_ai_assistant=True,
        ai_response_style="professional",
        ai_auto_suggest=True
    )

@router.put("/settings", response_model=SuccessResponse[ChatSettingsResponse], summary="更新聊天设置")
async def update_chat_settings(
    settings_data: ChatSettingsUpdate,
    current_user: User = Depends(require_current_user),
    session: AsyncSession = Depends(get_session)
):
    """更新用户的聊天设置"""
    # TODO: 实现聊天设置更新
    # 临时返回成功响应
    return SuccessResponse.create(
        message="聊天设置更新成功",
        data=ChatSettingsResponse(
            enable_notifications=True,
            enable_sound=True,
            enable_desktop_notifications=True,
            show_read_receipts=True,
            show_typing_indicator=True,
            allow_stranger_messages=False,
            enable_ai_assistant=True,
            ai_response_style="professional",
            ai_auto_suggest=True
        )
    )