import { ref } from 'vue'
import axios from 'axios'

const API_BASE_URL = '/api'

export function useFileStore() {
  const files = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // 确保 files 始终是一个数组
  const ensureFilesArray = () => {
    if (!Array.isArray(files.value)) {
      files.value = []
    }
  }

  const fetchFiles = async () => {
    ensureFilesArray()
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_BASE_URL}/files/`)
      const data = response.data
      files.value = Array.isArray(data) ? data : []
    } catch (err) {
      error.value = err.response?.data?.message || '获取文件列表失败'
      console.error('获取文件列表失败:', err)
      files.value = []
    } finally {
      loading.value = false
    }
  }

  const uploadFile = async (fileData) => {
    ensureFilesArray()
    loading.value = true
    error.value = null
    
    try {
      const formData = new FormData()
      formData.append('file', fileData.file)
      formData.append('title', fileData.title)
      formData.append('description', fileData.description || '')
      
      const response = await axios.post(`${API_BASE_URL}/files/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // 重新获取文件列表
      await fetchFiles()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || '文件上传失败'
      console.error('文件上传失败:', err)
      files.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteFile = async (fileId) => {
    ensureFilesArray()
    loading.value = true
    error.value = null
    
    try {
      await axios.delete(`${API_BASE_URL}/files/${fileId}/`)
      // 重新获取文件列表
      await fetchFiles()
    } catch (err) {
      error.value = err.response?.data?.message || '文件删除失败'
      console.error('文件删除失败:', err)
      files.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  const getFileById = (fileId) => {
    return Array.isArray(files.value) ? files.value.find(file => file.id === fileId) : null
  }

  const getFilesByType = (fileType) => {
    return Array.isArray(files.value) ? files.value.filter(file => file.file_type === fileType) : []
  }

  return {
    files,
    loading,
    error,
    fetchFiles,
    uploadFile,
    deleteFile,
    getFileById,
    getFilesByType
  }
}
