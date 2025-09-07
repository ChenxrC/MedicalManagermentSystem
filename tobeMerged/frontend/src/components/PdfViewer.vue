<template>
  <div class="pdf-viewer">
    <div class="pdf-toolbar">
      <div class="toolbar-left">
        <el-button-group>
          <el-button @click="prevPage" :disabled="currentPage <= 1">
            <ArrowLeft />
            上一页
          </el-button>
          <el-button @click="nextPage" :disabled="currentPage >= totalPages">
            下一页
            <ArrowRight />
          </el-button>
        </el-button-group>
        
        <span class="page-info">
          第 {{ currentPage }} 页，共 {{ totalPages }} 页
        </span>
      </div>
      
      <div class="toolbar-right">
        <el-button-group>
          <el-button @click="zoomOut" :disabled="scale <= 0.5">
            <ZoomOut />
          </el-button>
          <el-button @click="resetZoom">
            {{ Math.round(scale * 100) }}%
          </el-button>
          <el-button @click="zoomIn" :disabled="scale >= 3">
            <ZoomIn />
          </el-button>
        </el-button-group>
        
        <el-button @click="downloadPdf">
          <Download />
          下载
        </el-button>
      </div>
    </div>
    
         <div class="pdf-container" ref="pdfContainer">
       <div v-if="loading" class="loading-container">
         <el-skeleton :rows="10" animated />
       </div>
       
       <div v-else-if="error" class="error-container">
         <Warning class="error-icon" />
         <p>{{ error }}</p>
         <el-button @click="loadPdf" :loading="loading">
           {{ loading ? '重试中...' : '重试' }}
         </el-button>
       </div>
       
       <canvas 
         v-show="!loading && !error"
         ref="pdfCanvas"
         class="pdf-canvas"
         @wheel="handleWheel"
       ></canvas>
     </div>
    
    <div class="pdf-info">
      <h3>{{ pdf.title }}</h3>
      <div class="pdf-meta">
        <span class="file-size">{{ pdf.file_size_mb }}MB</span>
        <span class="upload-time">{{ formatDate(pdf.uploaded_at) }}</span>
      </div>
      <p v-if="pdf.description" class="description">{{ pdf.description }}</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf'

// 设置PDF.js worker路径
pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.js'

export default {
  name: 'PdfViewer',
  props: {
    pdf: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const pdfContainer = ref(null)
    const pdfCanvas = ref(null)
    const loading = ref(false)
    const error = ref(null)
    let pdfDoc = null // 不使用响应式，避免PDF.js私有属性访问问题
    const currentPage = ref(1)
    const totalPages = ref(0)
    const scale = ref(1.0)
    const retryCount = ref(0)
    const maxRetries = 3

    const pdfUrl = computed(() => props.pdf?.file_url || '')

    const isRendering = ref(false) // 渲染锁标志

    const loadPdf = async () => {
      loading.value = true
      error.value = null
      
      try {
        // 简化PDF加载配置
        const loadingTask = pdfjsLib.getDocument({
          url: pdfUrl.value
        })
        
        pdfDoc = await loadingTask.promise
        totalPages.value = pdfDoc.numPages
        currentPage.value = 1
        retryCount.value = 0 // 重置重试计数
        await renderPage()
      } catch (err) {
        console.error('PDF加载失败:', err)
        
        // 如果是版本不匹配错误，提供更详细的错误信息
        if (err.message.includes('API version') && err.message.includes('Worker version')) {
          error.value = 'PDF加载失败：PDF.js版本不匹配，请刷新页面重试'
        } else if (retryCount.value < maxRetries) {
          // 自动重试
          retryCount.value++
          error.value = `PDF加载失败，正在重试 (${retryCount.value}/${maxRetries})...`
          setTimeout(() => {
            loadPdf()
          }, 1000 * retryCount.value) // 递增延迟
          return
        } else {
          error.value = 'PDF加载失败：' + err.message
        }
      } finally {
        loading.value = false
      }
    }
    
    const renderPage = async () => {
      if (!pdfDoc || isRendering.value) return // 如果正在渲染，跳过
      
      isRendering.value = true // 上锁
      
      // 等待canvas元素渲染到DOM，最多等待1秒
      let attempts = 0
      const maxAttempts = 10
      
      while (!pdfCanvas.value && attempts < maxAttempts) {
        await nextTick()
        await new Promise(resolve => setTimeout(resolve, 100))
        attempts++
      }
      
      if (!pdfCanvas.value) {
        console.error('Canvas元素未找到，尝试次数:', attempts)
        error.value = 'Canvas元素渲染失败，请刷新页面重试'
        isRendering.value = false // 解锁
        return
      }
      
      try {
        const page = await pdfDoc.getPage(currentPage.value)
        const viewport = page.getViewport({ scale: scale.value })
        
        const canvas = pdfCanvas.value
        const context = canvas.getContext('2d')
        canvas.height = viewport.height
        canvas.width = viewport.width
        
        const renderContext = {
          canvasContext: context,
          viewport: viewport
        }
        
        await page.render(renderContext).promise
      } catch (err) {
        console.error('PDF页面渲染失败:', err)
        error.value = 'PDF页面渲染失败：' + err.message
      } finally {
        isRendering.value = false // 始终解锁
      }
    }
    
    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        renderPage()
      }
    }
    
    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        renderPage()
      }
    }
    
    const zoomIn = () => {
      if (scale.value < 3) {
        scale.value = Math.min(3, scale.value + 0.25)
        renderPage()
      }
    }
    
    const zoomOut = () => {
      if (scale.value > 0.5) {
        scale.value = Math.max(0.5, scale.value - 0.25)
        renderPage()
      }
    }
    
    const resetZoom = () => {
      scale.value = 1.0
      renderPage()
    }
    
    const handleWheel = (event) => {
      if (event.ctrlKey) {
        event.preventDefault()
        const delta = event.deltaY > 0 ? -0.1 : 0.1
        scale.value = Math.min(Math.max(scale.value + delta, 0.5), 3.0) // 限制缩放范围
        renderPage()
      }
    }
    
    const downloadPdf = () => {
      const link = document.createElement('a')
      link.href = pdfUrl.value
      link.download = props.pdf.title
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => {
      window.addEventListener('wheel', handleWheel, { passive: false })
      loadPdf()
    })
    
    onUnmounted(() => {
      window.removeEventListener('wheel', handleWheel)
      if (pdfDoc) {
        pdfDoc.destroy()
      }
    })
    
    return {
      pdfContainer,
      pdfCanvas,
      loading,
      error,
      currentPage,
      totalPages,
      scale,
      pdfUrl,
      loadPdf,
      prevPage,
      nextPage,
      zoomIn,
      zoomOut,
      resetZoom,
      handleWheel,
      downloadPdf,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.pdf-viewer {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.05);
}

