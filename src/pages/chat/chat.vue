<template>
	<view class="chat-container" :class="`theme-${themeStore.currentTheme}`">
		<!-- 聊天头部 -->
		<view class="chat-header">
			<view class="header-content">
				<text class="chat-title">{{ t('chat.title') }}</text>
				<view class="header-actions">
					<text class="action-btn" @click="showSettings">⚙️</text>
				</view>
			</view>
		</view>

		<!-- 消息列表 -->
		<scroll-view 
			class="message-list" 
			scroll-y 
			scroll-into-view="msg-{{messageList.length - 1}}"
			enable-back-to-top
		>
			<view 
				v-for="(message, index) in messageList" 
				:key="index"
				:id="`msg-${index}`"
				class="message-item"
				:class="message.type"
			>
				<view class="message-content">
					<view v-if="message.type === 'received'" class="avatar">
						<text class="avatar-text">🤖</text>
					</view>
					<view class="message-bubble" :class="message.type">
						<text class="message-text">{{ message.content }}</text>
						<text class="message-time">{{ formatTime(message.timestamp) }}</text>
					</view>
					<view v-if="message.type === 'sent'" class="avatar">
						<text class="avatar-text">👤</text>
					</view>
				</view>
			</view>
			
			<!-- 正在输入提示 -->
			<view v-if="isTyping" class="typing-indicator">
				<view class="typing-content">
					<view class="avatar">
						<text class="avatar-text">🤖</text>
					</view>
					<view class="typing-bubble">
						<view class="typing-dots">
							<view class="dot"></view>
							<view class="dot"></view>
							<view class="dot"></view>
						</view>
					</view>
				</view>
			</view>
		</scroll-view>

		<!-- 输入区域 -->
		<view class="input-area">
			<view class="input-container">
				<view class="input-wrapper">
					<textarea 
						v-model="inputText"
						:placeholder="t('chat.input_placeholder')"
						class="input-text"
						:maxlength="500"
						:auto-height="true"
						:show-confirm-bar="false"
						@input="onInput"
						@confirm="sendMessage"
					/>
					<text class="char-count">{{ inputText.length }}/500</text>
				</view>
				<view class="send-btn" :class="{ active: canSend }" @click="sendMessage">
					<text class="send-icon">✈️</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'

const { t } = useI18n()
const themeStore = useThemeStore()

const inputText = ref('')
const isTyping = ref(false)
const messageList = ref([
	{
		type: 'received',
		content: t('chat.welcome'),
		timestamp: new Date()
	}
])

const canSend = computed(() => inputText.value.trim().length > 0)

// 模拟回复
const mockReplies = [
	t('chat.reply_1'),
	t('chat.reply_2'),
	t('chat.reply_3'),
	t('chat.reply_4'),
	t('chat.reply_5')
]

const onInput = () => {
	// 输入处理
}

const sendMessage = async () => {
	if (!canSend.value) return
	
	const message = {
		type: 'sent',
		content: inputText.value.trim(),
		timestamp: new Date()
	}
	
	messageList.value.push(message)
	inputText.value = ''
	
	// 模拟AI回复
	await simulateReply()
}

const simulateReply = async () => {
	isTyping.value = true
	
	// 模拟延迟
	await new Promise(resolve => setTimeout(resolve, 1500))
	
	isTyping.value = false
	
	const reply = {
		type: 'received',
		content: mockReplies[Math.floor(Math.random() * mockReplies.length)],
		timestamp: new Date()
	}
	
	messageList.value.push(reply)
	
	// 滚动到底部
	await nextTick()
}

const formatTime = (timestamp) => {
	const date = new Date(timestamp)
	const hours = date.getHours().toString().padStart(2, '0')
	const minutes = date.getMinutes().toString().padStart(2, '0')
	return `${hours}:${minutes}`
}

const showSettings = () => {
	uni.showToast({
		title: t('chat.settings'),
		icon: 'none'
	})
}
</script>

<style scoped>
.chat-container {
	height: 100vh;
	display: flex;
	flex-direction: column;
	background: #f8f9fa;
	transition: all 0.3s ease;
}

