<template>
  <div class="exam-assignment">
    <AdminNavigation />
    <div class="assignment-content">
      <div class="page-header">
        <h1>试卷分配管理</h1>
        <el-button type="primary" @click="showAssignDialog = true">
          <el-icon><Plus /></el-icon>
          分配试卷
        </el-button>
      </div>

      <div class="search-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索试卷名称或学员姓名"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchForm.status" placeholder="分配状态" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="已分配" value="assigned" />
              <el-option label="已完成" value="completed" />
              <el-option label="已过期" value="expired" />
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
          <el-table-column prop="exam.title" label="试卷名称" width="200" />
          <el-table-column prop="student.username" label="学员账号" width="150" />
          <el-table-column prop="student.first_name" label="学员姓名" width="120" />
          <el-table-column prop="assigned_at" label="分配时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.assigned_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="due_date" label="截止日期" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.due_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag
                :type="getStatusType(scope.row.status)"
                size="small"
              >
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewAssignment(scope.row)">
                查看详情
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="deleteAssignment(scope.row)"
              >
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
            :total="totalAssignments"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 分配试卷对话框 -->
      <el-dialog
        v-model="showAssignDialog"
        title="分配试卷给学员"
        width="800px"
      >
        <el-form
          ref="assignFormRef"
          :model="assignForm"
          :rules="assignRules"
          label-width="100px"
        >
          <el-form-item label="选择试卷" prop="exam_id">
            <el-select v-model="assignForm.exam_id" placeholder="请选择试卷" filterable>
              <el-option
                v-for="exam in exams"
                :key="exam.id"
                :label="exam.title"
                :value="exam.id"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="选择学员" prop="student_ids">
            <el-select v-model="assignForm.student_ids" placeholder="请选择学员" multiple filterable collapse-tags>
              <el-option
                v-for="student in students"
                :key="student.id"
                :label="`${student.username} - ${student.first_name || student.username}`"
                :value="student.id"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="截止日期" prop="due_date">
            <el-date-picker
              v-model="assignForm.due_date"
              type="datetime"
              placeholder="选择截止日期"
              :default-time="'23:59:59'"
            />
          </el-form-item>
          
          <el-form-item label="备注">
            <el-input
              v-model="assignForm.note"
              type="textarea"
              placeholder="可选，填写分配说明"
              :rows="2"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showAssignDialog = false">取消</el-button>
            <el-button type="primary" @click="saveAssignment" :loading="saving">
              确认分配
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/userStore'
import api from '@/utils/axios'

// Mock数据，用于演示
const mockAssignments = [
  {
    id: 1,
    exam: { id: 1, title: 'JavaScript基础测试' },
    student: { id: 1, username: 'student1', first_name: '张三', last_name: '张' },
    assigned_at: '2024-01-10T09:00:00Z',
    due_date: '2024-01-15T23:59:59Z',
    status: 'assigned'
  },
  {
    id: 2,
    exam: { id: 2, title: 'Vue.js框架考试' },
    student: { id: 2, username: 'student2', first_name: '李四', last_name: '李' },
    assigned_at: '2024-01-05T14:30:00Z',
    due_date: '2024-01-10T23:59:59Z',
    status: 'completed'
  }
]

const mockExams = [
  { id: 1, title: 'JavaScript基础测试' },
  { id: 2, title: 'Vue.js框架考试' },
  { id: 3, title: 'Python编程基础' }
]

const mockStudents = [
  { id: 1, username: 'student1', first_name: '张三' },
  { id: 2, username: 'student2', first_name: '李四' },
  { id: 3, username: 'student3', first_name: '王五' }
]

