import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './styles/global.scss'
import { debugAPI } from './utils/debug.js'
import { setupPermissionDirective } from './utils/permission.js'

// 创建应用实例和Pinia存储
const pinia = createPinia()

// 尝试初始化应用并处理可能的错误
try {
  const app = createApp(App)
  
  // 注册所有图标
  for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
  
  // 全局事件监听（简化版，移除过多日志）
  document.addEventListener('DOMContentLoaded', () => {
    // 记录浏览器环境信息用于调试
    debugAPI.logBrowserEnvironment()
  })
  
  // 使用插件
  app.use(pinia)
  app.use(router)
  app.use(ElementPlus)
  
  // 注册权限指令
  setupPermissionDirective(app)
  
  app.mount('#app')
  
} catch (error) {
  console.error('应用初始化错误:', error)
  
  // 处理MetaMask相关错误
  if (debugAPI.handleExtensionErrors(error)) {
    // 如果是MetaMask错误，尝试重新初始化应用
    setTimeout(() => {
      try {
        const app = createApp(App)
        app.use(pinia)
        app.use(router)
        app.use(ElementPlus)
        
        // 注册权限指令
        setupPermissionDirective(app)
        
        app.mount('#app')
      } catch (retryError) {
        console.error('重新初始化应用失败:', retryError)
      }
    }, 100)
  }
}
