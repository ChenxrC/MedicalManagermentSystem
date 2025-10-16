<template>
  <div class="permission-management">
    <AdminNavigation />
    <div class="management-content">
      <div class="page-header">
        <h1>权限管理</h1>
      </div>

      <div class="search-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索用户名、姓名或邮箱"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchForm.role" placeholder="选择角色" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="管理员" value="admin" />
              <el-option label="老师" value="teacher" />
              <el-option label="学生" value="student" />
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
          :data="usersData"
          v-loading="loading"
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" width="150" />
          <el-table-column prop="email" label="邮箱" width="200" />
          <el-table-column prop="role" label="角色" width="120">
            <template #default="scope">
              <el-tag
                :type="roleType(scope.row.role)"
                size="small"
              >
                {{ roleText(scope.row.role) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="first_name" label="姓名" width="120" />
          <el-table-column prop="last_name" label="姓氏" width="120" />
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" type="primary" @click="managePermissions(scope.row)">
                管理权限
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-section">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="totalUsers"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 权限管理对话框 -->
      <el-dialog
        v-model="showPermissionDialog"
        title="管理用户权限"
        width="800px"
      >
        <div class="permission-dialog-content">
          <div class="user-basic-info">
            <h3>{{ selectedUser?.username }}</h3>
            <p>{{ selectedUser?.email }}</p>
            <p>当前角色：<el-tag :type="roleType(selectedUser?.role)">{{ roleText(selectedUser?.role) }}</el-tag></p>
          </div>

          <div class="permissions-categories">
            <div class="category-section">
              <h4>用户管理权限</h4>
              <el-checkbox-group v-model="currentPermissions" class="permissions-grid">
                <el-checkbox label="view_users">查看用户</el-checkbox>
                <el-checkbox label="create_users">创建用户</el-checkbox>
                <el-checkbox label="update_users">更新用户</el-checkbox>
                <el-checkbox label="delete_users">删除用户</el-checkbox>
              </el-checkbox-group>
            </div>

            <div class="category-section">
              <h4>课程管理权限</h4>
              <el-checkbox-group v-model="currentPermissions" class="permissions-grid">
                <el-checkbox label="view_courses">查看课程</el-checkbox>
                <el-checkbox label="create_courses">创建课程</el-checkbox>
                <el-checkbox label="update_courses">更新课程</el-checkbox>
                <el-checkbox label="delete_courses">删除课程</el-checkbox>
              </el-checkbox-group>
            </div>

            <div class="category-section">
              <h4>文档管理权限</h4>
              <el-checkbox-group v-model="currentPermissions" class="permissions-grid">
                <el-checkbox label="view_documents">查看文档</el-checkbox>
                <el-checkbox label="create_documents">创建文档</el-checkbox>
                <el-checkbox label="update_documents">更新文档</el-checkbox>
                <el-checkbox label="delete_documents">删除文档</el-checkbox>
              </el-checkbox-group>
            </div>

            <div class="category-section">
              <h4>考试管理权限</h4>
              <el-checkbox-group v-model="currentPermissions" class="permissions-grid">
                <el-checkbox label="view_exams">查看考试</el-checkbox>
                <el-checkbox label="create_exams">创建考试</el-checkbox>
                <el-checkbox label="update_exams">更新考试</el-checkbox>
                <el-checkbox label="delete_exams">删除考试</el-checkbox>
              </el-checkbox-group>
            </div>

            <div class="category-section">
              <h4>成绩管理权限</h4>
              <el-checkbox-group v-model="currentPermissions" class="permissions-grid">
                <el-checkbox label="view_results">查看成绩</el-checkbox>
                <el-checkbox label="take_exams">参加考试</el-checkbox>
              </el-checkbox-group>
            </div>

            <div class="category-section">
              <h4>系统管理权限</h4>
              <el-checkbox-group v-model="currentPermissions" class="permissions-grid">
                <el-checkbox label="manage_system">管理系统</el-checkbox>
              </el-checkbox-group>
            </div>
          </div>

          <div class="role-defaults-section">
            <h4>角色默认权限</h4>
            <el-radio-group v-model="roleDefaults" @change="applyRoleDefaults">
              <el-radio :label="'admin'">管理员默认权限</el-radio>
              <el-radio :label="'teacher'">老师默认权限</el-radio>
              <el-radio :label="'student'">学生默认权限</el-radio>
              <el-radio :label="''">自定义</el-radio>
            </el-radio-group>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showPermissionDialog = false">取消</el-button>
            <el-button type="primary" @click="savePermissions" :loading="saving">
              {{ saving ? '保存中...' : '保存' }}
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { ElMessage } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import AdminNavigation from './AdminNavigation.vue'
import { getUsers, updateUserPermissions, getRoleDefaultPermissions } from '@/services/userService'

export default {
  name: 'PermissionManagement',
  components: {
    Search,
    Refresh,
    AdminNavigation
  },
  setup() {
    const userStore = useUserStore()
    
    // 数据状态
    const users = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalUsers = ref(0)
    
    // 搜索表单
    const searchForm = ref({
      keyword: '',
      role: ''
    })
    
    // 对话框状态
    const showPermissionDialog = ref(false)
    const selectedUser = ref(null)
    const currentPermissions = ref([])
    const roleDefaults = ref('')
    
    // 角色默认权限
    const roleDefaultPermissions = getRoleDefaultPermissions()
    
    // 过滤后的用户数据
    const usersData = computed(() => {
      return users.value.filter(user => {
        const matchesKeyword = !searchForm.value.keyword || 
          user.username.includes(searchForm.value.keyword) ||
          user.email.includes(searchForm.value.keyword) ||
          (user.first_name && user.first_name.includes(searchForm.value.keyword)) ||
          (user.last_name && user.last_name.includes(searchForm.value.keyword))
        
        const matchesRole = !searchForm.value.role || user.role === searchForm.value.role
        
        return matchesKeyword && matchesRole
      })
    })
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    }
    
    // 角色标签类型
    const roleType = (role) => {
      switch (role) {
        case 'admin': return 'danger'
        case 'teacher': return 'primary'
        case 'student': return 'success'
        default: return ''
      }
    }
    
    // 角色文本
    const roleText = (role) => {
      switch (role) {
        case 'admin': return '管理员'
        case 'teacher': return '老师'
        case 'student': return '学生'
        default: return role
      }
    }
    
    // 获取用户列表
    const fetchUsers = async () => {
      loading.value = true
      try {
        const usersData = await getUsers()
        users.value = usersData
        totalUsers.value = users.value.length
      } catch (error) {
        console.error('获取用户列表失败:', error)
        ElMessage.error('获取用户列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 搜索用户
    const handleSearch = () => {
      currentPage.value = 1
    }
    
    // 重置搜索
    const resetSearch = () => {
      searchForm.value = {
        keyword: '',
        role: ''
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
    
    // 管理用户权限
    const managePermissions = (user) => {
      selectedUser.value = { ...user }
      // 获取用户当前权限，如果没有则设置为角色默认权限
      currentPermissions.value = user.permissions || roleDefaultPermissions[user.role] || []
      roleDefaults.value = user.role
      showPermissionDialog.value = true
    }
    
    // 应用角色默认权限
    const applyRoleDefaults = (role) => {
      if (role && roleDefaultPermissions[role]) {
        currentPermissions.value = [...roleDefaultPermissions[role]]
      }
    }
    
    // 保存用户权限
    const savePermissions = async () => {
      if (!selectedUser.value) return
      
      saving.value = true
      try {
        const userData = {
          permissions: currentPermissions.value
        }
        
        await updateUserPermissions(selectedUser.value.id, userData)
        ElMessage.success('权限更新成功')
        showPermissionDialog.value = false
        await fetchUsers()
        
        // 刷新当前用户的权限信息
        await userStore.refreshUserPermissions()
      } catch (error) {
        console.error('更新权限失败:', error)
        ElMessage.error('更新失败')
      } finally {
        saving.value = false
      }
    }
    
    // 初始化
    onMounted(() => {
      fetchUsers()
    })
    
    return {
      usersData,
      loading,
      saving,
      currentPage,
      pageSize,
      totalUsers,
      searchForm,
      showPermissionDialog,
      selectedUser,
      currentPermissions,
      roleDefaults,
      formatDate,
      roleType,
      roleText,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      managePermissions,
      applyRoleDefaults,
      savePermissions
    }
  }
}
</script>

<style scoped>
.permission-management {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.management-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-section {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.permission-dialog-content {
  padding: 10px 0;
}

.user-basic-info {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.user-basic-info h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: bold;
}

.user-basic-info p {
  margin: 4px 0;
  color: #606266;
}

.permissions-categories {
  margin-bottom: 20px;
}

.category-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.category-section h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.role-defaults-section {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.role-defaults-section h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
}

.role-defaults-section .el-radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>