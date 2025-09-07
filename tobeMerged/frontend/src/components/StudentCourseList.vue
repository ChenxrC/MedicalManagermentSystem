<template>
  <div class="student-course-list">
    <StudentNavigation />
    
    <div class="header">
      <h2>我的课程</h2>
      <div class="user-info">
        <el-avatar :size="40" icon="el-icon-user"></el-avatar>
        <span class="username">{{ currentUser.username }}</span>
      </div>
    </div>

    <div class="course-stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ courseStats.total }}</div>
              <div class="stat-label">总课程数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ courseStats.inProgress }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ courseStats.completed }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ courseStats.notStarted }}</div>
              <div class="stat-label">未开始</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="course-list">
      <div class="list-header">
        <h3>课程列表</h3>
        <el-button type="primary" @click="refreshCourses" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <div v-else-if="courses.length === 0" class="empty-state">
        <el-empty description="暂无课程" />
      </div>

      <div v-else class="course-cards">
        <el-card 
          v-for="course in courses" 
          :key="course.id" 
          class="course-card"
        >
          <div class="course-header">
            <div class="course-title">
              <h4>{{ course.title }}</h4>
              <el-tag :type="getStatusType(course)" size="small">
                {{ getStatusText(course) }}
              </el-tag>
            </div>
            <div class="course-actions">
              <el-button 
                type="primary" 
                size="small" 
                @click="startCourse(course)"
              >
                开始学习
              </el-button>
              <el-button 
                type="info" 
                size="small" 
                @click="viewCourseDetails(course)"
              >
                查看详情
              </el-button>
            </div>
          </div>

          <div class="course-content">
            <p class="course-description">{{ course.description }}</p>
            
            <div class="course-info">
              <div class="info-item">
                <el-icon><Calendar /></el-icon>
                <span>开始时间：{{ formatDate(course.start_date) }}</span>
              </div>
              <div class="info-item">
                <el-icon><Clock /></el-icon>
                <span>课程时长：{{ course.duration }} 小时</span>
              </div>
              <div class="info-item">
                <el-icon><User /></el-icon>
                <span>授课教师：{{ course.instructor }}</span>
              </div>
            </div>

            <div class="course-tags">
              <el-tag 
                v-for="tag in course.tags" 
                :key="tag" 
                size="small" 
                type="info"
                style="margin-right: 5px; margin-bottom: 5px;"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Refresh, Calendar, Clock, User } from '@element-plus/icons-vue'
import StudentNavigation from './StudentNavigation.vue'
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'StudentCourseList',
  components: {
    Refresh,
    Calendar,
    Clock,
    User,
    StudentNavigation
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const courses = ref([])
    const loading = ref(false)
    
    const currentUser = computed(() => userStore.userInfo)

    const courseStats = computed(() => {
      const total = courses.value.length
      const inProgress = Math.floor(total * 0.3)
      const completed = Math.floor(total * 0.2)
      const notStarted = total - inProgress - completed
      
      return { total, inProgress, completed, notStarted }
    })

    const getStatusType = (course) => {
      const statuses = ['info', 'warning', 'success']
      return statuses[Math.floor(Math.random() * statuses.length)]
    }

    const getStatusText = (course) => {
      const texts = ['未开始', '进行中', '已完成']
      return texts[Math.floor(Math.random() * texts.length)]
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }

    const fetchCourses = async () => {
      try {
        loading.value = true
        
        const mockCourses = [
          {
            id: 1,
            title: 'JavaScript基础入门',
            description: '从零开始学习JavaScript编程语言，掌握基础语法和核心概念',
            duration: 20,
            start_date: '2024-01-15',
            instructor: '张老师',
            tags: ['编程', '前端', '基础']
          },
          {
            id: 2,
            title: 'Vue.js框架开发',
            description: '学习Vue.js框架的使用，掌握组件化开发和状态管理',
            duration: 30,
            start_date: '2024-02-01',
            instructor: '李老师',
            tags: ['Vue.js', '前端框架', '组件化']
          },
          {
            id: 3,
            title: 'Python数据分析',
            description: '使用Python进行数据分析，掌握pandas、numpy等库的使用',
            duration: 25,
            start_date: '2024-01-20',
            instructor: '王老师',
            tags: ['Python', '数据分析', '机器学习']
          },
          {
            id: 4,
            title: 'Web安全基础',
            description: '学习Web安全基础知识，了解常见的安全威胁和防护方法',
            duration: 15,
            start_date: '2024-03-01',
            instructor: '陈老师',
            tags: ['安全', 'Web', '防护']
          }
        ]
        
        courses.value = mockCourses
        console.log(`获取到 ${mockCourses.length} 个课程`)
        
      } catch (error) {
        console.error('获取课程列表失败:', error)
        ElMessage.error('获取课程列表失败')
        courses.value = []
      } finally {
        loading.value = false
      }
    }

    const refreshCourses = () => {
      fetchCourses()
    }

    const startCourse = (course) => {
      ElMessage.success(`开始学习课程：${course.title}`)
    }

    const viewCourseDetails = (course) => {
      ElMessage.info(`查看课程详情：${course.title}`)
    }

    onMounted(() => {
      fetchCourses()
    })

    return {
      courses,
      loading,
      currentUser,
      courseStats,
      getStatusType,
      getStatusText,
      formatDate,
      fetchCourses,
      refreshCourses,
      startCourse,
      viewCourseDetails
    }
  }
}
</script>

<style scoped>
.student-course-list {
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

.course-stats {
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

.course-list {
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

.course-cards {
  padding: 20px;
}

.course-card {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
  transition: all 0.3s;
}

.course-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.course-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.course-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.course-title h4 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.course-actions {
  display: flex;
  gap: 8px;
}

.course-content {
  line-height: 1.6;
}

.course-description {
  color: #606266;
  margin-bottom: 15px;
}

.course-info {
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

.course-tags {
  margin-top: 10px;
}
</style>
