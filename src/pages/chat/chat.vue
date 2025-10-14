<template>
	<view class="chat-container-beautified" :class="`theme-${themeStore.currentTheme}`">
		<!-- 聊天头部 -->
		<view class="chat-header">
			<view class="header-content">
				<text class="chat-title">{{ t('chat.title') }}</text>
				<view class="header-actions">
					<up-icon name="setting" size="22" color="#666"></up-icon>
				</view>
			</view>
		</view>

		<!-- 消息列表 -->
		<scroll-view 
			class="message-list" 
			scroll-y 
			:scroll-into-view="`msg-${messageList.length - 1}`"
			enable-back-to-top
		>
			<view 
				v-for="(message, index) in messageList" 
				:key="index"
				:id="`msg-${index}`"
				class="message-item-wrapper"
				:class="message.type"
			>
				<up-avatar 
					v-if="message.type === 'received'"
					text="AI"
					shape="circle"
					bgColor="#007aff"
				></up-avatar>

				<view class="message-content-wrapper">
					<view class="message-bubble" :class="message.type">
						<up-markdown 
							v-if="message.type === 'received'" 
							:content="message.content" 
							class="message-markdown"
						/>
						<text v-else class="message-text">{{ message.content }}</text>
					</view>
					<text class="message-time">{{ formatTime(message.timestamp) }}</text>
				</view>

				<up-avatar 
					v-if="message.type === 'sent'"
					:text="userStore.user.username ? userStore.user.username.substring(0, 1) : '我'"
					shape="circle"
				></up-avatar>
			</view>
			
			<!-- 正在输入提示 -->
			<view v-if="isTyping" class="message-item-wrapper received">
				<up-avatar text="AI" shape="circle" bgColor="#007aff"></up-avatar>
				<view class="message-content-wrapper">
					<view class="message-bubble received typing-bubble">
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
			<up-input 
				v-model="inputText"
				:placeholder="t('chat.input_placeholder')"
				border="none"
				class="chat-input"
				customStyle="padding: 24rpx 32rpx; background-color: #f5f5f5; border-radius: 40rpx;"
				@confirm="sendMessage"
			></up-input>
			<up-button 
				:disabled="!canSend"
				type="primary"
				shape="circle"
				class="send-btn"
				@click="sendMessage"
			>
				<up-icon name="arrow-upward" color="#fff" size="24"></up-icon>
			</up-button>
		</view>
	</view>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'
// import { chatAPI } from '@/api/chatService-v2.js'

const { t } = useI18n()
const themeStore = useThemeStore()
const userStore = useUserStore()

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

const sendMessage = async () => {
	if (!canSend.value) return
	
	const messageContent = inputText.value.trim()
	
	const userMessage = {
		type: 'sent',
		content: messageContent,
		timestamp: new Date(),
	}
	
	messageList.value.push(userMessage)
	inputText.value = ''
	
	await nextTick()
	scrollToBottom()
	
	await getAIReply(messageContent)
}

const getAIReply = async (userMessage) => {
	isTyping.value = true
	scrollToBottom()

	// Mock AI Reply
	setTimeout(() => {
		isTyping.value = false;
		const aiReply = {
			type: 'received',
			content: `这是对您消息 “**${userMessage}**” 的模拟回复。我可以处理Markdown格式，例如：\n\n- 列表项1\n- 列表项2\n\n` + '`' + 'javascript' + '`' + `\nconsole.log("Hello, World!");\n` + '`' + '`' + ` `,
			timestamp: new Date(),
		};
		messageList.value.push(aiReply);
		nextTick(() => {
			scrollToBottom();
		});
	}, 1500);
}

const scrollToBottom = () => {
	nextTick(() => {
		uni.pageScrollTo({
			scrollTop: 999999,
			duration: 100
		});
	});
}

const formatTime = (timestamp) => {
	const date = new Date(timestamp)
	const hours = date.getHours().toString().padStart(2, '0')
	const minutes = date.getMinutes().toString().padStart(2, '0')
	return `${hours}:${minutes}`
}

</script>

<style scoped>
.chat-container-beautified {
	height: 100vh;
	display: flex;
	flex-direction: column;
	background-color: #f4f6f8;
	box-sizing: border-box;
	padding-bottom: calc(var(--window-bottom) + 120rpx);
}

.theme-dark .chat-container-beautified {
	background-color: #1a1a1a;
}

.chat-header {
	background: #fff;
	border-bottom: 1px solid #e9ecef;
	padding: 24rpx 40rpx;
	position: sticky;
	top: 0;
	z-index: 100;
}

.theme-dark .chat-header {
	background: #2d3748;
	border-bottom-color: #4a5568;
}

.header-content {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.chat-title {
	font-size: 36rpx;
	font-weight: 600;
	color: #333;
}

.theme-dark .chat-title {
	color: #e2e8f0;
}

.message-list {
	flex: 1;
	padding: 40rpx 30rpx;
	overflow-y: auto;
	box-sizing: border-box;
}

.message-item-wrapper {
	display: flex;
	margin-bottom: 24rpx;
	align-items: flex-start;
	gap: 20rpx;
}

.message-item-wrapper.sent {
	flex-direction: row-reverse;
}

.message-content-wrapper {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	max-width: 75%;
}

.message-item-wrapper.sent .message-content-wrapper {
	align-items: flex-end;
}

.message-bubble {
	padding: 24rpx 32rpx;
	border-radius: 36rpx;
	word-wrap: break-word;
	overflow-wrap: break-word;
	box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
}

.message-bubble.received {
	background-color: #fff;
	border-bottom-left-radius: 8rpx;
}

.theme-dark .message-bubble.received {
	background-color: #2d3748;
}

.message-bubble.sent {
	background-color: #007aff;
	color: #fff;
	border-bottom-right-radius: 8rpx;
}

.message-text {
	font-size: 30rpx;
	line-height: 1.6;
}

.message-bubble.sent .message-text {
	color: #fff;
}

.message-markdown {
	font-size: 30rpx;
	line-height: 1.6;
}

.message-time {
	font-size: 24rpx;
	color: #aaa;
	margin-top: 12rpx;
	padding: 0 10rpx;
}

.theme-dark .message-time {
	color: #666;
}

.input-area {
	display: flex;
	align-items: center;
	gap: 20rpx;
	padding: 20rpx 30rpx;
	background-color: #fff;
	border-top: 1px solid #e9ecef;
}

.theme-dark .input-area {
	background-color: #2d3748;
	border-top-color: #4a5568;
}

.chat-input {
	flex: 1;
}

.theme-dark .chat-input {
	--up-input-color: #e2e8f0;
}

.theme-dark .chat-input ::v-deep(.u-input__content) {
	background-color: #4a5568 !important;
}

.send-btn {
	width: 88rpx;
	height: 88rpx;
	flex-shrink: 0;
}

.typing-bubble {
	padding: 20rpx 30rpx;
}

.typing-dots {
	display: flex;
	align-items: center;
	gap: 8rpx;
}

.dot {
	width: 12rpx;
	height: 12rpx;
	border-radius: 50%;
	background-color: #aaa;
	animation: typing-blink 1.4s infinite both;
}

.dot:nth-child(2) {
	animation-delay: 0.2s;
}

.dot:nth-child(3) {
	animation-delay: 0.4s;
}

@keyframes typing-blink {
	0% { opacity: 0.2; }
	20% { opacity: 1; }
	100% { opacity: 0.2; }
}
</style>