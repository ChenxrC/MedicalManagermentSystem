<template>
  <div class="user-management">
    <AdminNavigation />
    <div class="management-content">
      <div class="page-header">
        <h1>用户管理</h1>
        <el-button type="primary" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          添加用户
        </el-button>
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
          <el-table-column label="操作" width="300" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="editUser(scope.row)">
                编辑信息
              </el-button>
              <el-button size="small" type="primary" @click="updateUserRole(scope.row)">
                分配角色
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="deleteUser(scope.row)"
                :disabled="scope.row.id === currentUser?.id"
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
            :total="totalUsers"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 添加/编辑用户对话框 -->
      <el-dialog
        v-model="showAddDialog"
        :title="editingUser ? '编辑用户' : '添加用户'"
        width="600px"
      >
        <el-form
          ref="userFormRef"
          :model="userForm"
          :rules="userRules"
          label-width="100px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="userForm.username" placeholder="请输入用户名" :disabled="editingUser" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="userForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item 
            label="密码" 
            prop="password"
            :required="!editingUser"
          >
            <el-input 
              v-model="userForm.password" 
              placeholder="请输入密码" 
              type="password"
              :show-password="true"
              :disabled="editingUser"
            />
            <div v-if="editingUser" class="el-form-item__help">编辑用户时不需要修改密码</div>
          </el-form-item>
          <el-form-item label="姓名" prop="first_name">
            <el-input v-model="userForm.first_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="姓氏" prop="last_name">
            <el-input v-model="userForm.last_name" placeholder="请输入姓氏" />
          </el-form-item>
          <el-form-item label="简介" prop="bio">
            <el-input v-model="userForm.bio" placeholder="请输入简介" type="textarea" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showAddDialog = false">取消</el-button>
            <el-button type="primary" @click="saveUser" :loading="saving">
              {{ saving ? '保存中...' : '保存' }}
            </el-button>
          </span>
        </template>
      </el-dialog>

      <!-- 分配角色对话框 -->
      <el-dialog
        v-model="showRoleDialog"
        title="分配角色"
        width="400px"
      >
        <div class="role-dialog-content">
          <p class="user-name">{{ roleDialogData.username }}</p>
          <el-form-item label="当前角色" class="current-role">
            <el-tag :type="roleType(roleDialogData.role)">
              {{ roleText(roleDialogData.role) }}
            </el-tag>
          </el-form-item>
          <el-form-item label="新角色">
            <el-select v-model="roleDialogData.newRole" placeholder="请选择新角色" style="width: 100%">
              <el-option label="管理员" value="admin" />
              <el-option label="老师" value="teacher" />
              <el-option label="学生" value="student" />
            </el-select>
          </el-form-item>
          <div v-if="roleDialogData.role !== 'admin' && currentUser?.role === 'admin'" class="permissions-section">
            <h4>权限列表</h4>
            <div class="permissions-grid">
              <el-checkbox-group v-model="roleDialogData.permissions">
                <div v-for="permission in allPermissions" :key="permission">
                  <el-checkbox :label="permission">
                    {{ permissionText(permission) }}
                  </el-checkbox>
                </div>
              </el-checkbox-group>
            </div>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showRoleDialog = false">取消</el-button>
            <el-button type="primary" @click="confirmRoleChange" :loading="updatingRole">
              {{ updatingRole ? '更新中...' : '确认' }}
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useUserStore } from '@/stores/userStore'
import api from '@/utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { watch } from 'vue'
import AdminNavigation from './AdminNavigation.vue'

