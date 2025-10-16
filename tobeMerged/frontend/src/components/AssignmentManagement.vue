<template>
  <div class="assignment-management">
    <AdminNavigation />
    <div class="management-content">
    <div class="page-header">
      <h1>试卷分配管理</h1>
      <el-button type="primary" @click="showAssignmentDialog = true">
        <el-icon><Plus /></el-icon>
        分配试卷
      </el-button>
    </div>

    <div class="search-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索学员姓名或试卷标题"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.exam_id" placeholder="选择试卷" clearable @change="handleSearch">
            <el-option
              v-for="exam in exams"
              :key="exam.id"
              :label="exam.title"
              :value="exam.id"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.student_id" placeholder="选择学员" clearable @change="handleSearch">
            <el-option
              v-for="student in students"
              :key="student.id"
              :label="`${student.name} (${student.student_id})`"
              :value="student.id"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-col>
      </el-row>
    </div>

    <div class="table-section">
      <el-table
        :data="filteredAssignments"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="exam_title" label="试卷标题" width="200" />
        <el-table-column prop="student_name" label="学员姓名" width="120" />
        <el-table-column prop="student_id" label="学号" width="120" />
        <el-table-column prop="assigned_at" label="分配时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.assigned_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="assigned_by" label="分配人" width="120" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '有效' : '已移除' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button 
              size="small" 
              type="danger" 
              @click="removeAssignment(scope.row)"
              :disabled="!scope.row.is_active"
            >
              移除分配
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalAssignments"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 分配试卷对话框 -->
    <el-dialog
      v-model="showAssignmentDialog"
      title="分配试卷"
      width="800px"
    >
      <el-form
        ref="assignmentFormRef"
        :model="assignmentForm"
        :rules="assignmentRules"
        label-width="100px"
      >
        <el-form-item label="选择试卷" prop="exam_id">
          <el-select v-model="assignmentForm.exam_id" placeholder="请选择试卷" style="width: 100%">
            <el-option
              v-for="exam in availableExams"
              :key="exam.id"
              :label="exam.title"
              :value="exam.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="选择学员" prop="student_ids">
          <el-select 
            v-model="assignmentForm.student_ids" 
            multiple
            placeholder="请选择学员" 
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="student in availableStudents"
              :key="student.id"
              :label="`${student.name} (${student.student_id})`"
              :value="student.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="批量操作">
          <el-radio-group v-model="assignmentForm.batch_type">
            <el-radio label="individual">单独分配</el-radio>
            <el-radio label="department">按院系分配</el-radio>
            <el-radio label="grade">按年级分配</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="assignmentForm.batch_type === 'department'" label="选择院系">
          <el-select v-model="assignmentForm.department" placeholder="请选择院系" style="width: 100%">
            <el-option
              v-for="dept in departments"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
        </el-form-item>

        <el-form-item v-if="assignmentForm.batch_type === 'grade'" label="选择年级">
          <el-select v-model="assignmentForm.grade" placeholder="请选择年级" style="width: 100%">
            <el-option
              v-for="grade in grades"
              :key="grade"
              :label="grade"
              :value="grade"
            />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAssignmentDialog = false">取消</el-button>
          <el-button type="primary" @click="saveAssignment" :loading="saving">
            {{ saving ? '分配中...' : '确认分配' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 统计信息 -->
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#409eff"><Connection /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.totalAssignments }}</h3>
                <p>总分配数</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#67c23a"><User /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.assignedStudents }}</h3>
                <p>已分配学员</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#e6a23c"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.assignedExams }}</h3>
                <p>已分配试卷</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="40" color="#f56c6c"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <h3>{{ stats.activeAssignments }}</h3>
                <p>有效分配</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, Connection, User, Document, Warning } from '@element-plus/icons-vue'
import axios from 'axios'
import AdminNavigation from './AdminNavigation.vue'

export default {
  name: 'AssignmentManagement',
  components: {
    Plus,
    Search,
    Refresh,
    Connection,
    User,
    Document,
    Warning,
    AdminNavigation
  },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const showAssignmentDialog = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalAssignments = ref(0)

    const assignments = ref([])
    const exams = ref([])
    const students = ref([])
    const departments = ref(['计算机学院', '数学学院', '物理学院', '化学学院', '生物学院'])
    const grades = ref(['2021级', '2022级', '2023级', '2024级'])

    const searchForm = reactive({
      keyword: '',
      exam_id: '',
      student_id: ''
    })

    const assignmentForm = reactive({
      exam_id: '',
      student_ids: [],
      batch_type: 'individual',
      department: '',
      grade: ''
    })

    const assignmentRules = {
      exam_id: [
        { required: true, message: '请选择试卷', trigger: 'change' }
      ],
      student_ids: [
        { required: true, message: '请选择学员', trigger: 'change' }
      ]
    }

    const assignmentFormRef = ref()

    // 移除模拟数据，完全依赖数据库数据

    const loadData = async () => {
      loading.value = true
      try {
        // 从后端API获取数据
        const [assignmentsResponse, examsResponse, studentsResponse] = await Promise.all([
          axios.get('/exam-assignments/'),
          axios.get('/exams/'),
          axios.get('/students/')
        ])

        const assignmentsData = assignmentsResponse.data
        const examsData = examsResponse.data
        const studentsData = studentsResponse.data

        // 处理分页格式的数据
        if (Array.isArray(assignmentsData)) {
          assignments.value = assignmentsData
          totalAssignments.value = assignmentsData.length
        } else if (assignmentsData && Array.isArray(assignmentsData.results)) {
          assignments.value = assignmentsData.results
          totalAssignments.value = assignmentsData.count || assignmentsData.results.length
        } else {
          console.warn('分配数据格式不正确')
          assignments.value = []
          totalAssignments.value = 0
        }

        if (Array.isArray(examsData)) {
          exams.value = examsData
        } else if (examsData && Array.isArray(examsData.results)) {
          exams.value = examsData.results
        } else {
          console.warn('试卷数据格式不正确')
          exams.value = []
        }

        if (Array.isArray(studentsData)) {
          students.value = studentsData
        } else if (studentsData && Array.isArray(studentsData.results)) {
          students.value = studentsData.results
        } else {
          console.warn('学员数据格式不正确')
          students.value = []
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        ElMessage.error('加载数据失败，请检查网络连接或联系管理员')
        // 如果API调用失败，清空数据
        assignments.value = []
        exams.value = []
        students.value = []
        totalAssignments.value = 0
      } finally {
        loading.value = false
      }
    }

    const filteredAssignments = computed(() => {
      // 确保assignments.value是数组
      if (!Array.isArray(assignments.value)) {
        return []
      }
      
      let filtered = assignments.value

      if (searchForm.keyword) {
        const keyword = searchForm.keyword.toLowerCase()
        filtered = filtered.filter(assignment =>
          assignment && assignment.exam_title && assignment.exam_title.toLowerCase().includes(keyword) ||
          assignment && assignment.student_name && assignment.student_name.toLowerCase().includes(keyword) ||
          assignment && assignment.student_id && assignment.student_id.toLowerCase().includes(keyword)
        )
      }

      if (searchForm.exam_id) {
        filtered = filtered.filter(assignment => assignment && assignment.exam_id === searchForm.exam_id)
      }

      if (searchForm.student_id) {
        filtered = filtered.filter(assignment => assignment && assignment.student_id === searchForm.student_id)
      }

      return filtered
    })

    const availableExams = computed(() => {
      if (!Array.isArray(exams.value)) {
        return []
      }
      return exams.value.filter(exam => exam && exam.is_active)
    })

    const availableStudents = computed(() => {
      if (!Array.isArray(students.value)) {
        return []
      }
      return students.value
    })

    const stats = computed(() => {
      const totalAssignments = assignments.value.length
      const activeAssignments = assignments.value.filter(a => a.is_active).length
      const assignedStudents = new Set(assignments.value.map(a => a.student_id)).size
      const assignedExams = new Set(assignments.value.map(a => a.exam_id)).size

      return {
        totalAssignments,
        activeAssignments,
        assignedStudents,
        assignedExams
      }
    })

    const handleSearch = () => {
      currentPage.value = 1
    }

    const resetSearch = () => {
      searchForm.keyword = ''
      searchForm.exam_id = ''
      searchForm.student_id = ''
      currentPage.value = 1
    }

    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
    }

    const removeAssignment = async (assignment) => {
      try {
        await ElMessageBox.confirm(
          `确定要移除学员 ${assignment.student_name} 的试卷分配吗？`,
          '确认移除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        const response = await axios.post(`/exam-assignments/${assignment.id}/remove_assignment/`)

        if (response.status !== 200) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        assignment.is_active = false
        ElMessage.success('移除成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('移除失败:', error)
          ElMessage.error('移除失败')
        }
      }
    }

    const saveAssignment = async () => {
      try {
        await assignmentFormRef.value.validate()
        saving.value = true

        const exam = exams.value.find(e => e.id === assignmentForm.exam_id)
        let targetStudents = []

        if (assignmentForm.batch_type === 'individual') {
          targetStudents = students.value.filter(s => assignmentForm.student_ids.includes(s.id))
        } else if (assignmentForm.batch_type === 'department') {
          targetStudents = students.value.filter(s => s.department === assignmentForm.department)
        } else if (assignmentForm.batch_type === 'grade') {
          targetStudents = students.value.filter(s => s.grade === assignmentForm.grade)
        }

        // 批量创建分配记录
        const assignmentPromises = targetStudents.map(student => 
          axios.post('/exam-assignments/', {
            exam: assignmentForm.exam_id,
            student: student.id,
            assigned_by: 1  // 添加分配人字段，这里使用默认管理员ID
          })
        )

        const responses = await Promise.all(assignmentPromises)
        const failedResponses = responses.filter(response => response.status !== 201)

        if (failedResponses.length > 0) {
          throw new Error(`部分分配失败: ${failedResponses.length} 个失败`)
        }

        // 重新加载分配数据
        await loadData()
        
        ElMessage.success(`成功分配试卷给 ${targetStudents.length} 名学员`)
        showAssignmentDialog.value = false
        resetAssignmentForm()
      } catch (error) {
        console.error('分配失败:', error)
        ElMessage.error('分配失败')
      } finally {
        saving.value = false
      }
    }

    const resetAssignmentForm = () => {
      assignmentForm.exam_id = ''
      assignmentForm.student_ids = []
      assignmentForm.batch_type = 'individual'
      assignmentForm.department = ''
      assignmentForm.grade = ''
      assignmentFormRef.value?.resetFields()
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      loadData()
    })

    return {
      loading,
      saving,
      showAssignmentDialog,
      currentPage,
      pageSize,
      totalAssignments,
      assignments,
      exams,
      students,
      departments,
      grades,
      searchForm,
      assignmentForm,
      assignmentRules,
      assignmentFormRef,
      filteredAssignments,
      availableExams,
      availableStudents,
      stats,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      removeAssignment,
      saveAssignment,
      formatDate
    }
  }
}
</script>

<style scoped>
.assignment-management {
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
  margin-bottom: 20px;
}

.pagination-section {
  padding: 20px;
  text-align: center;
}

.stats-section {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 20px;
}

.stat-info h3 {
  font-size: 28px;
  color: #1e3a8a;
  margin: 0 0 5px 0;
}

.stat-info p {
  color: #1e3a8a;
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .search-section .el-col {
    margin-bottom: 10px;
  }
  
  .stats-section .el-col {
    margin-bottom: 20px;
  }
}
</style>
