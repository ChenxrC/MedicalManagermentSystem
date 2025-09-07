<template>
  <div class="wrong-analysis">
    <StudentNavigation />
    
    <div class="header">
      <h2>错题分析</h2>
      <div class="user-info">
        <el-avatar :size="40" icon="el-icon-user"></el-avatar>
        <span class="username">{{ currentUser.username }}</span>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalWrong }}</div>
              <div class="stat-label">总错题数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.thisWeek }}</div>
              <div class="stat-label">本周错题</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.accuracy }}%</div>
              <div class="stat-label">正确率</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.improvement }}%</div>
              <div class="stat-label">提升空间</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 筛选和操作 -->
    <div class="filter-section">
      <el-row :gutter="20" align="middle">
        <el-col :span="6">
          <el-select v-model="filterExam" placeholder="选择考试" clearable>
            <el-option
              v-for="exam in examList"
              :key="exam.id"
              :label="exam.title"
              :value="exam.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filterType" placeholder="题目类型" clearable>
            <el-option label="选择题" value="choice" />
            <el-option label="填空题" value="fill" />
            <el-option label="问答题" value="essay" />
            <el-option label="多选题" value="multiple_choice" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="refreshData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 错题列表 -->
    <div class="wrong-answers-section">
      <div class="section-header">
        <h3>错题详情</h3>
        <div class="header-actions">
          <el-button type="success" @click="exportData">
            <el-icon><Download /></el-icon>
            导出错题
          </el-button>
          <el-button type="warning" @click="markAsReviewed">
            <el-icon><Check /></el-icon>
            标记已复习
          </el-button>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="!Array.isArray(filteredWrongAnswers) || filteredWrongAnswers.length === 0" class="empty-state">
        <el-empty description="暂无错题数据" />
      </div>

      <div v-else class="wrong-answers-list">
        <el-card 
          v-for="(item, index) in (Array.isArray(filteredWrongAnswers) ? filteredWrongAnswers : [])" 
          :key="item.id" 
          class="wrong-answer-card"
          :class="{ 'reviewed': item.is_reviewed }"
        >
          <div class="card-header">
            <div class="question-info">
              <span class="question-number">第{{ index + 1 }}题</span>
              <el-tag :type="getQuestionTypeColor(item.question_type)" size="small">
                {{ getQuestionTypeText(item.question_type) }}
              </el-tag>
              <span class="exam-title">{{ item.exam_title }}</span>
              <span class="date">{{ formatDate(item.date) }}</span>
            </div>
            <div class="score-info">
              <span class="score">得分：{{ item.score }}/{{ item.total_score }}</span>
              <el-tag 
                :type="item.is_reviewed ? 'success' : 'warning'" 
                size="small"
              >
                {{ item.is_reviewed ? '已复习' : '未复习' }}
              </el-tag>
            </div>
          </div>

          <div class="card-content">
            <div class="question-section">
              <h4>题目内容：</h4>
              <p class="question-text">{{ item.question_text }}</p>
              <div v-if="item.question_image" class="question-image">
                <img :src="item.question_image" alt="题目图片" />
              </div>
            </div>

            <div class="answer-section">
              <div class="your-answer">
                <h4>你的答案：</h4>
                <p class="answer-text wrong">{{ item.your_answer }}</p>
              </div>
              <div class="correct-answer">
                <h4>正确答案：</h4>
                <p class="answer-text correct">{{ item.correct_answer }}</p>
              </div>
            </div>

            <div class="analysis-section">
              <h4>错题分析：</h4>
              <p class="analysis-text">{{ item.analysis }}</p>
              <div class="analysis-tips">
                <h5>学习建议：</h5>
                <ul>
                  <li v-for="tip in item.learning_tips" :key="tip">{{ tip }}</li>
                </ul>
              </div>
            </div>

            <div class="related-resources">
              <h4>相关资源：</h4>
              <div class="resources-list">
                <el-button 
                  v-for="resource in item.related_resources" 
                  :key="resource.id"
                  type="text" 
                  size="small"
                  @click="openResource(resource)"
                >
                  <el-icon><Link /></el-icon>
                  {{ resource.title }}
                </el-button>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <el-button 
              type="primary" 
              size="small" 
              @click="reviewQuestion(item)"
            >
              复习此题
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              @click="viewSimilarQuestions(item)"
            >
              查看相似题目
            </el-button>
            <el-button 
              type="success" 
              size="small" 
              @click="markAsReviewed(item)"
              v-if="!item.is_reviewed"
            >
              标记已复习
            </el-button>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-section">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="totalItems"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Download, Check, Link } from '@element-plus/icons-vue'
