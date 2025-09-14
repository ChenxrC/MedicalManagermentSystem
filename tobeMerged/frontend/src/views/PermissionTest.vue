<template>
  <div class="permission-test-container">
    <el-card class="permission-test-card">
      <template #header>
        <div class="card-header">
          <span>权限测试页面</span>
        </div>
      </template>
      
      <div v-if="userStore.isAuthenticated && userStore.currentUser" class="permission-content">
        <div class="user-info">
          <h3>用户信息</h3>
          <p>用户名: {{ userStore.currentUser.username }}</p>
          <p>邮箱: {{ userStore.currentUser.email }}</p>
          <p>角色: {{ userStore.currentUser.role | capitalize }}</p>
        </div>
        
        <div class="permissions-section">
          <h3>用户权限</h3>
          <div class="permission-tags">
            <el-tag v-for="permission in userStore.currentUser.permissions" :key="permission" type="success" size="small">
              {{ permission }}
            </el-tag>
          </div>
        </div>
        
        <div class="permission-checks">
          <h3>权限检查</h3>
          <el-table :data="permissionCheckResults" stripe style="width: 100%">
            <el-table-column prop="permission" label="权限名称" width="180">
            </el-table-column>
            <el-table-column prop="hasPermission" label="权限状态">
              <template #default="scope">
                <el-tag :type="scope.row.hasPermission ? 'success' : 'danger'">
                  {{ scope.row.hasPermission ? '有权限' : '无权限' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <div class="role-checks">
          <h3>角色检查</h3>
          <div class="role-check-items">
            <div class="role-check-item">
              <span>管理员角色:</span>
              <el-tag :type="userStore.hasRole('admin') ? 'success' : 'danger'">
                {{ userStore.hasRole('admin') ? '是' : '否' }}
              </el-tag>
            </div>
            <div class="role-check-item">
              <span>教师角色:</span>
              <el-tag :type="userStore.hasRole('teacher') ? 'success' : 'danger'">
                {{ userStore.hasRole('teacher') ? '是' : '否' }}
              </el-tag>
            </div>
            <div class="role-check-item">
              <span>学生角色:</span>
              <el-tag :type="userStore.hasRole('student') ? 'success' : 'danger'">
                {{ userStore.hasRole('student') ? '是' : '否' }}
              </el-tag>
            </div>
          </div>
        </div>
        
        <div class="directive-test">
          <h3>指令测试</h3>
          <div class="directive-test-items">
            <div v-permission="'view_users'" class="directive-test-item">
              <el-alert title="查看用户权限测试" type="success" show-icon>
                只有拥有 'view_users' 权限的用户才能看到此内容
              </el-alert>
            </div>
            
            <div v-role="'admin'" class="directive-test-item">
              <el-alert title="管理员角色测试" type="warning" show-icon>
                只有管理员角色的用户才能看到此内容
              </el-alert>
            </div>
            
            <div v-any-role="['admin', 'teacher']" class="directive-test-item">
              <el-alert title="管理员或教师角色测试" type="info" show-icon>
                只有管理员或教师角色的用户才能看到此内容
              </el-alert>
            </div>
            
            <div v-any-permission="['create_users', 'update_users']" class="directive-test-item">
              <el-alert title="任一管理权限测试" type="primary" show-icon>
                拥有 'create_users' 或 'update_users' 权限的用户才能看到此内容
              </el-alert>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button type="primary" @click="refreshPermissions">刷新权限</el-button>
          <el-button type="default" @click="goToDashboard">前往管理面板</el-button>
          <el-button type="danger" @click="userStore.logout">退出登录</el-button>
        </div>
      </div>
      
      <div v-else class="not-authenticated">
        <el-empty description="请先登录以查看权限信息"></el-empty>
        <el-button type="primary" @click="$router.push('/login')">登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/userStore'
import { PERMISSIONS } from '@/utils/permission.js'

export default {
  name: 'PermissionTest',
  data() {
    return {
      permissionCheckResults: []
    }
  },
  computed: {
    userStore() {
      return useUserStore()
    }
  },
  filters: {
    capitalize(value) {
      if (!value) return ''
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
  },
  mounted() {
    this.loadPermissionChecks()
  },
  methods: {
    loadPermissionChecks() {
      // 生成权限检查结果
      this.permissionCheckResults = Object.values(PERMISSIONS).map(permission => ({
        permission,
        hasPermission: this.userStore.hasPermission(permission)
      }))
    },
    
    refreshPermissions() {
      this.userStore.refreshUserPermissions().then(success => {
        if (success) {
          this.loadPermissionChecks()
          this.$message.success('权限已刷新')
        } else {
          this.$message.error('权限刷新失败')
        }
      })
    },
    
    goToDashboard() {
      if (this.userStore.hasRole('admin')) {
        this.$router.push('/admin')
      } else if (this.userStore.hasRole('teacher')) {
        this.$router.push('/teacher')
      } else {
        this.$message.warning('您没有管理面板的访问权限')
      }
    }
  }
}
</script>

<style scoped>
.permission-test-container {
  padding: 20px;
  min-height: calc(100vh - 80px);
}

.permission-test-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.permission-content {
  padding: 20px 0;
}

.user-info {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.user-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}

.permissions-section {
  margin-bottom: 20px;
}

.permissions-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}

.permission-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.permission-checks {
  margin-bottom: 20px;
}

.permission-checks h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}

.role-checks {
  margin-bottom: 20px;
}

.role-checks h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}

.role-check-items {
  display: flex;
  gap: 16px;
}

.role-check-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.directive-test {
  margin-bottom: 20px;
}

.directive-test h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
}

.directive-test-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.directive-test-item {
  padding: 8px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 20px;
}

.not-authenticated {
  text-align: center;
  padding: 40px 0;
}

.not-authenticated .el-empty {
  margin-bottom: 20px;
}
</style>