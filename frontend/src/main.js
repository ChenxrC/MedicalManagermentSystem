import { createApp } from 'vue'
// 猴子补丁: 捕获ResizeObserver循环错误 - 添加调试日志
console.log('Applying ResizeObserver monkey-patch');
const originalResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends originalResizeObserver {
  constructor(callback) {
    console.log('ResizeObserver instance created with monkey-patch');
    super((entries, observer) => {
      // 使用requestAnimationFrame打破ResizeObserver循环
      requestAnimationFrame(() => {
        try {
          callback(entries, observer);
        } catch (e) {
          if (e.message.includes('ResizeObserver loop completed with undelivered notifications')) {
            console.log('Caught ResizeObserver loop error, suppressing...');
            // 仅在开发环境打印调试信息
            if (process.env.NODE_ENV !== 'production') {
              console.debug('Suppressed ResizeObserver error:', e);
            }
          } else {
            throw e;
          }
        }
      });
    });
  }
};

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/global.scss'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(ElementPlus)
app.use(router)

// 全局错误处理兜底
window.addEventListener('error', (e) => {
  if (e.message && e.message.includes('ResizeObserver loop completed with undelivered notifications')) {
    e.preventDefault();
    e.stopPropagation();
  }
});

// 处理ResizeObserver特定错误
window.addEventListener('resizeobservererror', (e) => {
  if (e.message && e.message.includes('ResizeObserver loop completed with undelivered notifications')) {
    e.preventDefault();
    e.stopPropagation();
  }
});

app.mount('#app')