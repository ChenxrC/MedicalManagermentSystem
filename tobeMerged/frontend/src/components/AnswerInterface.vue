<template>
  <div class="exam-answer-interface">
    <!-- 导航栏 -->
    <StudentNavigation />
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!exam" class="error-container">
      <el-result icon="error" title="考试不存在" sub-title="请检查考试ID是否正确">
        <template #extra>
          <el-button type="primary" @click="$router.push('/student-exams')">返回考试列表</el-button>
        </template>
      </el-result>
    </div>
    
    <div v-else class="exam-container">
      <!-- 考试头部信息 -->
      <div class="exam-header">
        <div class="exam-info">
          <h1>{{ exam.title }}</h1>
          <p class="exam-description">{{ exam.description || '暂无描述' }}</p>
        </div>
        <div class="exam-timer">
          <el-card class="timer-card">
            <div class="timer-content">
              <el-icon><Clock /></el-icon>
              <span class="timer-text">{{ formatTime(remainingTime) }}</span>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 题目列表 -->
      <div class="questions-container">
        <div class="questions-header">
          <h2>题目列表 (共 {{ exam.questions?.length || 0 }} 题)</h2>
          <div class="progress-info">
            <span>已完成: {{ answeredCount }}/{{ exam.questions?.length || 0 }}</span>
            <el-progress 
              :percentage="progressPercentage" 
              :stroke-width="8"
              :show-text="false"
            />
          </div>
        </div>
        
        <div class="questions-list">
          <div 
            v-for="(question, index) in exam.questions" 
            :key="question.id"
            class="question-item"
            :class="{ 'answered': isQuestionAnswered(question.id) }"
          >
            <div class="question-header">
              <span class="question-number">{{ index + 1 }}.</span>
              <span class="question-type">
                <el-tag :type="getQuestionTypeColor(question.question_type)" size="small">
                  {{ getQuestionTypeName(question.question_type) }}
                </el-tag>
              </span>
              <span class="question-points">({{ question.points }}分)</span>
            </div>
            
            <div class="question-content">
              <div class="question-text">{{ question.text }}</div>
              
              <!-- 题目图片 -->
              <div v-if="question.image_url" class="question-image">
                <el-image 
                  :src="question.image_url" 
                  :preview-src-list="[question.image_url]"
                  fit="contain"
                  style="max-width: 400px; max-height: 300px;"
                />
              </div>
              
              <!-- 选择题选项 -->
              <div v-if="question.question_type === 'multiple' || question.question_type === 'multiple_choice'" class="options-list">
                <el-radio-group 
                  v-if="question.question_type === 'multiple'"
                  v-model="answers[question.id]"
                  @change="saveAnswer(question.id, $event)"
                >
                  <el-radio 
                    v-for="option in question.options" 
                    :key="option.id" 
                    :label="option.id"
                    class="option-item"
                  >
                    {{ option.text }}
                  </el-radio>
                </el-radio-group>
                
                <el-checkbox-group 
                  v-else
                  v-model="answers[question.id]"
                  @change="saveAnswer(question.id, $event)"
                >
                  <el-checkbox 
                    v-for="option in question.options" 
                    :key="option.id" 
                    :label="option.id"
                    class="option-item"
                  >
                    {{ option.text }}
                  </el-checkbox>
                </el-checkbox-group>
              </div>
              
              <!-- 填空题 -->
              <div v-else-if="question.question_type === 'fill'" class="fill-answer">
                <el-input
                  v-model="answers[question.id]"
                  type="text"
                  placeholder="请输入答案"
                  @input="saveAnswer(question.id, $event)"
                />
              </div>
              
              <!-- 问答题 -->
              <div v-else-if="question.question_type === 'essay'" class="essay-answer">
                <el-input
                  v-model="answers[question.id]"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入答案"
                  @input="saveAnswer(question.id, $event)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 底部操作栏 -->
      <div class="exam-footer">
        <div class="footer-actions">
          <el-button @click="saveProgress" :loading="saving">
            <el-icon><Save /></el-icon>
            保存进度
          </el-button>
          <el-button type="primary" @click="submitExam" :loading="submitting">
            <el-icon><Check /></el-icon>
            提交考试
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 提交确认对话框 -->
    <el-dialog v-model="showSubmitDialog" title="确认提交" width="400px">
      <div class="submit-confirm">
        <p>确定要提交考试吗？提交后将无法修改答案。</p>
        <div class="confirm-stats">
          <p>已完成: {{ answeredCount }}/{{ exam.questions?.length || 0 }} 题</p>
          <p>未完成: {{ exam.questions?.length - answeredCount || 0 }} 题</p>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showSubmitDialog = false">取消</el-button>
          <el-button type="primary" @click="confirmSubmit" :loading="submitting">
            确认提交
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Save, Check } from '@element-plus/icons-vue'
import api from '@/utils/axios'
import StudentNavigation from './StudentNavigation.vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'AnswerInterface',
  components: {
    Clock,
    Save,
    Check,
    StudentNavigation
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const exam = ref(null)
    const loading = ref(true)
    const saving = ref(false)
    const submitting = ref(false)
    const showSubmitDialog = ref(false)
    const answers = ref({})
    const remainingTime = ref(7200) // 默认2小时
    const timer = ref(null)
    
    // 计算已答题数量
    const answeredCount = computed(() => {
      return Object.keys(answers.value).filter(key => {
        const answer = answers.value[key]
        return answer !== undefined && answer !== null && answer !== ''
      }).length
    })
    
    // 计算进度百分比
    const progressPercentage = computed(() => {
      if (!exam.value?.questions?.length) return 0
      return Math.round((answeredCount.value / exam.value.questions.length) * 100)
    })
    
    // 获取考试详情
    const fetchExam = async () => {
      try {
        loading.value = true
        const examId = route.params.examId
        const studentId = userStore.userInfo?.student_profile?.id || userStore.userInfo?.id
        
        const response = await api.get(`/api/exams/${examId}/for_student/?student=${studentId}`)
        exam.value = response.data
        
        // 从本地存储恢复答案
        const savedAnswers = localStorage.getItem(`exam_answers_${examId}`)
        if (savedAnswers) {
          answers.value = JSON.parse(savedAnswers)
        }
        
      } catch (error) {
        console.error('获取考试详情失败:', error)
        ElMessage.error('获取考试详情失败')
        exam.value = null
      } finally {
        loading.value = false
      }
    }
    
    // 保存答案
    const saveAnswer = (questionId, answer) => {
      answers.value[questionId] = answer
      // 自动保存到本地存储
      const examId = route.params.examId
      localStorage.setItem(`exam_answers_${examId}`, JSON.stringify(answers.value))
    }
    
    // 检查题目是否已回答
    const isQuestionAnswered = (questionId) => {
      const answer = answers.value[questionId]
      return answer !== undefined && answer !== null && answer !== ''
    }
    
    // 保存进度
    const saveProgress = async () => {
      try {
        saving.value = true
        const examId = route.params.examId
        localStorage.setItem(`exam_answers_${examId}`, JSON.stringify(answers.value))
        ElMessage.success('进度已保存')
      } catch (error) {
        console.error('保存进度失败:', error)
        ElMessage.error('保存进度失败')
      } finally {
        saving.value = false
      }
    }
    
    // 提交考试
    const submitExam = () => {
      showSubmitDialog.value = true
    }
    
    // 确认提交
    const confirmSubmit = async () => {
      try {
        submitting.value = true
        const examId = route.params.examId
        
        // 准备提交数据
        const submitData = {
          exam_id: parseInt(examId),
          answers: Object.keys(answers.value).map(questionId => {
            const answer = answers.value[questionId]
            return {
              question_id: parseInt(questionId),
              answer_text: typeof answer === 'string' ? answer : '',
              selected_option: Array.isArray(answer) ? answer : answer
            }
          })
        }
        
        console.log('提交数据:', submitData)
        
        // 提交答案
        const response = await api.post('/api/student-answers/submit_answers/', submitData)
        
        // 清除本地存储
        localStorage.removeItem(`exam_answers_${examId}`)
        
        ElMessage.success(`考试提交成功！得分：${response.data.score}分`)
        router.push('/student-exams')
        
      } catch (error) {
        console.error('提交考试失败:', error)
        if (error.response?.data?.error) {
          ElMessage.error(error.response.data.error)
        } else {
          ElMessage.error('提交考试失败')
        }
      } finally {
        submitting.value = false
        showSubmitDialog.value = false
      }
    }
    
    // 格式化时间
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    // 获取题目类型名称
    const getQuestionTypeName = (type) => {
      const typeMap = {
        'multiple': '单选题',
        'multiple_choice': '多选题',
        'fill': '填空题',
        'essay': '问答题'
      }
      return typeMap[type] || type
    }
    
    // 获取题目类型颜色
    const getQuestionTypeColor = (type) => {
      const colorMap = {
        'multiple': 'primary',
        'multiple_choice': 'success',
        'fill': 'warning',
        'essay': 'info'
      }
      return colorMap[type] || 'default'
    }
    
    // 倒计时
    const startTimer = () => {
      timer.value = setInterval(() => {
        if (remainingTime.value > 0) {
          remainingTime.value--
        } else {
          // 时间到，自动提交
          clearInterval(timer.value)
          ElMessage.warning('考试时间已到，系统将自动提交')
          confirmSubmit()
        }
      }, 1000)
    }
    
    // 页面离开前提示
    const handleBeforeUnload = (e) => {
      if (answeredCount.value > 0) {
        e.preventDefault()
        e.returnValue = '您有未保存的答案，确定要离开吗？'
        return '您有未保存的答案，确定要离开吗？'
      }
    }
    
    onMounted(() => {
      fetchExam()
      startTimer()
      window.addEventListener('beforeunload', handleBeforeUnload)
    })
    
    onUnmounted(() => {
      if (timer.value) {
        clearInterval(timer.value)
      }
      window.removeEventListener('beforeunload', handleBeforeUnload)
    })
    
    return {
      exam,
      loading,
      saving,
      submitting,
      showSubmitDialog,
      answers,
      remainingTime,
      answeredCount,
      progressPercentage,
      saveAnswer,
      isQuestionAnswered,
      saveProgress,
      submitExam,
      confirmSubmit,
      formatTime,
      getQuestionTypeName,
      getQuestionTypeColor
    }
  }
}
</script>