.chat-header {
	background: #fff;
	border-bottom: 1px solid #eee;
	padding: 15px 20px;
	position: sticky;
	top: 0;
	z-index: 100;
}

.header-content {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.chat-title {
	font-size: 18px;
	font-weight: bold;
	color: #333;
}

.header-actions {
	display: flex;
	gap: 15px;
}

.action-btn {
	font-size: 20px;
	opacity: 0.7;
}

.message-list {
	flex: 1;
	padding: 20px;
	overflow-y: auto;
}

.message-item {
	margin-bottom: 20px;
}

.message-content {
	display: flex;
	align-items: flex-end;
	gap: 10px;
}

.message-item.sent .message-content {
	flex-direction: row-reverse;
}

.avatar {
	width: 40px;
	height: 40px;
	border-radius: 20px;
	background: #e9ecef;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-shrink: 0;
}

.avatar-text {
	font-size: 18px;
}

.message-bubble {
	max-width: 70%;
	padding: 12px 16px;
	border-radius: 18px;
	position: relative;
}

.message-bubble.received {
	background: #fff;
	border-bottom-left-radius: 6px;
}

.message-bubble.sent {
	background: #007aff;
	border-bottom-right-radius: 6px;
}

.message-text {
	display: block;
	font-size: 16px;
	line-height: 1.4;
	word-wrap: break-word;
}

.message-bubble.received .message-text {
	color: #333;
}

.message-bubble.sent .message-text {
	color: #fff;
}

.message-time {
	display: block;
	font-size: 12px;
	margin-top: 5px;
	opacity: 0.7;
}

.typing-indicator {
	margin-bottom: 20px;
}

.typing-content {
	display: flex;
	align-items: flex-end;
	gap: 10px;
}

.typing-bubble {
	background: #fff;
	padding: 12px 16px;
	border-radius: 18px;
	border-bottom-left-radius: 6px;
}

.typing-dots {
	display: flex;
	gap: 4px;
}

.dot {
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background: #ccc;
	animation: typing 1.4s infinite ease-in-out;
}

.dot:nth-child(1) {
	animation-delay: -0.32s;
}

.dot:nth-child(2) {
	animation-delay: -0.16s;
}

@keyframes typing {
	0%, 80%, 100% {
		transform: scale(0.8);
		opacity: 0.5;
	}
	40% {
		transform: scale(1);
		opacity: 1;
	}
}

.input-area {
	background: #fff;
	border-top: 1px solid #eee;
	padding: 15px 20px;
	padding-bottom: calc(15px + env(safe-area-inset-bottom));
}

.input-container {
	display: flex;
	align-items: flex-end;
	gap: 10px;
}

.input-wrapper {
	flex: 1;
	background: #f5f5f5;
	border-radius: 20px;
	padding: 10px 15px;
	position: relative;
}

.input-text {
	width: 100%;
	min-height: 20px;
	max-height: 100px;
	border: none;
	background: transparent;
	font-size: 16px;
	line-height: 1.4;
	resize: none;
}

.char-count {
	font-size: 12px;
	color: #999;
	position: absolute;
	right: 15px;
	bottom: 5px;
}

.send-btn {
	width: 40px;
	height: 40px;
	border-radius: 20px;
	background: #ddd;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.3s ease;
}

.send-btn.active {
	background: #007aff;
}

.send-icon {
	font-size: 18px;
}

.send-btn.active .send-icon {
	color: #fff;
}

/* 主题样式 */
.theme-dark .chat-container {
	background: #1a1a1a;
}

.theme-dark .chat-header {
	background: #2a2a2a;
	border-bottom-color: #333;
}

.theme-dark .chat-title {
	color: #fff;
}

.theme-dark .message-bubble.received {
	background: #2a2a2a;
}

.theme-dark .message-bubble.received .message-text {
	color: #fff;
}

.theme-dark .typing-bubble {
	background: #2a2a2a;
}

.theme-dark .input-area {
	background: #2a2a2a;
	border-top-color: #333;
}

.theme-dark .input-wrapper {
	background: #333;
}

.theme-dark .input-text {
	color: #fff;
}
</style>