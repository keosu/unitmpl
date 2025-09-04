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
						<text class="typing-text">正在输入...</text>
					</view>
				</view>
			</view>
		</scroll-view>

		<!-- 输入区域 -->
		<view class="input-area">
			<view class="input-container">
				<up-input 
					v-model="inputText"
					:placeholder="t('chat.input_placeholder')"
					type="textarea"
					:maxlength="500"
					:autoHeight="true"
					:showConfirmBar="false"
					border="none"
					customStyle="flex: 1; background: #f5f5f5; border-radius: 40rpx; padding: 20rpx 30rpx;"
					@confirm="sendMessage"
				></up-input>
				<text class="char-count">{{ inputText.length }}/500</text>
				<up-button 
					:disabled="!canSend"
					type="primary"
					shape="circle"
					size="default"
					customStyle="width: 80rpx; height: 80rpx; margin-left: 20rpx;"
					@click="sendMessage"
				>
					<up-icon name="arrow-right" color="white" size="36"></up-icon>
				</up-button>
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
	
	// 滚动到底部
	await nextTick()
	scrollToBottom()
	
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
	scrollToBottom()
}

// 滚动到底部的方法
const scrollToBottom = () => {
	setTimeout(() => {
		uni.pageScrollTo({
			scrollTop: 99999,
			duration: 300
		})
	}, 100)
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
	height: 100%;
	display: flex;
	flex-direction: column;
	background: #f8f9fa;
	position: relative;
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
	padding-bottom: 100px;
	overflow-y: auto;
	box-sizing: border-box;
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

.typing-text {
	font-size: 14px;
	color: #999;
}

.input-area {
	position: absolute;
	bottom: 5px;
	left: 0;
	right: 0;
	background: #fff;
	border-top: 1px solid #eee;
	padding: 15px 20px;
	padding-bottom: 15px;
	z-index: 100;
	box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
	border-radius: 15px 15px 0 0;
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
	background: #f8f9fa;
}

.theme-dark .chat-header {
	background: #667eea;
	border-bottom-color: #5a6fd8;
}

.theme-dark .chat-title {
	color: #fff;
}

.theme-dark .message-bubble.received {
	background: #fff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.theme-dark .message-bubble.received .message-text {
	color: #333;
}

.theme-dark .typing-bubble {
	background: #fff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.theme-dark .input-area {
	background: #fff;
	border-top-color: #eee;
	box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.theme-dark .input-wrapper {
	background: #f5f5f5;
}

.theme-dark .input-text {
	color: #333;
}
</style>