<style scoped>
.exam-answer-interface {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container {
  padding: 40px;
}

.error-container {
  padding: 40px;
  text-align: center;
}

.exam-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 30px;
  border-bottom: 1px solid #e4e7ed;
}

.exam-info h1 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 24px;
}

.exam-description {
  color: #606266;
  margin: 0;
}

.timer-card {
  min-width: 120px;
}

.timer-content {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

.timer-text {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

.questions-container {
  padding: 30px;
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.questions-header h2 {
  margin: 0;
  color: #303133;
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.progress-info span {
  color: #606266;
  font-size: 14px;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.question-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s;
}

.question-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.question-item.answered {
  border-color: #67c23a;
  background: #f0f9ff;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.question-number {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.question-points {
  color: #909399;
  font-size: 14px;
}

.question-content {
  line-height: 1.6;
}

.question-text {
  font-size: 16px;
  color: #303133;
  margin-bottom: 15px;
}

.question-image {
  margin: 15px 0;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  margin-bottom: 8px;
}

.fill-answer,
.essay-answer {
  margin-top: 15px;
}

.exam-footer {
  padding: 20px 30px;
  border-top: 1px solid #e4e7ed;
  background: #f8f9fa;
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.submit-confirm {
  text-align: center;
}

.confirm-stats {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.confirm-stats p {
  margin: 5px 0;
  color: #606266;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>

