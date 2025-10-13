<template>
  <view class="publish-container" :class="`theme-${themeStore.currentTheme}`">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">{{ t('publish.title') }}</text>
    </view>

    <!-- 发布表单 -->
    <view class="publish-form">
      <up-form 
        ref="publishFormRef"
        :model="formData"
        :rules="formRules"
        label-position="left"
        label-width="120"
      >
        <!-- 案例标题 -->
        <up-form-item 
          :label="t('publish.case_title')" 
          prop="title"
          required
        >
          <up-input 
            v-model="formData.title"
            :placeholder="t('publish.case_title_placeholder')"
            border="surround"
          />
        </up-form-item>

        <!-- 案例类型 -->
        <up-form-item 
          :label="t('publish.case_type')" 
          prop="case_type"
          required
        >
          <view class="case-type-container">
            <up-tag
              v-for="option in caseTypeOptions"
              :key="option.value"
              :text="option.label"
              :type="formData.case_type === option.value ? 'primary' : 'info'"
              :plain="formData.case_type !== option.value"
              shape="circle"
              class="case-type-tag"
              @click="setCaseType(option.value)"
            />
          </view>
        </up-form-item>

        <!-- 发布者 -->
        <up-form-item label="发布者" prop="publisher">
          <up-input
            :modelValue="userStore.user.username"
            disabled
            border="surround"
          ></up-input>
        </up-form-item>

        <!-- 案例描述 -->
        <up-form-item 
          :label="t('publish.case_description')" 
          prop="description"
          required
        >
          <up-textarea 
            v-model="formData.description"
            :placeholder="t('publish.case_description_placeholder')"
            border="surround"
            :auto-height="false"
            :height="200"
          />
        </up-form-item>

        <!-- 案例分类 -->
        <up-form-item 
          :label="t('publish.case_category')" 
          prop="category"
        >
          <up-input 
            v-model="formData.category"
            :placeholder="t('publish.case_category_placeholder')"
            border="surround"
          />
        </up-form-item>

        <!-- 标签 -->
        <up-form-item 
          :label="t('publish.tags')" 
          prop="tags"
        >
          <view class="tags-section">
            <up-input 
              v-model="tagInput"
              :placeholder="t('publish.tags_placeholder')"
              border="surround"
              @confirm="addTag"
            />
            <view class="tags-container">
              <up-tag 
                v-for="(tag, index) in formData.tags" 
                :key="index"
                :text="tag"
                type="primary"
                size="mini"
                closable
                @close="removeTag(index)"
                class="tag-item"
              />
            </view>
          </view>
        </up-form-item>

        <!-- 优先级 -->
        <up-form-item 
          :label="t('publish.priority')" 
          prop="priority"
        >
          <up-radio-group 
            v-model="formData.priority" 
            placement="row"
          >
            <up-radio 
              v-for="priority in priorityOptions" 
              :key="priority.value"
              :name="priority.value"
              :label="priority.label"
              class="priority-radio"
            />
          </up-radio-group>
        </up-form-item>

        <!-- 事发日期 -->
        <up-form-item :label="t('publish.incident_date')" prop="incident_date">
          <picker mode="date" :value="formData.incident_date" @change="onIncidentDateChange">
            <view class="uni-input">{{ formData.incident_date || t('publish.incident_date_placeholder') }}</view>
          </picker>
        </up-form-item>

        <!-- 截止日期 -->
        <up-form-item :label="t('publish.deadline')" prop="deadline">
          <picker mode="date" :value="formData.deadline" @change="onDeadlineChange">
            <view class="uni-input">{{ formData.deadline || t('publish.deadline_placeholder') }}</view>
          </picker>
        </up-form-item>

        <!-- 法律问题 -->
        <up-form-item 
          :label="t('publish.legal_issues')" 
          prop="legal_issues"
        >
          <up-textarea 
            v-model="formData.legal_issues"
            :placeholder="t('publish.legal_issues_placeholder')"
            border="surround"
            auto-height
          />
        </up-form-item>

        <!-- 客户目标 -->
        <up-form-item 
          :label="t('publish.client_goals')" 
          prop="client_goals"
        >
          <up-textarea 
            v-model="formData.client_goals"
            :placeholder="t('publish.client_goals_placeholder')"
            border="surround"
            auto-height
          />
        </up-form-item>

        <!-- 预估费用 -->
        <up-form-item 
          :label="t('publish.estimated_fee')" 
          prop="estimated_fee"
        >
          <up-input 
            v-model="formData.estimated_fee"
            :placeholder="t('publish.estimated_fee_placeholder')"
            type="digit"
            border="surround"
          />
        </up-form-item>

        <!-- 保密设置 -->
        <up-form-item 
          :label="t('publish.privacy_settings')" 
          prop="is_confidential"
        >
          <up-switch 
            v-model="formData.is_confidential"
            size="20"
          />
          <text class="privacy-label">
            {{ formData.is_confidential ? t('publish.confidential') : t('publish.public') }}
          </text>
        </up-form-item>

      </up-form>

      <!-- 提交按钮 -->
      <view class="submit-section">
        <up-button 
          type="primary"
          size="large"
          shape="circle"
          :loading="isSubmitting"
          :disabled="isSubmitting"
          @click="submitCase"
          class="submit-btn"
        >
          {{ isSubmitting ? t('publish.submitting') : t('publish.submit') }}
        </up-button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/store/theme.js'
