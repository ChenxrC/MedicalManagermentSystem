<template>
  <div class="exam-management">
    <AdminNavigation />
    <div class="management-content">
    <div class="page-header">
      <h1>试卷管理</h1>
      <div class="header-actions">
        <el-button type="success" @click="goToExamEditor">
          <el-icon><Plus /></el-icon>
          创建新试卷
        </el-button>
        <el-button type="primary" @click="goToExamEditor">
          <el-icon><Edit /></el-icon>
          编辑试卷
        </el-button>
      </div>
    </div>

    <div class="search-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索试卷标题"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.status" placeholder="试卷状态" clearable @change="handleSearch">
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </el-col>
        <el-col :span="4">
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-col>
      </el-row>
    </div>

    <div class="table-section">
      <el-table
        :data="filteredExams"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="试卷标题" width="200" />
        <el-table-column prop="description" label="描述" width="300" show-overflow-tooltip />
        <el-table-column prop="question_count" label="题目数量" width="100" />
        <el-table-column prop="total_points" label="总分" width="100" />
                 <el-table-column prop="is_active" label="状态" width="100">
           <template #default="scope">
             <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
               {{ scope.row.is_active ? '启用' : '禁用' }}
             </el-tag>
           </template>
         </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="editExam(scope.row)">
              编辑
            </el-button>
            <el-button size="small" type="success" @click="viewExam(scope.row)">
              查看
            </el-button>
                         <el-button 
               size="small" 
               :type="scope.row.is_active ? 'warning' : 'success'"
               @click="toggleExamStatus(scope.row)"
             >
               {{ scope.row.is_active ? '禁用' : '启用' }}
             </el-button>
            <el-button size="small" type="danger" @click="deleteExam(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalExams"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 试卷详情对话框 -->
    <el-dialog
      v-model="showExamDetail"
      title="试卷详情"
      width="800px"
    >
      <div v-if="selectedExam" class="exam-detail">
        <div class="detail-section">
          <h3>基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="试卷标题">{{ selectedExam.title }}</el-descriptions-item>
                         <el-descriptions-item label="试卷状态">
               <el-tag :type="selectedExam.is_active ? 'success' : 'danger'">
                 {{ selectedExam.is_active ? '启用' : '禁用' }}
               </el-tag>
             </el-descriptions-item>
            <el-descriptions-item label="题目数量">{{ selectedExam.question_count }}</el-descriptions-item>
            <el-descriptions-item label="总分">{{ selectedExam.total_points }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(selectedExam.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="创建者">{{ selectedExam.created_by }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="detail-section">
          <h3>试卷描述</h3>
          <p>{{ selectedExam.description || '暂无描述' }}</p>
        </div>

        <div class="detail-section">
          <h3>题目列表</h3>
          <el-table :data="selectedExam.questions" stripe>
            <el-table-column prop="id" label="题号" width="80" />
            <el-table-column prop="text" label="题目内容" show-overflow-tooltip />
            <el-table-column prop="question_type" label="题型" width="100">
              <template #default="scope">
                {{ getQuestionTypeName(scope.row.question_type) }}
              </template>
            </el-table-column>
            <el-table-column prop="points" label="分值" width="80" />
          </el-table>
        </div>
      </div>
    </el-dialog>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Search, Refresh } from '@element-plus/icons-vue'
import AdminNavigation from './AdminNavigation.vue'
import { debugAPI } from '@/utils/debug.js'
import api from '@/utils/axios'
import { useUserStore } from '@/stores/userStore'
import { PERMISSIONS } from '@/utils/permission.js'

export default {
  name: 'ExamManagement',
  components: {
    Plus,
    Edit,
    Search,
    Refresh,
    AdminNavigation
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const loading = ref(false)
    const showExamDetail = ref(false)
    const selectedExam = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalExams = ref(0)
    const hasExamPermission = ref(false)

    const exams = ref([])
    const searchForm = reactive({
      keyword: '',
      status: ''
    })

         // 模拟试卷数据
     const mockExams = [
       {
         id: 1,
         title: 'JavaScript基础考试',
         description: '测试学员对JavaScript基础知识的掌握程度',
         question_count: 20,
         total_points: 100,
         is_active: true,
         created_at: '2024-01-15T10:00:00Z',
         created_by: '管理员',
         questions: [
           { id: 1, text: 'JavaScript中，以下哪个方法用于将字符串转换为整数？', question_type: 'multiple', points: 5 },
           { id: 2, text: '请解释什么是闭包？', question_type: 'essay', points: 10 }
         ]
       },
       {
         id: 2,
         title: 'Vue.js框架考试',
         description: '测试学员对Vue.js框架的理解和应用能力',
         question_count: 15,
         total_points: 80,
         is_active: true,
         created_at: '2024-01-16T10:00:00Z',
         created_by: '管理员',
         questions: [
           { id: 1, text: 'Vue.js中的响应式数据是如何实现的？', question_type: 'essay', points: 15 },
           { id: 2, text: 'Vue.js的生命周期钩子有哪些？', question_type: 'multiple', points: 8 }
         ]
       },
       {
         id: 3,
         title: '数据库设计考试',
         description: '测试学员对数据库设计原则的理解',
         question_count: 25,
         total_points: 120,
         is_active: false,
         created_at: '2024-01-17T10:00:00Z',
         created_by: '管理员',
         questions: [
           { id: 1, text: '什么是数据库范式？', question_type: 'essay', points: 20 },
           { id: 2, text: '请设计一个学生信息表', question_type: 'essay', points: 25 }
         ]
       }
     ]

    const loadExams = async () => {
      loading.value = true
      try {
        // 从后端API获取试卷数据，使用axios实例自动添加认证头
        const response = await api.get('/api/exams')
        
        const data = response.data
        
        // 调试信息
        debugAPI.checkResponse(response, '/api/exams/')
        debugAPI.checkData(data, '/api/exams/')
        
        // 确保数据是数组格式
        if (data && Array.isArray(data.exams)) {
          // 后端返回的是{'exams': exams_data}格式
          exams.value = data.exams.map(exam => ({
            ...exam,
            // 添加前端组件所需的字段，确保界面正常显示
            description: `课程ID: ${exam.course_id} 的考试`,
            question_count: 0,  // 默认值，实际应用中应该从数据库获取
            total_points: 100,  // 默认值
            is_active: true,    // 默认值
            created_by: '管理员', // 默认值
            questions: []       // 默认空数组
          }))
          totalExams.value = data.exams.length
        } else if (Array.isArray(data)) {
          exams.value = data
          totalExams.value = data.length
        } else if (data && Array.isArray(data.results)) {
          exams.value = data.results
          totalExams.value = data.count || data.results.length
        } else {
          // 如果数据格式不正确，使用模拟数据
          console.warn('API返回的数据格式不正确，使用模拟数据')
          exams.value = mockExams
          totalExams.value = mockExams.length
        }
        
        // 调试表格数据
        debugAPI.checkTableData(exams.value, 'ExamManagement')
      } catch (error) {
        console.error('加载试卷数据失败:', error)
        ElMessage.error('加载试卷数据失败')
        // 如果API调用失败，使用模拟数据
        exams.value = mockExams
        totalExams.value = mockExams.length
      } finally {
        loading.value = false
      }
    }

    const filteredExams = computed(() => {
      // 确保exams.value是数组
      if (!Array.isArray(exams.value)) {
        return []
      }
      
      let filtered = exams.value

      if (searchForm.keyword) {
        const keyword = searchForm.keyword.toLowerCase()
        filtered = filtered.filter(exam =>
          exam && exam.title && exam.title.toLowerCase().includes(keyword) ||
          exam && exam.description && exam.description.toLowerCase().includes(keyword)
        )
      }

      if (searchForm.status) {
        filtered = filtered.filter(exam => exam && exam.is_active === (searchForm.status === 'active'))
      }

      return filtered
    })

    const handleSearch = () => {
      currentPage.value = 1
    }

    const resetSearch = () => {
      searchForm.keyword = ''
      searchForm.status = ''
      currentPage.value = 1
    }

    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
    }

    const goToExamEditor = () => {
      router.push('/exam-editor')
    }

    const editExam = (exam) => {
      router.push(`/exam-editor?id=${exam.id}`)
    }

    const viewExam = (exam) => {
      selectedExam.value = exam
      showExamDetail.value = true
    }

    const toggleExamStatus = async (exam) => {
      try {
        const newStatus = exam.is_active ? false : true
        const action = newStatus ? '启用' : '禁用'
        
        await ElMessageBox.confirm(
          `确定要${action}试卷"${exam.title}"吗？`,
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        const response = await api.patch(`/api/exams/${exam.id}/`, { is_active: newStatus })

        const updatedExam = response.data
        exam.is_active = updatedExam.is_active
        ElMessage.success(`${action}成功`)
      } catch (error) {
        if (error !== 'cancel') {
          console.error('操作失败:', error)
          ElMessage.error('操作失败')
        }
      }
    }

    const deleteExam = async (exam) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除试卷"${exam.title}"吗？此操作不可恢复！`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        await api.delete(`/api/exams/${exam.id}/`)

        exams.value = exams.value.filter(e => e.id !== exam.id)
        totalExams.value = exams.value.length
        ElMessage.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    const getQuestionTypeName = (type) => {
      const typeMap = {
        'multiple': '单选题',
        'multiple_choice': '多选题',
        'fill': '填空题',
        'essay': '简答题'
      }
      return typeMap[type] || type
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString('zh-CN')
    }

    const checkPermissions = async () => {
      // 确保用户已登录
      if (!userStore.isAuthenticated) {
        await userStore.initUser()
      }
      
      // 检查是否有查看考试的权限
      hasExamPermission.value = userStore.hasPermission(PERMISSIONS.VIEW_EXAMS)
      
      console.log('用户权限检查结果:', {
        isAuthenticated: userStore.isAuthenticated,
        userRole: userStore.currentUser?.role,
        hasExamPermission: hasExamPermission.value,
        allPermissions: userStore.currentUser?.permissions
      })
      
      if (!hasExamPermission.value) {
        ElMessage.warning('您没有查看试卷管理的权限')
        // 保留模拟数据以便展示界面
        exams.value = mockExams
        totalExams.value = mockExams.length
      }
    }

    onMounted(async () => {
      await checkPermissions()
      if (hasExamPermission.value) {
        loadExams()
      }
    })

    return {
      loading,
      showExamDetail,
      selectedExam,
      currentPage,
      pageSize,
      totalExams,
      exams,
      searchForm,
      filteredExams,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      goToExamEditor,
      editExam,
      viewExam,
      toggleExamStatus,
      deleteExam,
      getQuestionTypeName,
      formatDate
    }
  }
}
</script>

<style scoped>
.exam-management {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.management-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #1e3a8a;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* 确保表格文字在白色背景上清晰可见 */
.table-section :deep(.el-table) {
  color: #1e3a8a;
}

.table-section :deep(.el-table th) {
  background-color: #f8f9fa;
  color: #1e3a8a;
}

.table-section :deep(.el-table td) {
  color: #1e3a8a;
}

.table-section {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.pagination-section {
  padding: 20px;
  text-align: center;
}

.exam-detail {
  max-height: 600px;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h3 {
  margin-bottom: 15px;
  color: #1e3a8a;
  border-bottom: 2px solid #409eff;
  padding-bottom: 5px;
}

.detail-section p {
  color: #1e3a8a;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .search-section .el-col {
    margin-bottom: 10px;
  }
}
</style>
