<template>
  <div class="profile">
    <el-card class="profile-card">
      <div slot="header" class="clearfix">
        <span>个人资料</span>
      </div>
      <el-form :model="userInfo" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="userInfo.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userInfo.email" disabled></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-input v-model="userInfo.role" disabled></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="handleBack">返回首页</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getUserInfo } from '@/services/auth'

export default {
  name: 'ProfileView',
  data() {
    return {
      userInfo: {
        username: '',
        email: '',
        role: ''
      }
    }
  },
  mounted() {
    // 获取用户信息
    const user = getUserInfo()
    if (user) {
      this.userInfo.username = user.username
      this.userInfo.email = user.email
      this.userInfo.role = user.role
    }
  },
  methods: {
    handleBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.profile {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.profile-card {
  width: 400px;
}
</style>