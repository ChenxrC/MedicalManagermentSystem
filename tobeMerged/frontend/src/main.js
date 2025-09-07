import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './styles/global.scss'

const app = createApp(App)
const pinia = createPinia()

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 全局事件监听，用于调试输入框问题
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM加载完成')
  
  // 监听全局键盘事件
  document.addEventListener('keydown', (e) => {
    console.log('全局键盘事件:', e.key, e.target.tagName, e.target.className)
  })
  
  // 监听全局输入事件
  document.addEventListener('input', (e) => {
    console.log('全局输入事件:', e.target.value, e.target.tagName, e.target.className)
  })
  
  // 监听全局焦点事件
  document.addEventListener('focusin', (e) => {
    console.log('全局获得焦点:', e.target.tagName, e.target.className)
  })
  
  document.addEventListener('focusout', (e) => {
    console.log('全局失去焦点:', e.target.tagName, e.target.className)
  })
})

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