export default {
  name: 'UserManagement',
  components: {
    Plus,
    Search,
    Refresh,
    AdminNavigation
  },
  setup() {
    const userStore = useUserStore()
    const currentUser = computed(() => userStore.currentUser)
    
    // 数据状态
    const users = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const updatingRole = ref(false)
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalUsers = ref(0)
    
    // 搜索表单
    const searchForm = ref({
      keyword: '',
      role: ''
    })
    
    // 对话框状态
    const showAddDialog = ref(false)
    const showRoleDialog = ref(false)
    const editingUser = ref(null)
    
    // 用户表单
    const userFormRef = ref(null)
    const userForm = ref({
      username: '',
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      bio: ''
    })
    
    // 用户表单验证规则
    const userRules = ref({
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符之间', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
      ]
    })
    
    // 角色对话框数据
    const roleDialogData = ref({
      id: '',
      username: '',
      role: '',
      newRole: '',
      permissions: []
    })
    
    // 所有权限列表
    const allPermissions = ref([
      'view_users', 'create_users', 'update_users', 'delete_users',
      'view_courses', 'create_courses', 'update_courses', 'delete_courses',
      'view_documents', 'create_documents', 'update_documents', 'delete_documents',
      'view_exams', 'create_exams', 'update_exams', 'delete_exams',
      'view_results', 'take_exams', 'manage_system'
    ])
    
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
    
    // 权限文本
    const permissionText = (permission) => {
      const permissionMap = {
        'view_users': '查看用户',
        'create_users': '创建用户',
        'update_users': '更新用户',
        'delete_users': '删除用户',
        'view_courses': '查看课程',
        'create_courses': '创建课程',
        'update_courses': '更新课程',
        'delete_courses': '删除课程',
        'view_documents': '查看文档',
        'create_documents': '创建文档',
        'update_documents': '更新文档',
        'delete_documents': '删除文档',
        'view_exams': '查看考试',
        'create_exams': '创建考试',
        'update_exams': '更新考试',
        'delete_exams': '删除考试',
        'view_results': '查看结果',
        'take_exams': '参加考试',
        'manage_system': '管理系统'
      }
      return permissionMap[permission] || permission
    }
    
    // 获取用户列表
    const fetchUsers = async () => {
      loading.value = true
      try {
        console.log('正在请求用户列表，使用正确路径: /users')
        const response = await api.get('/users')
        console.log('API响应数据:', response.data)
        console.log('API响应状态码:', response.status)
        // 确保正确获取用户列表数据
        if (response.data && response.data.users) {
          users.value = response.data.users
        } else {
          users.value = response.data || []
        }
        totalUsers.value = users.value.length
        console.log('处理后的用户列表:', users.value)
        console.log('用户总数:', totalUsers.value)
      } catch (error) {
        console.error('获取用户列表失败:', error)
        console.error('错误详情:', error.response)
        console.error('错误消息:', error.message)
        ElMessage.error('获取用户列表失败: ' + (error.message || '未知错误'))
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
    
    // 编辑用户
    const editUser = (user) => {
      editingUser.value = { ...user }
      userForm.value = {
        username: user.username,
        email: user.email,
        password: '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        bio: user.bio || ''
      }
      showAddDialog.value = true
    }
    
    // 保存用户
    const saveUser = async () => {
      if (!userFormRef.value) return
      
      try {
        await userFormRef.value.validate()
        saving.value = true
        
        if (editingUser.value) {
          // 更新用户
          const userData = {
            email: userForm.value.email,
            first_name: userForm.value.first_name,
            last_name: userForm.value.last_name,
            bio: userForm.value.bio
          }
          
          await api.put(`/users/${editingUser.value.id}`, userData)
          ElMessage.success('用户信息更新成功')
        } else {
          // 创建用户
          const userData = {
            ...userForm.value,
            role: 'student' // 默认创建学生角色
          }
          
          await api.post('/users', userData)
          ElMessage.success('用户创建成功')
        }
        
        // 重置表单并刷新列表
        showAddDialog.value = false
        await fetchUsers()
      } catch (error) {
        console.error('保存用户失败:', error)
        ElMessage.error(error.response?.data?.error || '保存失败')
      } finally {
        saving.value = false
      }
    }
    
    // 删除用户
    const deleteUser = async (user) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除用户 "${user.username}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await api.delete(`/users/${user.id}`)
        ElMessage.success('用户删除成功')
        await fetchUsers()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除用户失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }
    
    // 角色对应的默认权限
    const roleDefaultPermissions = {
      admin: [
        'view_users', 'create_users', 'update_users', 'delete_users',
        'view_courses', 'create_courses', 'update_courses', 'delete_courses',
        'view_documents', 'create_documents', 'update_documents', 'delete_documents',
        'view_exams', 'create_exams', 'update_exams', 'delete_exams',
        'view_results', 'manage_system'
      ],
      teacher: [
        'view_users', 'view_courses', 'create_courses', 'update_courses', 'delete_courses',
        'view_documents', 'create_documents', 'update_documents', 'delete_documents',
        'view_exams', 'create_exams', 'update_exams', 'delete_exams',
        'view_results'
      ],
      student: [
        'view_courses', 'view_documents', 'view_exams', 'take_exams', 'view_results'
      ]
    }
    
    // 监听新角色变化，更新权限列表
    watch(() => roleDialogData.value.newRole, (newRole) => {
      // 当切换角色时，更新权限列表为该角色的默认权限
      roleDialogData.value.permissions = roleDefaultPermissions[newRole] || []
    })
    
    // 更新用户角色
    const updateUserRole = (user) => {
      roleDialogData.value = {
        id: user.id,
        username: user.username,
        role: user.role,
        newRole: user.role,
        permissions: roleDefaultPermissions[user.role] || []
      }
      showRoleDialog.value = true
    }
    
    // 确认角色变更
    const confirmRoleChange = async () => {
      if (roleDialogData.value.newRole === roleDialogData.value.role) {
        ElMessage.warning('未做任何更改')
        return
      }
      
      updatingRole.value = true
      try {
        const userData = {
          role: roleDialogData.value.newRole
        }
        
        await api.patch(`/users/${roleDialogData.value.id}`, userData)
        ElMessage.success('角色更新成功')
        showRoleDialog.value = false
        await fetchUsers()
        
        // 刷新当前用户的权限信息
        await userStore.refreshUserPermissions()
      } catch (error) {
        console.error('更新角色失败:', error)
        ElMessage.error('更新失败')
      } finally {
        updatingRole.value = false
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
      updatingRole,
      currentPage,
      pageSize,
      totalUsers,
      searchForm,
      showAddDialog,
      showRoleDialog,
      editingUser,
      userFormRef,
      userForm,
      userRules,
      roleDialogData,
      allPermissions,
      currentUser,
      formatDate,
      roleType,
      roleText,
      permissionText,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange,
      editUser,
      saveUser,
      deleteUser,
      updateUserRole,
      confirmRoleChange
    }
  }
}
</script>

<style scoped>
.user-management {
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

.role-dialog-content {
  padding: 10px 0;
}

.user-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
}

.current-role {
  margin-bottom: 20px;
}

.permissions-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e6e6e6;
}

.permissions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 10px;
}
</style>