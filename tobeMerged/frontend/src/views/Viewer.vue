<template>
  <div class="viewer-container">
    <!-- 顶部导航栏 -->
    <div class="header">
      <div class="header-content">
        <h1 class="title">
          <VideoPlay class="title-icon" />
          视频和PDF浏览系统
        </h1>
        <div class="header-actions">
          <el-button type="primary" @click="showUploadDialog = true">
            <Upload class="button-icon" />
            上传文件
          </el-button>
          <el-button @click="toggleFullscreen">
            <FullScreen v-if="!isFullscreen" class="button-icon" />
            <Aim v-else class="button-icon" />
            {{ isFullscreen ? '退出全屏' : '全屏模式' }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content" :class="{ 'fullscreen': isFullscreen }">
      <!-- 文件列表侧边栏 -->
      <div class="sidebar" :class="{ 'collapsed': sidebarCollapsed }">
        <div class="sidebar-header">
          <h3>文件列表</h3>
          <el-button 
            type="text" 
            @click="sidebarCollapsed = !sidebarCollapsed"
            class="collapse-btn"
          >
            <ArrowLeft v-if="!sidebarCollapsed" />
            <ArrowRight v-else />
          </el-button>
        </div>
        
                                     <div class="file-tabs">
                        <el-tabs v-model="activeTab" type="card">
             <el-tab-pane label="全部文件" name="all">
               <FileList :files="allFiles" :selectedFileId="selectedVideo?.id || selectedPdf?.id" @select-file="selectFile" />
             </el-tab-pane>
             <el-tab-pane label="视频文件" name="video">
               <FileList :files="videoFiles" :selectedFileId="selectedVideo?.id" @select-file="selectFile" />
             </el-tab-pane>
             <el-tab-pane label="PDF文件" name="pdf">
               <FileList :files="pdfFiles" :selectedFileId="selectedPdf?.id" @select-file="selectFile" />
             </el-tab-pane>
           </el-tabs>
         </div>
      </div>

      <!-- 查看器区域 -->
      <div class="viewer-area">
        <div class="viewer-toolbar">
          <div class="viewer-controls">
            <el-button-group>
              <el-button 
                :type="viewMode === 'single' ? 'primary' : ''" 
                @click="viewMode = 'single'"
              >
                单屏模式
              </el-button>
              <el-button 
                :type="viewMode === 'split' ? 'primary' : ''" 
                @click="viewMode = 'split'"
              >
                分屏模式
              </el-button>
            </el-button-group>
          </div>
          
          <div class="viewer-info" v-if="selectedVideo || selectedPdf">
            <span class="info-item">
              <VideoPlay v-if="selectedVideo" />
              <Document v-else />
              {{ selectedVideo?.title || selectedPdf?.title }}
            </span>
          </div>
        </div>

        <!-- 查看器内容 -->
        <div class="viewer-content" :class="viewMode">
          <!-- 单屏模式 -->
          <div v-if="viewMode === 'single'" class="single-viewer">
            <VideoPlayer 
              v-if="selectedVideo" 
              :video="selectedVideo" 
              @fullscreen="handleVideoFullscreen"
            />
            <PdfViewer 
              v-else-if="selectedPdf" 
              :pdf="selectedPdf"
            />
            <EmptyViewer v-else />
          </div>

          <!-- 分屏模式 -->
          <div v-else-if="viewMode === 'split'" class="split-viewer">
            <div class="split-panel left-panel">
              <div class="panel-header">
                <VideoPlay />
                视频播放
              </div>
              <VideoPlayer 
                v-if="selectedVideo" 
                :video="selectedVideo" 
                @fullscreen="handleVideoFullscreen"
              />
              <EmptyPanel v-else message="请选择视频文件" />
            </div>
            
            <div class="split-panel right-panel">
              <div class="panel-header">
                <Document />
                PDF查看
              </div>
              <PdfViewer 
                v-if="selectedPdf" 
                :pdf="selectedPdf"
              />
              <EmptyPanel v-else message="请选择PDF文件" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 上传对话框 -->
    <UploadDialog 
      v-model="showUploadDialog"
      @upload-success="handleUploadSuccess"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watchEffect } from 'vue'