.pdf-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0; // 防止被压缩
  
  // 在分屏模式下更紧凑
  @media (max-width: 1200px) {
    padding: $spacing-xs $spacing-sm;
  }
  
  // 在小屏幕上调整布局
  @media (max-width: 768px) {
    flex-direction: column;
    gap: $spacing-sm;
    padding: $spacing-sm;
    
    .toolbar-left,
    .toolbar-right {
      width: 100%;
      justify-content: center;
    }
  }
  
  .toolbar-left,
  .toolbar-right {
    display: flex;
    align-items: center;
    gap: $spacing-md;
  }
  
  .page-info {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.8);
    margin-left: $spacing-sm;
    
    // 在分屏模式下更小
    @media (max-width: 1200px) {
      font-size: 11px;
      margin-left: $spacing-xs;
    }
  }
}

.pdf-container {
  flex: 1;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-md;
  background: rgba(0, 0, 0, 0.3);
  min-height: 0; // 确保flex子元素可以收缩
  
  .loading-container {
    width: 100%;
    max-width: 600px;
  }
  
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $spacing-md;
    color: rgba(255, 255, 255, 0.8);
    
    .error-icon {
      font-size: 48px;
      color: $danger-color;
    }
    
    p {
      margin: 0;
      text-align: center;
    }
  }
  
  .pdf-canvas {
    max-width: 100%;
    max-height: 100%;
    box-shadow: $shadow-heavy;
    border-radius: $border-radius-small;
    background: #ffffff;
    object-fit: contain; // 保持宽高比
  }
}

.pdf-info {
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0; // 防止被压缩
  
  // 在分屏模式下更紧凑
  @media (max-width: 1200px) {
    padding: $spacing-xs $spacing-sm;
  }
  
  // 在小屏幕上减少内边距
  @media (max-width: 768px) {
    padding: $spacing-sm;
  }
  
  h3 {
    margin: 0 0 $spacing-xs 0;
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    
    // 在分屏模式下更小
    @media (max-width: 1200px) {
      font-size: 12px;
      margin: 0 0 4px 0;
    }
  }
  
  .pdf-meta {
    display: flex;
    gap: $spacing-sm;
    margin-bottom: $spacing-xs;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.7);
    
    // 在分屏模式下更紧凑
    @media (max-width: 1200px) {
      gap: $spacing-xs;
      font-size: 10px;
      margin-bottom: 2px;
    }
    
    .file-size {
      color: $tech-cyan;
    }
  }
  
  .description {
    margin: 0;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.3;
    
    // 在分屏模式下更小
    @media (max-width: 1200px) {
      font-size: 10px;
      line-height: 1.2;
    }
  }
}
</style>
