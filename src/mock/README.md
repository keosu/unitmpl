# Mock 数据模块

这个目录包含了项目的模拟数据模块，采用模块化设计，便于未来无缝切换到真实的后端API。

## 文件结构

```
src/mock/
├── chatReplies.js     # 聊天回复数据模块
└── README.md          # 说明文档
```

## chatReplies.js

聊天回复数据模块，包含以下功能：

### 数据类型

- **basicReplies**: 基础文本回复数组
- **markdownReplies**: Markdown格式回复对象数组
- **themeReplies**: 主题相关回复
- **errorReplies**: 错误处理回复

### 主要函数

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `getRandomBasicReply()` | 无 | string | 获取随机基础回复 |
| `getRandomMarkdownReply()` | 无 | string | 获取随机Markdown回复 |
| `getAllReplies()` | 无 | Array | 获取所有回复内容 |
| `getReplyByKeyword(keyword)` | string | string | 根据关键词获取回复 |
| `getErrorReply()` | 无 | string | 获取错误回复 |
| `getThemeReply(theme)` | string | string | 获取主题相关回复 |
| `mockApiResponse(content, delay)` | string, number | Promise | 模拟API响应 |

### 关键词映射

支持以下关键词的智能回复：

- `代码` → 代码示例回复
- `列表` → 列表格式回复  
- `表格` → 表格格式回复
- `格式` → 文本格式回复
- `复杂` → 复合内容回复

### Markdown 支持

模拟数据完整支持以下Markdown语法：

- **标题**: H1-H6
- **代码块**: 支持语法高亮
- **列表**: 有序和无序列表
- **表格**: 响应式表格
- **引用**: 多层嵌套引用
- **链接**: 可点击链接
- **文本格式**: 粗体、斜体、行内代码
- **分割线**: 水平分割线

### API 响应格式

```javascript
{
  success: true,
  data: {
    content: "回复内容",
    timestamp: "2025-01-01T00:00:00.000Z",
    type: "text",
    format: "markdown"
  },
  message: "Success"
}
```

## 使用示例

```javascript
import { 
  getRandomMarkdownReply, 
  getReplyByKeyword,
  mockApiResponse 
} from '@/mock/chatReplies.js'

// 获取随机回复
const reply = getRandomMarkdownReply()

// 根据关键词获取回复
const codeReply = getReplyByKeyword('代码')

// 模拟API调用
const response = await mockApiResponse(reply, 1500)
```

## 未来迁移指南

当切换到真实后端API时：

1. 保持相同的API响应格式
2. 更新 `src/api/chatService.js` 中的API端点
3. 替换mock函数为真实HTTP请求
4. 保留错误处理和数据验证逻辑

## 注意事项

- 所有mock数据都采用中文内容，符合应用的语言设置规范
- Markdown内容经过优化，适配移动端显示
- 响应延迟模拟真实网络环境（默认1500ms）
- 支持主题切换功能，提供对应的回复内容