export default {
  name: 'ExamAssignment',
  setup() {
    const userStore = useUserStore()
    const assignments = ref([])
    const exams = ref([])
    const students = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalAssignments = ref(0)
    const showAssignDialog = ref(false)
    const assignFormRef = ref()
    
    const searchForm = ref({
      keyword: '',
      status: ''
    })
    
    const assignForm = ref({
      exam_id: '',
      student_ids: [],
      due_date: '',
      note: ''
    })
    
    const assignRules = ref({
      exam_id: [
        { required: true, message: '请选择试卷', trigger: 'change' }
      ],
      student_ids: [
        { required: true, message: '请选择至少一名学员', trigger: 'change' }
      ],
      due_date: [
        { required: true, message: '请选择截止日期', trigger: 'change' }
      ]
    })
    
    // 过滤后的分配数据
    const filteredAssignments = computed(() => {
      return assignments.value.filter(assignment => {
        const matchesKeyword = !searchForm.value.keyword || 
          assignment.exam?.title?.includes(searchForm.value.keyword) ||
          assignment.student?.username?.includes(searchForm.value.keyword) ||
          assignment.student?.first_name?.includes(searchForm.value.keyword)
        
        const matchesStatus = !searchForm.value.status || assignment.status === searchForm.value.status
        
        return matchesKeyword && matchesStatus
      })
    })
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    }
    
    // 状态标签类型
    const getStatusType = (status) => {
      switch (status) {
        case 'assigned': return 'primary'
        case 'completed': return 'success'
        case 'expired': return 'danger'
        default: return ''
      }
    }
    
    // 状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'assigned': return '已分配'
        case 'completed': return '已完成'
        case 'expired': return '已过期'
        default: return status
      }
    }
    
    // 获取试卷分配列表
    const fetchAssignments = async () => {
      loading.value = true
      try {
        // 尝试从API获取数据
        const response = await api.get('/exam-assignments')
        // 确保正确获取数据格式
        if (response.data && response.data.results) {
          assignments.value = response.data.results
          totalAssignments.value = response.data.count
        } else {
          assignments.value = response.data || mockAssignments
          totalAssignments.value = assignments.value.length
        }
      } catch (error) {
        console.error('获取试卷分配列表失败:', error)
        ElMessage.error('获取试卷分配列表失败，使用模拟数据')
        // 如果API调用失败，使用模拟数据
        assignments.value = mockAssignments
        totalAssignments.value = mockAssignments.length
      } finally {
        loading.value = false
      }
    }
    
    // 获取试卷列表
    const fetchExams = async () => {
      try {
        // 尝试从API获取数据
        const response = await api.get('/exams')
        // 确保正确获取数据格式
        if (response.data && response.data.results) {
          exams.value = response.data.results
        } else {
          exams.value = response.data || mockExams
        }
      } catch (error) {
        console.error('获取试卷列表失败:', error)
        // 如果API调用失败，使用模拟数据
        exams.value = mockExams
      }
    }
    
    // 获取学员列表
    const fetchStudents = async () => {
      try {
        // 尝试从API获取数据
        const response = await api.get('/users?role=student')
        // 确保正确获取数据格式
        if (response.data && response.data.users) {
          students.value = response.data.users
        } else {
          students.value = response.data || mockStudents
        }
      } catch (error) {
        console.error('获取学员列表失败:', error)
        // 如果API调用失败，使用模拟数据
        students.value = mockStudents
      }
    }
    
    // 保存试卷分配
    const saveAssignment = async () => {
      if (!assignFormRef.value) return
      
      try {
        await assignFormRef.value.validate()
        saving.value = true
        
        // 遍历选中的学员，为每个学员创建一个分配记录
        const promises = assignForm.value.student_ids.map(studentId => {
          const assignmentData = {
            exam_id: assignForm.value.exam_id,
            student_id: studentId,
            due_date: assignForm.value.due_date,
            note: assignForm.value.note
          }
          return api.post('/exam-assignments', assignmentData)
        })
        
        await Promise.all(promises)
        
        ElMessage.success('试卷分配成功')
        showAssignDialog.value = false
        resetAssignForm()
        await fetchAssignments()
      } catch (error) {
        console.error('试卷分配失败:', error)
        ElMessage.error('试卷分配失败')
      } finally {
        saving.value = false
      }
    }
    
    // 重置分配表单
    const resetAssignForm = () => {
      assignForm.value = {
        exam_id: '',
        student_ids: [],
        due_date: '',
        note: ''
      }
      if (assignFormRef.value) {
        assignFormRef.value.resetFields()
      }
    }
    
    // 删除试卷分配
    const deleteAssignment = async (assignment) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除试卷「${assignment.exam?.title}」给学员「${assignment.student?.first_name}」的分配吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await api.delete(`/exam-assignments/${assignment.id}`)
        ElMessage.success('删除成功')
        await fetchAssignments()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }
    
    // 查看分配详情
    const viewAssignment = (assignment) => {
      ElMessage.info(`查看试卷分配ID: ${assignment.id} 的详情`)
      // 这里可以实现查看详情的逻辑，比如打开详情对话框
    }
    
    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.value = {
        keyword: '',
        status: ''
      }
      currentPage.value = 1
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
    }
    
    // 初始化
    onMounted(async () => {
      await Promise.all([
        fetchAssignments(),
        fetchExams(),
        fetchStudents()
      ])
    })
    
    return {
      assignments,
      exams,
      students,
      loading,
      saving,
      currentPage,
      pageSize,
      totalAssignments,
      showAssignDialog,
      assignFormRef,
      searchForm,
      assignForm,
      assignRules,
      filteredAssignments,
      formatDate,
      getStatusType,
      getStatusText,
      fetchAssignments,
      saveAssignment,
      deleteAssignment,
      viewAssignment,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.exam-assignment {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.assignment-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px 0;
}

.search-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.table-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
}

.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>