import { useUserStore } from '@/store/user.js'
import { caseService } from '@/api/caseService.js'

const { t } = useI18n()
const themeStore = useThemeStore()
const userStore = useUserStore()

// 表单引用
const publishFormRef = ref(null)

// 标签输入
const tagInput = ref('')

// 提交状态
const isSubmitting = ref(false)

// 设置案例类型
const setCaseType = (type) => {
  formData.case_type = type;
}

// 表单数据
const formData = reactive({
  title: '',
  description: '',
  case_type: 'civil',
  category: '',
  tags: [],
  priority: 'medium',
  incident_date: '',
  deadline: '',
  legal_issues: '',
  client_goals: '',
  estimated_fee: '',
  is_confidential: true
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: t('publish.case_title_required'), trigger: ['blur', 'change'] },
    { min: 1, max: 200, message: t('publish.case_title_length'), trigger: ['blur', 'change'] }
  ],
  description: [
    { required: true, message: t('publish.case_description_required'), trigger: ['blur', 'change'] }
  ],
  case_type: [
    { required: true, message: t('publish.case_type_required'), trigger: ['blur', 'change'] }
  ]
}

// 案例类型选项
const caseTypeOptions = computed(() => [
  { label: t('case_type.civil'), value: 'civil' },
  { label: t('case_type.criminal'), value: 'criminal' },
  { label: t('case_type.administrative'), value: 'administrative' },
  { label: t('case_type.economic'), value: 'economic' },
  { label: t('case_type.labor'), value: 'labor' },
  { label: t('case_type.family'), value: 'family' },
  { label: t('case_type.property'), value: 'property' },
  { label: t('case_type.intellectual'), value: 'intellectual' },
  { label: t('case_type.environmental'), value: 'environmental' },
  { label: t('case_type.other'), value: 'other' }
])

// 优先级选项
const priorityOptions = computed(() => [
  { label: t('priority.low'), value: 'low' },
  { label: t('priority.medium'), value: 'medium' },
  { label: t('priority.high'), value: 'high' },
  { label: t('priority.urgent'), value: 'urgent' }
])



const onIncidentDateChange = (e) => {
  formData.incident_date = e.detail.value
}

const onDeadlineChange = (e) => {
  formData.deadline = e.detail.value
}

// 添加标签
const addTag = () => {
  if (tagInput.value.trim() && !formData.tags.includes(tagInput.value.trim())) {
    formData.tags.push(tagInput.value.trim())
    tagInput.value = ''
  }
}

// 移除标签
const removeTag = (index) => {
  formData.tags.splice(index, 1)
}

// 提交案例
const submitCase = async () => {
  try {
    // 验证表单
    await publishFormRef.value.validate()
    
    // 设置提交状态
    isSubmitting.value = true
    
    // 准备提交数据
    const submitData = {
      ...formData,
      estimated_fee: formData.estimated_fee ? parseFloat(formData.estimated_fee) : null
    }
    
    // 调用API创建案例
    const result = await caseService.createCase(submitData)
    
    // 显示成功消息
    uni.showToast({
      title: t('publish.submit_success'),
      icon: 'success'
    })
    
    // 返回上一页或跳转到案例详情页
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    console.error('提交案例失败:', error)
    uni.showToast({
      title: t('publish.submit_failed'),
      icon: 'none'
    })
  } finally {
    isSubmitting.value = false
  }
}

// 页面加载事件
onLoad(() => {
  // 检查登录状态
  if (!userStore.isLoggedIn) {
    uni.showToast({
      title: t('common.login_required'),
      icon: 'none'
    })
    
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/login/login'
      })
    }, 1500)
  }
})
</script>

<style scoped>
/* 浅色主题（默认） */
.publish-container {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 20rpx;
}

.page-header {
  text-align: center;
  margin-bottom: 40rpx;
  padding: 20rpx 0;
}

.page-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.publish-form {
  background: #fff;
  border-radius: 30rpx;
  padding: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
}

.case-type-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.case-type-tag {
  cursor: pointer;
}

.picker-wrapper,
.date-picker-wrapper {
  width: 100%;
}

.tags-section {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 10rpx;
}

.tag-item {
  margin: 0;
}

.priority-radio {
  margin-right: 30rpx;
}

.privacy-label {
  margin-left: 20rpx;
  font-size: 28rpx;
  color: #666;
}

.submit-section {
  margin-top: 60rpx;
  padding-top: 40rpx;
  border-top: 1rpx solid #eee;
}

.submit-btn {
  width: 100%;
}

/* 暗色主题 */
.theme-dark .publish-container {
  background: #1a1a1a;
}

.theme-dark .publish-form {
  background: #2d3748;
}

.theme-dark .page-title,
.theme-dark ::v-deep(.up-form-item__label) {
  color: #e2e8f0;
}

.theme-dark .privacy-label {
  color: #a0aec0;
}

.theme-dark ::v-deep(up-input),
.theme-dark ::v-deep(up-textarea) {
  background: #4a5568;
  color: #e2e8f0;
}
</style>