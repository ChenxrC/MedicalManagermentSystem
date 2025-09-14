// 简单的API测试脚本
const axios = require('axios');

// 设置axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
});

// 测试函数
async function testApiEndpoints() {
  console.log('开始测试API端点...\n');
  
  try {
    // 测试用户信息端点
    console.log('1. 测试用户信息端点 (/api/auth/me):');
    try {
      const response = await api.get('/api/auth/me');
      console.log('  状态码:', response.status);
      console.log('  响应数据:', response.data);
    } catch (error) {
      console.log('  测试失败:', error.response?.status || error.message);
      console.log('  这是预期的，因为我们没有登录凭证');
    }
    
    // 测试登录端点（使用示例凭据）
    console.log('\n2. 测试登录端点 (/api/auth/login):');
    try {
      const response = await api.post('/api/auth/login', {
        username: 'testuser', // 这里使用实际存在的用户名
        password: 'testpassword' // 这里使用实际密码
      });
      console.log('  状态码:', response.status);
      console.log('  响应数据:', response.data);
    } catch (error) {
      console.log('  测试失败:', error.response?.status || error.message);
      console.log('  这可能是因为测试凭据无效');
    }
    
    // 测试登出端点
    console.log('\n3. 测试登出端点 (/api/logout/):');
    try {
      const response = await api.post('/api/logout/');
      console.log('  状态码:', response.status);
      console.log('  响应数据:', response.data);
    } catch (error) {
      console.log('  测试失败:', error.response?.status || error.message);
    }
    
    console.log('\nAPI测试完成!');
  } catch (error) {
    console.error('测试过程中发生错误:', error);
  }
}

// 运行测试
if (require.main === module) {
  testApiEndpoints();
}

module.exports = { testApiEndpoints };