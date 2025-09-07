<template>
  <div class="file-list">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="files.length === 0" class="empty-container">
      <Document class="empty-icon" />
      <p>暂无文件</p>
    </div>
    
    <div v-else class="files-container">
      <div 
        v-for="file in files" 
        :key="file.id"
        class="file-item"
        :class="{ 'active': selectedFileId === file.id }"
        @click="selectFile(file)"
      >
        <div class="file-icon">
          <VideoPlay v-if="file.file_type === 'video'" />
          <Document v-else />
        </div>
        
        <div class="file-info">
          <div class="file-title">{{ file.title }}</div>
          <div class="file-meta">
            <span class="file-size">{{ file.file_size_mb }}MB</span>
            <span class="file-date">{{ formatDate(file.uploaded_at) }}</span>
          </div>
        </div>
        
        <div class="file-actions">
          <el-button 
            type="text" 
            size="small"
            @click.stop="deleteFile(file.id)"
            class="delete-btn"
          >
            <Delete />
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Document, VideoPlay, Delete } from '@element-plus/icons-vue'
import { useFileStore } from '@/stores/fileStore'

export default {
  name: 'FileList',
  props: {
    files: {
      type: Array,
      default: () => []
    },
    selectedFileId: {
      type: [String, Number],
      default: null
    }
  },
  emits: ['select-file'],
  setup(props, { emit }) {
    const fileStore = useFileStore()
    
    const loading = computed(() => fileStore.loading.value)
    
    const selectFile = (file) => {
      emit('select-file', file)
    }
    
    const deleteFile = async (fileId) => {
      try {
        await ElMessageBox.confirm(
          '确定要删除这个文件吗？此操作不可恢复。',
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await fileStore.deleteFile(fileId)
        ElMessage.success('文件删除成功')
      } catch (err) {
        if (err !== 'cancel') {
          ElMessage.error('文件删除失败')
        }
      }
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
      loading,
      selectFile,
      deleteFile,
      formatDate
    }
  }
}
</script>

<style lang="scss" scoped>
.file-list {
  height: 100%;
  overflow-y: auto;
  padding: $spacing-sm;
}

.loading-container {
  padding: $spacing-lg;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: rgba(255, 255, 255, 0.6);
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: $spacing-md;
  }
  
  p {
    margin: 0;
    font-size: 14px;
  }
}

.files-container {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.file-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  background: rgba(255, 255, 255, 0.05);
  border-radius: $border-radius-medium;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: $shadow-light;
  }
  
  &.active {
    background: rgba(0, 212, 255, 0.2);
    border-color: $tech-blue;
    box-shadow: $shadow-glow;
  }
  
  .file-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: $border-radius-small;
    margin-right: $spacing-md;
    font-size: 20px;
    color: $tech-blue;
  }
  
  .file-info {
    flex: 1;
    min-width: 0;
    
    .file-title {
      font-weight: 500;
      margin-bottom: $spacing-xs;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    
    .file-meta {
      display: flex;
      gap: $spacing-md;
      font-size: 12px;
      color: rgba(255, 255, 255, 0.6);
      
      .file-size {
        color: $tech-cyan;
      }
    }
  }
  
  .file-actions {
    opacity: 0;
    transition: opacity 0.3s ease;
    
    .delete-btn {
      color: rgba(255, 255, 255, 0.6);
      
      &:hover {
        color: $danger-color;
      }
    }
  }
  
  &:hover .file-actions {
    opacity: 1;
  }
}
</style>
