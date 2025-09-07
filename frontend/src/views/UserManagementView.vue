<template>
  <div class="user-management page-container">
    <el-card class="header-card enhanced-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">人员管理</span>
          <el-button 
            v-if="userRole === 'admin'" 
            type="primary" 
            class="enhanced-button"
            @click="onCreateUser"
          >
            添加用户
          </el-button>
        </div>
      </template>
      <div class="card-content">
        <el-table :data="users" style="width: 100%;" v-loading="loading" stripe class="enhanced-table">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="role" label="角色" />
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button 
                v-if="userRole === 'admin'" 
                size="small" 
                class="enhanced-button"
                @click="onEdit(scope.row)"
              >
                编辑
              </el-button>
              <el-button 
                v-if="userRole === 'admin'" 
                size="small" 
                type="danger" 
                class="enhanced-button"
                @click="onDelete(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <!-- 创建/编辑用户对话框 -->
    <el-dialog v-model="userDialogVisible" :title="editingUser ? '编辑用户' : '创建用户'" width="500px" class="enhanced-dialog">
      <el-form :model="userForm" :rules="userRules" ref="userForm" label-width="80px" class="enhanced-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="!!editingUser"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="学生" value="student"></el-option>
            <el-option label="教师" value="teacher"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!editingUser">
          <el-input v-model="userForm.password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="userDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveUser" :loading="saving">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="500px" class="enhanced-dialog">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordForm" label-width="80px" class="enhanced-form">
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="changePassword" :loading="changingPassword">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { getUsers, createUser, updateUser, deleteUser, changeUserPassword } from '@/services/api'
import { getUserInfo } from '@/services/auth'

export default {
  name: 'UserManagementView',
  data() {
    return {
      users: [],
      loading: false,
      saving: false,
      changingPassword: false,
      userRole: '',
      userDialogVisible: false,
      passwordDialogVisible: false,
      editingUser: null,
      userForm: {
        username: '',
        email: '',
        role: '',
        password: ''
      },
      passwordForm: {
        user_id: null,
        new_password: ''
      },
      userRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少6位', trigger: 'blur' }
        ]
      },
      passwordRules: {
        new_password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少6位', trigger: 'blur' }
        ]
      }
    }
  },
  async created() {
    // 获取用户角色
    const userInfo = getUserInfo()
    if (userInfo) {
      this.userRole = userInfo.role
    }
    
    // 获取用户列表
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await getUsers()
        this.users = response.data.users
      } catch (error) {
        this.$message.error('获取用户列表失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    onCreateUser() {
      this.editingUser = null
      this.userForm = { username: '', email: '', role: '', password: '' }
      this.userDialogVisible = true
    },
    onEdit(row) {
      this.editingUser = row
      this.userForm = { 
        username: row.username, 
        email: row.email, 
        role: row.role,
        password: ''
      }
      this.userDialogVisible = true
    },
    async saveUser() {
      this.$refs.userForm.validate(async (valid) => {
        if (valid) {
          this.saving = true
          try {
            let response
            if (this.editingUser) {
              // 更新用户
              response = await updateUser(this.editingUser.id, {
                username: this.userForm.username,
                email: this.userForm.email,
                role: this.userForm.role
              })
            } else {
              // 创建用户
              response = await createUser(this.userForm)
            }
            
            this.$message.success(response.data.message)
            this.userDialogVisible = false
            await this.fetchUsers()
          } catch (error) {
            this.$message.error((error.response?.data?.message || error.message))
          } finally {
            this.saving = false
          }
        }
      })
    },
    onDelete(row) {
      this.$confirm('确定要删除用户 "' + row.username + '" 吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const response = await deleteUser(row.id)
          this.$message.success(response.data.message)
          await this.fetchUsers()
        } catch (error) {
          this.$message.error((error.response?.data?.message || error.message))
        }
      }).catch(() => {
        // 用户取消删除
      })
    },
    onChangePassword(row) {
      this.passwordForm.user_id = row.id
      this.passwordForm.new_password = ''
      this.passwordDialogVisible = true
    },
    async changePassword() {
      this.$refs.passwordForm.validate(async (valid) => {
        if (valid) {
          this.changingPassword = true
          try {
            const response = await changeUserPassword(this.passwordForm.user_id, {
              new_password: this.passwordForm.new_password
            })
            
            this.$message.success(response.data.message)
            this.passwordDialogVisible = false
          } catch (error) {
            this.$message.error((error.response?.data?.message || error.message))
          } finally {
            this.changingPassword = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
}
</style>