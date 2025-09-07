<template>
  <div class="student-exam-list">
    <!-- 导航栏 -->
    <StudentNavigation />
    
    <div class="header">
      <h2>我的考试</h2>
      <div class="user-info">
        <el-avatar :size="40" icon="el-icon-user"></el-avatar>
        <span class="username">{{ currentUser.username }}</span>
      </div>
    </div>

    <!-- 考试统计 -->
    <div class="exam-stats">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ examStats.total }}</div>
              <div class="stat-label">总考试数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ examStats.completed }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ examStats.pending }}</div>
              <div class="stat-label">待完成</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 考试列表 -->
    <div class="exam-list">
      <div class="list-header">
        <h3>考试列表</h3>
        <el-button type="primary" @click="refreshExams" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="exams.length === 0" class="empty-state">
        <el-empty description="暂无考试" />
      </div>

      <div v-else class="exam-cards">
        <el-card 
          v-for="exam in exams.filter(exam => exam && exam.id)" 
          :key="exam.id" 
          class="exam-card"
          :class="{ 'completed': getExamStatus(exam) === 'completed' }"
        >
          <div class="exam-header">
            <div class="exam-title">
              <h4>{{ exam.title }}</h4>
              <el-tag :type="getStatusType(exam)" size="small">
                {{ getStatusText(exam) }}
              </el-tag>
            </div>
            <div class="exam-actions">
              <el-button 
                v-if="getExamStatus(exam) === 'pending'"
                type="primary" 
                size="small" 
                @click="startExam(exam)"
              >
                开始考试
              </el-button>
              <el-button 
                v-else-if="getExamStatus(exam) === 'completed'"
                type="success" 
                size="small" 
                @click="viewScore(exam)"
              >
                查看成绩
              </el-button>
              <el-button 
                type="info" 
                size="small" 
                @click="viewExamDetails(exam)"
              >
                查看详情
              </el-button>
            </div>
          </div>

          <div class="exam-content">
            <p class="exam-description">{{ exam.description || '暂无描述' }}</p>
            
            <div class="exam-info">
              <div class="info-item">
                <el-icon><Calendar /></el-icon>
                <span>创建时间：{{ formatDate(exam.created_at) }}</span>
              </div>
              <div class="info-item">
                <el-icon><Document /></el-icon>
                <span>题目数量：{{ exam.questions?.length || 0 }} 题</span>
              </div>
              <div class="info-item">
                <el-icon><User /></el-icon>
                <span>创建者：{{ exam.created_by?.username || '未知' }}</span>
              </div>
            </div>

            <!-- 考试状态信息 -->
            <div v-if="getExamStatus(exam) === 'completed'" class="exam-result">
              <div class="result-item">
                <span class="label">得分：</span>
                <span class="value score">{{ getExamScore(exam) }} 分</span>
              </div>
              <div class="result-item">
                <span class="label">完成时间：</span>
                <span class="value">{{ getExamCompletionTime(exam) }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 考试详情对话框 -->
    <el-dialog v-model="showExamDetails" title="考试详情" width="600px">
      <div v-if="selectedExam" class="exam-details">
        <h4>{{ selectedExam.title }}</h4>
        <p>{{ selectedExam.description || '暂无描述' }}</p>
        
        <div class="details-info">
          <div class="detail-item">
            <span class="label">创建时间：</span>
            <span>{{ formatDate(selectedExam.created_at) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">题目数量：</span>
            <span>{{ selectedExam.questions?.length || 0 }} 题</span>
          </div>
          <div class="detail-item">
            <span class="label">创建者：</span>
            <span>{{ selectedExam.created_by?.username || '未知' }}</span>
          </div>
        </div>

        <!-- 题目预览 -->
        <div v-if="selectedExam.questions && selectedExam.questions.length > 0" class="questions-preview">
          <h5>题目预览</h5>
          <div class="question-list">
            <div 
              v-for="(question, index) in selectedExam.questions.slice(0, 3)" 
              :key="question.id" 
              class="question-item"
            >
              <span class="question-number">{{ index + 1 }}.</span>
              <span class="question-text">{{ question.text }}</span>
              <el-tag size="small" :type="getQuestionTypeColor(question.question_type)">
                {{ getQuestionTypeName(question.question_type) }}
              </el-tag>
            </div>
            <div v-if="selectedExam.questions.length > 3" class="more-questions">
              还有 {{ selectedExam.questions.length - 3 }} 道题目...
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Refresh, Calendar, Document, User } from '@element-plus/icons-vue'
import axios from 'axios'
import StudentNavigation from './StudentNavigation.vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'StudentExamList',
  components: {
    Refresh,
    Calendar,
    Document,
    User,
    StudentNavigation
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const exams = ref([])
    const loading = ref(false)
    const showExamDetails = ref(false)
    const selectedExam = ref(null)
    
    // 获取当前登录用户
    const currentUser = computed(() => userStore.userInfo)

    // 计算考试统计
    const examStats = computed(() => {
      const total = exams.value.length
      const completed = exams.value.filter(exam => getExamStatus(exam) === 'completed').length
      const pending = total - completed
      
      return { total, completed, pending }
    })

    // 获取考试状态
    const getExamStatus = (exam) => {
      // 检查exam是否有效
      if (!exam || !exam.id) {
        return 'pending'
      }
      
      // 检查是否有成绩记录来判断是否已完成
      if (exam.has_score) {
        return 'completed'
      }
      
      return 'pending'
    }

    // 获取状态类型
    const getStatusType = (exam) => {
      if (!exam || !exam.id) {
        return 'warning'
      }
      const status = getExamStatus(exam)
      return status === 'completed' ? 'success' : 'warning'
    }

    // 获取状态文本
    const getStatusText = (exam) => {
      if (!exam || !exam.id) {
        return '待完成'
      }
      const status = getExamStatus(exam)
      return status === 'completed' ? '已完成' : '待完成'
    }

    // 获取考试分数
    const getExamScore = (exam) => {
      // 从成绩记录中获取实际分数
      if (exam.score && exam.score.total_score !== undefined) {
        return exam.score.total_score
      }
      return 0
    }

    // 获取完成时间
    const getExamCompletionTime = (exam) => {
      // 从成绩记录中获取实际完成时间
      if (exam.score && exam.score.submitted_at) {
        return formatDate(exam.score.submitted_at)
      }
      return '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
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

    // 获取考试列表
    const fetchExams = async () => {
      try {
        loading.value = true
        console.log('获取考试列表...')
        
        // 由于没有真实的后端API，使用模拟数据
        const mockExams = [
          {
            id: 1,
            title: 'JavaScript基础考试',
            description: '测试JavaScript基础知识掌握情况，包括变量、函数、对象等概念',
            created_at: '2024-01-15T10:00:00Z',
            questions: [
              { id: 1, text: 'JavaScript中如何声明变量？', question_type: 'multiple' },
              { id: 2, text: '什么是闭包？', question_type: 'essay' },
              { id: 3, text: '数组的常用方法有哪些？', question_type: 'multiple_choice' }
            ],
            created_by: { username: '张老师' },
            has_score: false
          },
          {
            id: 2,
            title: 'Vue.js框架考试',
            description: '测试Vue.js框架的使用能力，包括组件、路由、状态管理等',
            created_at: '2024-01-20T14:30:00Z',
            questions: [
              { id: 4, text: 'Vue.js的生命周期钩子有哪些？', question_type: 'multiple_choice' },
              { id: 5, text: '如何实现组件间的通信？', question_type: 'essay' }
            ],
            created_by: { username: '李老师' },
            has_score: true,
            score: {
              total_score: 85,
              submitted_at: '2024-01-25T16:45:00Z'
            }
          },
          {
            id: 3,
            title: 'Python编程基础',
            description: '测试Python编程基础知识，包括语法、数据结构、函数等',
            created_at: '2024-01-10T09:00:00Z',
            questions: [
              { id: 6, text: 'Python中的列表和元组有什么区别？', question_type: 'essay' },
              { id: 7, text: '如何定义和使用函数？', question_type: 'multiple' }
            ],
            created_by: { username: '王老师' },
            has_score: false
          }
        ]
        
        exams.value = mockExams
        console.log(`获取到 ${mockExams.length} 个模拟考试`)
        
      } catch (error) {
        console.error('获取考试列表失败:', error)
        ElMessage.error('获取考试列表失败')
        exams.value = []
      } finally {
        loading.value = false
      }
    }

    // 刷新考试列表
    const refreshExams = () => {
      fetchExams()
    }

    // 开始考试
    const startExam = (exam) => {
      router.push(`/answer/${exam.id}`)
    }

    // 查看成绩
    const viewScore = (exam) => {
      router.push('/scores')
    }

    // 查看考试详情
    const viewExamDetails = (exam) => {
      selectedExam.value = exam
      showExamDetails.value = true
    }

    onMounted(() => {
      fetchExams()
    })

    return {
      exams,
      loading,
      currentUser,
      examStats,
      showExamDetails,
      selectedExam,
      getExamStatus,
      getStatusType,
      getStatusText,
      getExamScore,
      getExamCompletionTime,
      formatDate,
      getQuestionTypeName,
      getQuestionTypeColor,
      fetchExams,
      refreshExams,
      startExam,
      viewScore,
      viewExamDetails
    }
  }
}
</script>

<style scoped>
.student-exam-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.header h2 {
  margin: 0;
  color: #303133;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-size: 16px;
  color: #606266;
}

.exam-stats {
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.exam-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.list-header h3 {
  margin: 0;
  color: #303133;
}

.loading-container {
  padding: 40px;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.exam-cards {
  padding: 20px;
}

.exam-card {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
}

.exam-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.exam-card.completed {
  border-color: #67c23a;
  background: #f0f9ff;
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.exam-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.exam-title h4 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.exam-actions {
  display: flex;
  gap: 8px;
}

.exam-content {
  line-height: 1.6;
}

.exam-description {
  color: #606266;
  margin-bottom: 15px;
}

.exam-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
}

.exam-result {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #67c23a;
}

.result-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-item .label {
  color: #606266;
}

.result-item .value {
  font-weight: bold;
}

.result-item .score {
  color: #67c23a;
  font-size: 16px;
}

.exam-details {
  line-height: 1.6;
}

.exam-details h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.details-info {
  margin: 20px 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item .label {
  font-weight: bold;
  color: #606266;
}

.questions-preview {
  margin-top: 20px;
}

.questions-preview h5 {
  margin: 0 0 15px 0;
  color: #303133;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.question-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.question-number {
  font-weight: bold;
  color: #409eff;
  min-width: 20px;
}

.question-text {
  flex: 1;
  color: #606266;
}

.more-questions {
  text-align: center;
  color: #909399;
  font-style: italic;
  padding: 10px;
}
</style>