import { ElMessage } from 'element-plus'
import { VideoPlay, Upload, FullScreen, Aim, Document, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import FileList from '@/components/FileList.vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import PdfViewer from '@/components/PdfViewer.vue'
import EmptyViewer from '@/components/EmptyViewer.vue'
import EmptyPanel from '@/components/EmptyPanel.vue'
import UploadDialog from '@/components/UploadDialog.vue'
import { useFileStore } from '@/stores/fileStore'

export default {
  name: 'Viewer',
  components: {
    FileList,
    VideoPlayer,
    PdfViewer,
    EmptyViewer,
    EmptyPanel,
    UploadDialog
  },
  setup() {
    const fileStore = useFileStore()
    
    // 响应式数据
    const showUploadDialog = ref(false)
    const sidebarCollapsed = ref(false)
    const activeTab = ref('all')
    const viewMode = ref('single')
    const isFullscreen = ref(false)
    const selectedVideo = ref(null)
    const selectedPdf = ref(null)
    
    // 临时：直接存储文件列表
    const filesList = ref([])

    // 监控 fileStore.files 的变化
    watchEffect(() => {
      if (Array.isArray(fileStore.files.value) && fileStore.files.value.length > 0) {
        filesList.value = [...fileStore.files.value]
      }
    })

    // 计算属性
    const allFiles = computed(() => {
      return Array.isArray(fileStore.files.value) ? fileStore.files.value : []
    })
    const videoFiles = computed(() => {
      return Array.isArray(fileStore.files.value) ? fileStore.files.value.filter(f => f.file_type === 'video') : []
    })
    const pdfFiles = computed(() => {
      return Array.isArray(fileStore.files.value) ? fileStore.files.value.filter(f => f.file_type === 'pdf') : []
    })

    // 方法
    const selectFile = (file) => {
      if (!file || !file.file_type) {
        console.warn('Invalid file object:', file)
        return
      }
      
      if (file.file_type === 'video') {
        selectedVideo.value = file
        if (viewMode.value === 'single') {
          selectedPdf.value = null
        }
      } else if (file.file_type === 'pdf') {
        selectedPdf.value = file
        if (viewMode.value === 'single') {
          selectedVideo.value = null
        }
      }
    }

    const handleUploadSuccess = (file) => {
      ElMessage.success('文件上传成功！')
      fileStore.fetchFiles().catch(err => {
        console.error('Failed to refresh files after upload:', err)
      })
    }

    const handleVideoFullscreen = () => {
      // 视频全屏处理
    }

    const toggleFullscreen = () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen()
        isFullscreen.value = true
      } else {
        document.exitFullscreen()
        isFullscreen.value = false
      }
    }

    const handleFullscreenChange = () => {
      isFullscreen.value = !!document.fullscreenElement
    }

    // 生命周期
    onMounted(async () => {
      try {
        await fileStore.fetchFiles()
        
        // 手动更新 filesList
        if (Array.isArray(fileStore.files.value) && fileStore.files.value.length > 0) {
          filesList.value = [...fileStore.files.value]
        }
      } catch (error) {
        console.error('Failed to fetch files:', error)
      }
      document.addEventListener('fullscreenchange', handleFullscreenChange)
    })

    onUnmounted(() => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
    })

    return {
      showUploadDialog,
      sidebarCollapsed,
      activeTab,
      viewMode,
      isFullscreen,
      selectedVideo,
      selectedPdf,
      allFiles,
      videoFiles,
      pdfFiles,
      filesList,
      selectFile,
      handleUploadSuccess,
      handleVideoFullscreen,
      toggleFullscreen
    }
  }
}
</script>

<style lang="scss" scoped>
.viewer-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: $gradient-dark;
}

.header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: $spacing-md $spacing-lg;
  z-index: 100;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
  }

  .title {
    display: flex;
    align-items: center;
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    background: $gradient-primary;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;

    .title-icon {
      margin-right: $spacing-sm;
      font-size: 28px;
    }
  }

  .header-actions {
    display: flex;
    gap: $spacing-sm;

    .button-icon {
      margin-right: $spacing-xs;
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;

  &.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999;
  }
}

.sidebar {
  width: 320px;
  background: rgba(255, 255, 255, 0.05);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;

  &.collapsed {
    width: 60px;
    
    .sidebar-header h3,
    .file-tabs {
      display: none;
    }
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: $spacing-md;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 500;
    }

    .collapse-btn {
      color: rgba(255, 255, 255, 0.7);
      
      &:hover {
        color: $tech-blue;
      }
    }
  }

  .file-tabs {
    flex: 1;
    overflow: hidden;

    :deep(.el-tabs) {
      height: 100%;
      
      .el-tabs__content {
        height: calc(100% - 40px);
        overflow: hidden;
      }
    }
  }
}

.viewer-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(0, 0, 0, 0.3);
}

.viewer-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  background: rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .viewer-controls {
    display: flex;
    gap: $spacing-sm;
  }

  .viewer-info {
    display: flex;
    align-items: center;
    gap: $spacing-md;

    .info-item {
      display: flex;
      align-items: center;
      gap: $spacing-xs;
      font-size: 14px;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

.viewer-content {
  flex: 1;
  overflow: hidden;

  &.single {
    .single-viewer {
      height: 100%;
    }
  }

  &.split {
    .split-viewer {
      display: flex;
      height: 100%;

      .split-panel {
        flex: 1;
        display: flex;
        flex-direction: column;
        border-right: 1px solid rgba(255, 255, 255, 0.1);

        &:last-child {
          border-right: none;
        }

        .panel-header {
          display: flex;
          align-items: center;
          gap: $spacing-xs;
          padding: 1px $spacing-xs; // 进一步减小padding
          background: rgba(255, 255, 255, 0.05);
          font-size: 10px; // 进一步减小字体
          font-weight: 400; // 减小粗细
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          flex: 1; // 占1部分 (~1%)
          height: 10px; // 固定更小高度
          min-height: 10px;
          
          // 在小屏幕上最小化
          @media (max-height: 600px) or (max-width: 1200px) {
            padding: 1px 2px;
            span { display: none; } // 隐藏文本，只显示图标
            height: 8px;
            min-height: 8px;
          }
        }

        // 内容区域占99部分 (~99%)
        & > * { // 针对VideoPlayer, PdfViewer, EmptyPanel
          flex: 99;
          overflow: hidden;
        }

        // 在小屏幕下保持比例
        @media (max-height: 600px) {
          .panel-header { flex: 1; height: 8px; min-height: 8px; }
          & > * { flex: 99; }
        }
      }
    }
  }
}
</style>
