/**
 * 聊天回复模拟数据模块
 * 包含各种Markdown格式的示例回复
 * 设计为易于替换，未来可无缝切换到后端API
 */

// 基础回复数据
export const basicReplies = [
	'很高兴为您服务！有什么我可以帮助您的吗？',
	'我明白您的问题，让我为您详细解答。',
	'这是一个很有趣的问题，我来为您分析一下。',
	'感谢您的提问，我会尽力为您提供准确的答案。'
]

// Markdown格式的回复示例
export const markdownReplies = [
	{
		id: 'code_example',
		content: `# 代码示例
这是一个简单的JavaScript函数：
\`\`\`javascript
function greet(name) {
    return \`Hello, \${name}!\`;
}
console.log(greet("World"));
\`\`\`

希望这个示例对你有帮助！`
	},
	{
		id: 'list_example',
		content: `## 列表示例
这里有一些要点：

### 无序列表：
- 第一项
- 第二项  
- 第三项

### 有序列表：
1. 步骤一
2. 步骤二
3. 步骤三

**注意**：这些都是重要的信息。`
	},
	{
		id: 'format_example',
		content: `我可以帮你处理各种格式的文本，包括：

- **粗体文字**
- *斜体文字* 
- \`行内代码\`
- [链接示例](https://example.com)

> 这是一个引用块，用于强调重要信息。

还有分割线：
---
希望这些格式对你有用！`
	},
	{
		id: 'table_example',
		content: `## 表格示例

| 功能 | 状态 | 描述 |
|------|------|------|
| Markdown | ✅ | 完全支持 |
| 代码高亮 | ✅ | 语法高亮 |
| 表格 | ✅ | 响应式表格 |
| 链接 | ✅ | 可点击链接 |

这样的表格让信息更清晰易读！`
	},
	{
		id: 'advanced_code',
		content: `## 高级代码示例

### Python 示例：
\`\`\`python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 输出前10个斐波那契数
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
\`\`\`

### CSS 示例：
\`\`\`css
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 20px;
}
\`\`\`

代码支持多种语言的语法高亮！`
	},
	{
		id: 'complex_content',
		content: `# 复合内容示例

## 任务清单
- [x] 已完成的任务
- [x] 另一个完成的任务
- [ ] 待完成的任务
- [ ] 未来的计划

## 数学公式（文本形式）
对于二次方程 ax² + bx + c = 0，解为：
\`x = (-b ± √(b² - 4ac)) / 2a\`

## 引用嵌套
> ### 重要提示
> 
> 这是第一层引用
> 
> > 这是嵌套的引用
> > 
> > > 这是更深层的嵌套
> 
> 回到第一层引用

## 混合列表
1. 第一项
   - 子项 A
   - 子项 B
2. 第二项
   - 子项 C
     1. 嵌套编号项
     2. 另一个编号项
3. 第三项

这展示了Markdown的强大表达能力！`
	}
]

// 主题相关的回复
export const themeReplies = [
	{
		light: '☀️ 当前是浅色主题，界面清爽明亮！',
		dark: '🌙 当前是暗色主题，保护您的眼睛！'
	}
]

// 错误处理回复
export const errorReplies = [
	'抱歉，我遇到了一些问题，请稍后再试。',
	'系统暂时无法响应，请检查网络连接。',
	'处理您的请求时出现错误，请重新尝试。'
]

// 获取随机基础回复
export function getRandomBasicReply() {
	return basicReplies[Math.floor(Math.random() * basicReplies.length)]
}

// 获取随机Markdown回复
export function getRandomMarkdownReply() {
	return markdownReplies[Math.floor(Math.random() * markdownReplies.length)].content
}

// 获取所有可用的回复内容（用于兼容现有逻辑）
export function getAllReplies() {
	return [
		...basicReplies,
		...markdownReplies.map(item => item.content)
	]
}

// 根据关键词获取相关回复
export function getReplyByKeyword(keyword) {
	const keywordMap = {
		'代码': markdownReplies.find(r => r.id === 'code_example')?.content,
		'列表': markdownReplies.find(r => r.id === 'list_example')?.content,
		'表格': markdownReplies.find(r => r.id === 'table_example')?.content,
		'格式': markdownReplies.find(r => r.id === 'format_example')?.content,
		'复杂': markdownReplies.find(r => r.id === 'complex_content')?.content
	}
	
	return keywordMap[keyword] || getRandomMarkdownReply()
}

// 获取错误回复
export function getErrorReply() {
	return errorReplies[Math.floor(Math.random() * errorReplies.length)]
}

// 获取主题相关回复
export function getThemeReply(currentTheme) {
	const themeReply = themeReplies[0]
	return currentTheme === 'dark' ? themeReply.dark : themeReply.light
}

// 模拟API响应格式（为未来后端集成做准备）
export function mockApiResponse(replyContent, delay = 1500) {
	return new Promise((resolve) => {
		setTimeout(() => {
			resolve({
				success: true,
				data: {
					content: replyContent,
					timestamp: new Date().toISOString(),
					type: 'text',
					format: 'markdown'
				},
				message: 'Success'
			})
		}, delay)
	})
}

// 导出默认配置
export default {
	basicReplies,
	markdownReplies,
	themeReplies,
	errorReplies,
	getRandomBasicReply,
	getRandomMarkdownReply,
	getAllReplies,
	getReplyByKeyword,
	getErrorReply,
	getThemeReply,
	mockApiResponse
}