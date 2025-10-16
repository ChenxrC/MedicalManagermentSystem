<template>
  <div class="student-management">
    <AdminNavigation />
    <div class="management-content">
    <div class="page-header">
      <h1>学员管理</h1>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加学员
      </el-button>
    </div>

    <div class="search-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索账号、姓名或邮箱"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.department" placeholder="选择地区" clearable @change="handleSearch">
            <el-option
              v-for="dept in departments"
              :key="dept"
              :label="dept"
              :value="dept"
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
        :data="filteredStudents"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="student_id" label="账号" width="120" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="phone" label="电话" width="120" />
        <el-table-column prop="department" label="地区" width="150" />
        <el-table-column prop="major" label="部门" width="150" />
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="editStudent(scope.row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteStudent(scope.row)">
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
          :total="totalStudents"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 添加/编辑学员对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingStudent ? '编辑学员' : '添加学员'"
      width="600px"
    >
      <el-form
        ref="studentFormRef"
        :model="studentForm"
        :rules="studentRules"
        label-width="100px"
      >
        <el-form-item label="账号" prop="student_id">
          <el-input v-model="studentForm.student_id" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="studentForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="studentForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="studentForm.phone" placeholder="请输入电话（可选）" />
        </el-form-item>
        <el-form-item label="地区" prop="department">
          <el-select v-model="studentForm.department" placeholder="请选择地区（可选）" style="width: 100%">
            <el-option
              v-for="dept in departments"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部门" prop="major">
          <el-input v-model="studentForm.major" placeholder="请输入部门（可选）" />
        </el-form-item>
        <el-form-item label="年级" prop="grade">
          <el-select v-model="studentForm.grade" placeholder="请选择年级（可选）" style="width: 100%">
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
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="saveStudent" :loading="saving">
            {{ saving ? '保存中...' : '保存' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import AdminNavigation from './AdminNavigation.vue'
import axios from 'axios'

export default {
  name: 'StudentManagement',
  components: {
    Plus,
    Search,
    Refresh,
    AdminNavigation
  },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const showAddDialog = ref(false)
    const editingStudent = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalStudents = ref(0)

    const students = ref([])
    const departments = ref(['北京', '上海', '深圳', '广州', '杭州', '成都', '武汉', '西安'])
    const grades = ref(['2021级', '2022级', '2023级', '2024级'])

    const searchForm = reactive({
      keyword: '',
      department: '',
      grade: ''
    })

    const studentForm = reactive({
      student_id: '',
      name: '',
      email: '',
      phone: '',
      department: '',
      major: '',
      grade: ''
    })

    const studentRules = {
      student_id: [
        { required: true, message: '请输入账号', trigger: 'blur' },
        { min: 3, max: 20, message: '账号长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ]
      // 其他字段为可选，不添加验证规则
    }

    const studentFormRef = ref()

    // 模拟学员数据
    const mockStudents = [
      {
        id: 1,
        student_id: 'user001',
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '13800138001',
        department: '北京',
        major: '技术部',
        grade: '2021级',
        created_at: '2024-01-15T10:00:00Z'
      },
      {
        id: 2,
        student_id: 'user002',
        name: '李四',
        email: 'lisi@example.com',
        phone: '13800138002',
        department: '上海',
        major: '市场部',
        grade: '2021级',
        created_at: '2024-01-16T10:00:00Z'
      },
      {
        id: 3,
        student_id: 'user003',
        name: '王五',
        email: 'wangwu@example.com',
        phone: '13800138003',
        department: '深圳',
        major: '产品部',
        grade: '2022级',
        created_at: '2024-01-17T10:00:00Z'
      }
    ]

    const loadStudents = async () => {
      loading.value = true
      try {
        // 从后端API获取学员数据
        const response = await axios.get('/students/')
        
        const data = response.data
        
        // 确保数据是数组格式
        if (Array.isArray(data)) {
          students.value = data
          totalStudents.value = data.length
        } else if (data && Array.isArray(data.results)) {
          students.value = data.results
          totalStudents.value = data.count || data.results.length
        } else {
          // 如果数据格式不正确，使用模拟数据
          console.warn('API返回的数据格式不正确，使用模拟数据')
          students.value = mockStudents
          totalStudents.value = mockStudents.length
        }
      } catch (error) {
        console.error('加载学员数据失败:', error)
        ElMessage.warning('后端服务不可用，使用模拟数据')
        // 如果API调用失败，使用模拟数据
        students.value = mockStudents
        totalStudents.value = mockStudents.length
      } finally {
        loading.value = false
      }
    }

    const filteredStudents = computed(() => {
      // 确保students.value是数组
      if (!Array.isArray(students.value)) {
        return []
      }
      
      let filtered = students.value

      if (searchForm.keyword) {
        const keyword = searchForm.keyword.toLowerCase()
        filtered = filtered.filter(student =>
          student && student.student_id && student.student_id.toLowerCase().includes(keyword) ||
          student && student.name && student.name.toLowerCase().includes(keyword) ||
          student && student.email && student.email.toLowerCase().includes(keyword)
        )
      }

      if (searchForm.department) {
        filtered = filtered.filter(student => student && student.department === searchForm.department)
      }

      if (searchForm.grade) {
        filtered = filtered.filter(student => student && student.grade === searchForm.grade)
      }

      return filtered
    })

    const handleSearch = () => {
      currentPage.value = 1
    }

    const resetSearch = () => {
      searchForm.keyword = ''
      searchForm.department = ''
      searchForm.grade = ''
      currentPage.value = 1
    }

    const handleSizeChange = (val) => {
      pageSize.value = val
      currentPage.value = 1
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
    }

    const editStudent = (student) => {
      editingStudent.value = student
      Object.assign(studentForm, student)
      showAddDialog.value = true
    }

    const deleteStudent = async (student) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除学员 ${student.name} 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        const response = await fetch(`/api/students/${student.id}/`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        students.value = students.value.filter(s => s.id !== student.id)
        totalStudents.value = students.value.length
        ElMessage.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    const saveStudent = async () => {
      try {
        await studentFormRef.value.validate()
        saving.value = true

        const url = editingStudent.value 
          ? `/api/students/${editingStudent.value.id}/`
          : '/api/students/'
        
        const method = editingStudent.value ? 'PUT' : 'POST'
        
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(studentForm)
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const savedStudent = await response.json()
        
        if (editingStudent.value) {
          // 编辑模式
          const index = students.value.findIndex(s => s.id === editingStudent.value.id)
          if (index !== -1) {
            students.value[index] = savedStudent
          }
          ElMessage.success('编辑成功')
        } else {
          // 添加模式
          students.value.push(savedStudent)
          totalStudents.value = students.value.length
          ElMessage.success('添加成功')
        }

        showAddDialog.value = false
        resetForm()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      } finally {
        saving.value = false
      }
    }

    const resetForm = () => {
      editingStudent.value = null
      Object.keys(studentForm).forEach(key => {
        studentForm[key] = ''
      })
      studentFormRef.value?.resetFields()
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      loadStudents()
    })

    return {
      loading,
      saving,
      showAddDialog,
      editingStudent,
      currentPage,
      pageSize,
      totalStudents,
      students,
      departments,
      grades,
      searchForm,
      studentForm,
      studentRules,
      studentFormRef,
      filteredStudents,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      editStudent,
      deleteStudent,
      saveStudent,
      formatDate
    }
  }
}
</script>

<style scoped>
.student-management {
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
}

.pagination-section {
  padding: 20px;
  text-align: center;
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
}
</style>