import StudentNavigation from './StudentNavigation.vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'WrongAnalysis',
  components: {
    Refresh,
    Download,
    Check,
    Link,
    StudentNavigation
  },
  setup() {
    const userStore = useUserStore()
    const wrongAnswers = ref([])
    const loading = ref(false)
    const filterExam = ref('')
    const filterType = ref('')
    const dateRange = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    
    const currentUser = computed(() => userStore.userInfo)

    // 模拟考试列表
    const examList = ref([
      { id: 1, title: 'JavaScript基础考试' },
      { id: 2, title: 'Vue.js框架考试' },
      { id: 3, title: 'Python编程考试' }
    ])

    // 统计信息
    const stats = computed(() => {
      const totalWrong = Array.isArray(wrongAnswers.value) ? wrongAnswers.value.length : 0
      const thisWeek = Math.floor(totalWrong * 0.3)
      const accuracy = Math.max(60, 100 - Math.floor(totalWrong * 2))
      const improvement = Math.min(40, Math.floor(totalWrong * 3))
      
      return { totalWrong, thisWeek, accuracy, improvement }
    })

    // 过滤后的错题列表
    const filteredWrongAnswers = computed(() => {
      // 确保wrongAnswers.value是数组
      if (!Array.isArray(wrongAnswers.value)) {
        return []
      }
      
      let filtered = wrongAnswers.value

      if (filterExam.value) {
        filtered = filtered.filter(item => item && item.exam_id === filterExam.value)
      }

      if (filterType.value) {
        filtered = filtered.filter(item => item && item.question_type === filterType.value)
      }

      if (dateRange.value && dateRange.value.length === 2) {
        filtered = filtered.filter(item => {
          if (!item || !item.date) return false
          const itemDate = new Date(item.date)
          const startDate = new Date(dateRange.value[0])
          const endDate = new Date(dateRange.value[1])
          return itemDate >= startDate && itemDate <= endDate
        })
      }

      return filtered
    })

    const totalItems = computed(() => filteredWrongAnswers.value.length)

    // 获取题目类型颜色
    const getQuestionTypeColor = (type) => {
      const colorMap = {
        'choice': 'primary',
        'fill': 'success',
        'essay': 'warning',
        'multiple_choice': 'info'
      }
      return colorMap[type] || 'info'
    }

    // 获取题目类型文本
    const getQuestionTypeText = (type) => {
      const textMap = {
        'choice': '选择题',
        'fill': '填空题',
        'essay': '问答题',
        'multiple_choice': '多选题'
      }
      return textMap[type] || '未知'
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }

    // 获取错题数据
    const fetchWrongAnswers = async () => {
      try {
        loading.value = true
        
        // 模拟错题数据
        const mockWrongAnswers = [
          {
            id: 1,
            exam_id: 1,
            exam_title: 'JavaScript基础考试',
            question_type: 'choice',
            question_text: 'JavaScript中，以下哪个方法用于将字符串转换为整数？',
            question_image: null,
            your_answer: 'parseInt()',
            correct_answer: 'parseInt()',
            score: 0,
            total_score: 5,
            date: '2024-01-15',
            is_reviewed: false,
            analysis: '你的答案是正确的，但可能由于格式问题被判定为错误。parseInt()确实是JavaScript中用于将字符串转换为整数的方法。',
            learning_tips: [
              '复习JavaScript数据类型转换方法',
              '注意parseInt()和parseFloat()的区别',
              '了解Number()构造函数的使用'
            ],
            related_resources: [
              { id: 1, title: 'JavaScript数据类型转换教程' },
              { id: 2, title: 'parseInt()方法详解' }
            ]
          },
          {
            id: 2,
            exam_id: 2,
            exam_title: 'Vue.js框架考试',
            question_type: 'fill',
            question_text: 'Vue.js中，用于声明响应式数据的选项是____。',
            question_image: null,
            your_answer: 'data',
            correct_answer: 'data()',
            score: 2,
            total_score: 5,
            date: '2024-01-20',
            is_reviewed: true,
            analysis: '你的答案基本正确，但Vue.js中data应该是一个函数，返回一个对象。这是为了确保每个组件实例都有自己独立的数据副本。',
            learning_tips: [
              '理解Vue.js组件数据的作用域',
              '掌握data()函数的使用方式',
              '学习Vue.js响应式原理'
            ],
            related_resources: [
              { id: 3, title: 'Vue.js组件数据管理' },
              { id: 4, title: 'Vue.js响应式系统详解' }
            ]
          },
          {
            id: 3,
            exam_id: 3,
            exam_title: 'Python编程考试',
            question_type: 'essay',
            question_text: '请解释Python中的装饰器模式，并给出一个实际的使用示例。',
            question_image: null,
            your_answer: '装饰器是一种设计模式，用于在不修改原函数的情况下添加新功能。',
            correct_answer: '装饰器是Python中的一种设计模式，它允许我们在不修改原函数代码的情况下，通过包装函数来扩展其功能。装饰器本质上是一个函数，它接受一个函数作为参数，并返回一个新的函数。',
            score: 3,
            total_score: 10,
            date: '2024-01-25',
            is_reviewed: false,
            analysis: '你的回答过于简单，没有详细解释装饰器的工作原理和使用方法。需要补充装饰器的语法、实际应用场景和代码示例。',
            learning_tips: [
              '深入学习Python装饰器语法',
              '理解装饰器的工作原理',
              '练习编写自定义装饰器',
              '掌握装饰器的实际应用场景'
            ],
            related_resources: [
              { id: 5, title: 'Python装饰器详解' },
              { id: 6, title: '装饰器设计模式' }
            ]
          }
        ]
        
        // 确保数据是数组
        wrongAnswers.value = Array.isArray(mockWrongAnswers) ? mockWrongAnswers : []
        console.log(`获取到 ${wrongAnswers.value.length} 个错题`)
        
      } catch (error) {
        console.error('获取错题数据失败:', error)
        ElMessage.error('获取错题数据失败')
        wrongAnswers.value = []
      } finally {
        loading.value = false
      }
    }

    // 刷新数据
    const refreshData = () => {
      fetchWrongAnswers()
    }

    // 导出数据
    const exportData = () => {
      ElMessage.success('错题数据导出功能开发中...')
    }

    // 标记已复习
    const markAsReviewed = (item) => {
      if (item) {
        item.is_reviewed = true
        ElMessage.success('已标记为复习完成')
      } else {
        wrongAnswers.value.forEach(item => {
          item.is_reviewed = true
        })
        ElMessage.success('已全部标记为复习完成')
      }
    }

    // 复习题目
    const reviewQuestion = (item) => {
      ElMessage.info(`开始复习题目：${item.question_text.substring(0, 20)}...`)
    }

    // 查看相似题目
    const viewSimilarQuestions = (item) => {
      ElMessage.info(`查看相似题目：${item.question_text.substring(0, 20)}...`)
    }

    // 打开资源
    const openResource = (resource) => {
      ElMessage.info(`打开资源：${resource.title}`)
    }

    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
    }

    onMounted(() => {
      fetchWrongAnswers()
    })

    return {
      wrongAnswers,
      loading,
      currentUser,
      examList,
      stats,
      filteredWrongAnswers,
      filterExam,
      filterType,
      dateRange,
      currentPage,
      pageSize,
      totalItems,
      getQuestionTypeColor,
      getQuestionTypeText,
      formatDate,
      fetchWrongAnswers,
      refreshData,
      exportData,
      markAsReviewed,
      reviewQuestion,
      viewSimilarQuestions,
      openResource,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.wrong-analysis {
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

.stats-section {
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

.filter-section {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.wrong-answers-section {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.section-header h3 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.loading-container {
  padding: 40px;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.wrong-answers-list {
  padding: 20px;
}

.wrong-answer-card {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
}

.wrong-answer-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.wrong-answer-card.reviewed {
  border-color: #67c23a;
  background: #f0f9ff;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.question-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.question-number {
  font-weight: bold;
  color: #409eff;
}

.exam-title {
  color: #606266;
  font-size: 14px;
}

.date {
  color: #909399;
  font-size: 12px;
}

.score-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score {
  color: #f56c6c;
  font-weight: bold;
}

.card-content {
  line-height: 1.6;
}

.question-section,
.answer-section,
.analysis-section,
.related-resources {
  margin-bottom: 20px;
}

.question-section h4,
.answer-section h4,
.analysis-section h4,
.related-resources h4 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 16px;
}

.question-text {
  color: #606266;
  margin: 0;
}

.question-image {
  margin-top: 10px;
}

.question-image img {
  max-width: 100%;
  border-radius: 4px;
}

.answer-section {
  display: flex;
  gap: 20px;
}

.your-answer,
.correct-answer {
  flex: 1;
}

.answer-text {
  margin: 0;
  padding: 10px;
  border-radius: 4px;
  font-weight: bold;
}

.answer-text.wrong {
  background: #fef0f0;
  color: #f56c6c;
  border: 1px solid #fbc4c4;
}

.answer-text.correct {
  background: #f0f9ff;
  color: #67c23a;
  border: 1px solid #b3d8ff;
}

.analysis-text {
  color: #606266;
  margin: 0 0 15px 0;
}

.analysis-tips h5 {
  margin: 0 0 10px 0;
  color: #303133;
}

.analysis-tips ul {
  margin: 0;
  padding-left: 20px;
  color: #606266;
}

.analysis-tips li {
  margin-bottom: 5px;
}

.resources-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  padding: 20px;
}
</style>
