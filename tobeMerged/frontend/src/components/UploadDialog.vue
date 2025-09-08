<template>
  <el-dialog
    v-model="dialogVisible"
    title="上传文件"
    width="500px"
    :before-close="handleClose"
    class="upload-dialog"
  >
    <div class="upload-content">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :on-change="handleFileChange"
            :before-upload="beforeUpload"
            :file-list="fileList"
            drag
            accept=".mp4,.avi,.mov,.wmv,.flv,.webm,.mkv,.pdf"
            class="upload-area"
          >
            <div class="upload-trigger">
              <Upload class="upload-icon" />
              <div class="upload-text">
                <p>将文件拖到此处，或<em>点击上传</em></p>
                <p class="upload-hint">支持视频文件(.mp4, .avi, .mov, .wmv, .flv, .webm, .mkv)和PDF文件(.pdf)</p>
              </div>
            </div>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入文件标题"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入文件描述（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
        <el-progress
          :percentage="uploadProgress"
          :status="uploadStatus"
          :stroke-width="8"
        />
        <p class="progress-text">{{ progressText }}</p>
      </div>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="uploading"
          :disabled="!form.file || !form.title"
          @click="handleUpload"
        >
          {{ uploading ? '上传中...' : '开始上传' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useFileStore } from '@/stores/fileStore'

export default {
  name: 'UploadDialog',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'upload-success'],
  setup(props, { emit }) {
    const fileStore = useFileStore()
    const formRef = ref(null)
    const uploadRef = ref(null)
    
    const form = ref({
      file: null,
      title: '',
      description: ''
    })
    
    const fileList = ref([])
    const uploading = ref(false)
    const uploadProgress = ref(0)
    const uploadStatus = ref('')
    const progressText = ref('')
    
    const dialogVisible = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })
    
    const rules = {
      file: [
        { required: true, message: '请选择要上传的文件', trigger: 'change' }
      ],
      title: [
        { required: true, message: '请输入文件标题', trigger: 'blur' },
        { min: 1, max: 255, message: '标题长度在 1 到 255 个字符', trigger: 'blur' }
      ]
    }
    
    const handleFileChange = (file) => {
      form.value.file = file.raw
      if (!form.value.title) {
        form.value.title = file.name.replace(/\.[^/.]+$/, '') // 移除扩展名
      }
    }
    
    const beforeUpload = (file) => {
      // 检查文件大小 (50MB)
      const isLt50M = file.size / 1024 / 1024 < 50
      if (!isLt50M) {
        ElMessage.error('文件大小不能超过 50MB!')
        return false
      }
      
      // 检查文件类型
      const allowedTypes = [
        'video/mp4', 'video/avi', 'video/quicktime', 'video/x-ms-wmv',
        'video/x-flv', 'video/webm', 'video/x-matroska', 'application/pdf'
      ]
      const isValidType = allowedTypes.includes(file.type) || 
                         file.name.toLowerCase().endsWith('.pdf')
      
      if (!isValidType) {
        ElMessage.error('只支持视频文件和PDF文件!')
        return false
      }
      
      return false // 阻止自动上传
    }
    
    const handleUpload = async () => {
      if (!form.value.file || !form.value.title) {
        ElMessage.warning('请选择文件并输入标题')
        return
      }
      
      try {
        await formRef.value.validate()
        
        uploading.value = true
        uploadProgress.value = 0
        uploadStatus.value = ''
        progressText.value = '准备上传...'
        
        // 模拟上传进度
        const progressInterval = setInterval(() => {
          if (uploadProgress.value < 90) {
            uploadProgress.value += Math.random() * 10
            progressText.value = `上传中... ${Math.round(uploadProgress.value)}%`
          }
        }, 200)
        
        await fileStore.uploadFile(form.value)
        
        clearInterval(progressInterval)
        uploadProgress.value = 100
        uploadStatus.value = 'success'
        progressText.value = '上传完成!'
        
        setTimeout(() => {
          ElMessage.success('文件上传成功!')
          emit('upload-success', form.value)
          handleClose()
        }, 500)
        
      } catch (err) {
        uploadStatus.value = 'exception'
        progressText.value = '上传失败'
        ElMessage.error(err.message || '文件上传失败')
      } finally {
        uploading.value = false
      }
    }
    
    const handleClose = () => {
      if (uploading.value) {
        ElMessage.warning('文件正在上传中，请稍候...')
        return
      }
      
      // 重置表单
      form.value = {
        file: null,
        title: '',
        description: ''
      }
      fileList.value = []
      uploadProgress.value = 0
      uploadStatus.value = ''
      progressText.value = ''
      
      if (formRef.value) {
        formRef.value.resetFields()
      }
      
      dialogVisible.value = false
    }
    
    // 监听对话框关闭
    watch(dialogVisible, (newVal) => {
      if (!newVal) {
        handleClose()
      }
    })
    
    return {
      formRef,
      uploadRef,
      form,
      fileList,
      uploading,
      uploadProgress,
      uploadStatus,
      progressText,
      dialogVisible,
      rules,
      handleFileChange,
      beforeUpload,
      handleUpload,
      handleClose
    }
  }
}
</script>

<style lang="scss" scoped>
.upload-dialog {
  :deep(.el-dialog) {
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: $border-radius-large;
    
    .el-dialog__header {
      background: rgba(255, 255, 255, 0.05);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      
      .el-dialog__title {
        color: #ffffff;
        font-weight: 600;
      }
    }
    
    .el-dialog__body {
      color: #ffffff;
    }
    
    .el-dialog__footer {
      background: rgba(255, 255, 255, 0.05);
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
  }
}

.upload-content {
  .upload-area {
    :deep(.el-upload-dragger) {
      background: rgba(255, 255, 255, 0.05);
      border: 2px dashed rgba(255, 255, 255, 0.3);
      border-radius: $border-radius-large;
      
      &:hover {
        border-color: $tech-blue;
        background: rgba(0, 212, 255, 0.1);
      }
    }
  }
  
  .upload-trigger {
    padding: $spacing-xl;
    text-align: center;
    
    .upload-icon {
      font-size: 48px;
      color: $tech-blue;
      margin-bottom: $spacing-md;
    }
    
    .upload-text {
      p {
        margin: 0;
        font-size: 16px;
        color: rgba(255, 255, 255, 0.8);
        
        em {
          color: $tech-blue;
          font-style: normal;
          font-weight: 600;
        }
      }
      
      .upload-hint {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        margin-top: $spacing-sm;
      }
    }
  }
  
  .upload-progress {
    margin-top: $spacing-lg;
    padding: $spacing-md;
    background: rgba(255, 255, 255, 0.05);
    border-radius: $border-radius-medium;
    
    .progress-text {
      margin: $spacing-sm 0 0 0;
      font-size: 14px;
      color: rgba(255, 255, 255, 0.8);
      text-align: center;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-sm;
}
</style>
