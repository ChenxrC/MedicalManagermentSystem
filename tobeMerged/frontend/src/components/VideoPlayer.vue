<template>
  <div class="video-player">
    <div class="video-container">
      <video
        ref="videoRef"
        class="video-element"
        :class="{ 'portrait': isPortrait, 'landscape': !isPortrait }"
        controls
        preload="auto"
        @loadedmetadata="onVideoLoaded"
      >
        <source :src="videoUrl" :type="videoType">
        您的浏览器不支持视频播放。
      </video>
    </div>
    
    <div class="video-info">
      <h3>{{ video.title }}</h3>
      <div class="video-meta">
        <span class="file-size">{{ video.file_size_mb }}MB</span>
        <span class="upload-time">{{ formatDate(video.uploaded_at) }}</span>
      </div>
      <p v-if="video.description" class="description">{{ video.description }}</p>
    </div>
    
    <div class="video-controls">
      <el-button-group>
        <el-button @click="toggleFullscreen">
          <FullScreen v-if="!isFullscreen" />
          <Aim v-else />
          {{ isFullscreen ? '退出全屏' : '全屏播放' }}
        </el-button>
        <el-button @click="downloadVideo">
          <Download />
          下载视频
        </el-button>
      </el-button-group>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'VideoPlayer',
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  emits: ['fullscreen'],
  setup(props, { emit }) {
    const videoRef = ref(null)
    const isFullscreen = ref(false)
    const isPortrait = ref(false)
    const videoAspectRatio = ref(16/9) // 默认宽高比
    
    const videoUrl = computed(() => {
      return props.video.file_url || `/api${props.video.file}`
    })
    
    const videoType = computed(() => {
      const ext = props.video.file_extension
      const typeMap = {
        '.mp4': 'video/mp4',
        '.avi': 'video/avi',
        '.mov': 'video/quicktime',
        '.wmv': 'video/x-ms-wmv',
        '.flv': 'video/x-flv',
        '.webm': 'video/webm',
        '.mkv': 'video/x-matroska'
      }
      return typeMap[ext] || 'video/mp4'
    })
    
    const onVideoLoaded = () => {
      if (videoRef.value) {
        const video = videoRef.value
        const aspectRatio = video.videoWidth / video.videoHeight
        videoAspectRatio.value = aspectRatio
        isPortrait.value = aspectRatio < 1 // 宽高比小于1为竖屏
      }
    }
    
    const toggleFullscreen = () => {
      if (videoRef.value) {
        if (document.fullscreenElement) {
          document.exitFullscreen()
        } else {
          videoRef.value.requestFullscreen()
        }
      }
    }
    
    const downloadVideo = () => {
      const link = document.createElement('a')
      link.href = videoUrl.value
      link.download = props.video.title
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
    
    return {
      videoRef,
      isFullscreen,
      isPortrait,
      videoUrl,
      videoType,
      onVideoLoaded,
      toggleFullscreen,
      downloadVideo,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.video-player {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 0, 0, 0.8);
}

.video-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-md;
  overflow: hidden;
  min-height: 0; // 确保flex子元素可以收缩
  
  // 在小屏幕上减少内边距
  @media (max-height: 600px) {
    padding: $spacing-sm;
  }
  
  .video-element {
    max-width: 100%;
    max-height: 100%;
    border-radius: 8px;
    background: #000;
    object-fit: contain; // 保持宽高比，完整显示视频
    
    &.portrait {
      // 竖屏视频：限制最大高度，宽度自适应
      max-height: 80vh; // 限制最大高度为视口高度的80%
      width: auto;
      height: auto;
      
      // 在小屏幕上进一步限制高度
      @media (max-height: 600px) {
        max-height: 70vh;
      }
      
      @media (max-height: 500px) {
        max-height: 60vh;
      }
    }
    
    &.landscape {
      // 横屏视频：限制最大宽度，高度自适应
      max-width: 100%;
      height: auto;
    }
  }
}

.video-info {
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0; // 防止被压缩
  
  // 在分屏模式下更紧凑
  @media (max-width: 1200px) {
    padding: $spacing-xs $spacing-sm;
  }
  
  // 在小屏幕上减少内边距
  @media (max-height: 600px) {
    padding: $spacing-sm $spacing-md;
  }
  
  @media (max-height: 500px) {
    padding: $spacing-xs $spacing-sm;
  }
  
  h3 {
    margin: 0 0 $spacing-xs 0;
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    word-break: break-word; // 长标题换行
    
    // 在分屏模式下更小
    @media (max-width: 1200px) {
      font-size: 12px;
      margin: 0 0 4px 0;
    }
    
    // 在小屏幕上减小字体大小
    @media (max-height: 600px) {
      font-size: 16px;
      margin-bottom: $spacing-xs;
    }
    
    @media (max-height: 500px) {
      font-size: 14px;
    }
  }
  
  .video-meta {
    display: flex;
    gap: $spacing-sm;
    margin-bottom: $spacing-xs;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.7);
    flex-wrap: wrap; // 在小屏幕上换行
    
    // 在分屏模式下更紧凑
    @media (max-width: 1200px) {
      gap: $spacing-xs;
      font-size: 10px;
      margin-bottom: 2px;
    }
    
    .file-size {
      color: $tech-cyan;
    }
    
    // 在小屏幕上减小字体大小和间距
    @media (max-height: 600px) {
      font-size: 12px;
      gap: $spacing-sm;
      margin-bottom: $spacing-xs;
    }
    
    @media (max-height: 500px) {
      font-size: 11px;
      gap: $spacing-xs;
    }
  }
  
  .description {
    margin: 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.5;
    word-break: break-word; // 长描述换行
    
    // 在小屏幕上隐藏描述以节省空间
    @media (max-height: 500px) {
      display: none;
    }
  }
}

.video-controls {
  padding: $spacing-sm $spacing-md;
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
  flex-shrink: 0; // 防止被压缩
  
  // 在分屏模式下更紧凑
  @media (max-width: 1200px) {
    padding: $spacing-xs $spacing-sm;
  }
  
  // 在小屏幕上减少内边距
  @media (max-height: 600px) {
    padding: $spacing-sm $spacing-md;
  }
  
  @media (max-height: 500px) {
    padding: $spacing-xs $spacing-sm;
  }
  
  .el-button-group {
    display: flex;
    gap: $spacing-sm;
    flex-wrap: wrap; // 在小屏幕上换行
    justify-content: center;
    
    // 在小屏幕上减小按钮大小
    @media (max-height: 600px) {
      gap: $spacing-xs;
      
      .el-button {
        padding: 8px 12px;
        font-size: 12px;
      }
    }
    
    @media (max-height: 500px) {
      .el-button {
        padding: 6px 10px;
        font-size: 11px;
      }
    }
  }
}
</style>
