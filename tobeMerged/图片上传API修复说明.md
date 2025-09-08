# 图片上传API修复说明

## 🎯 问题描述

用户报告图片上传时出现错误：
```
Not Found: /undefined/api/exams/upload-image/
[23/Aug/2025 21:30:02] "POST /undefined/api/exams/upload-image/ HTTP/1.1" 404 2523
```

## 🔍 问题分析

### 1. **URL路径错误**
- 前端使用的URL：`/api/exams/upload-image/`
- 实际API端点：`/api/exams/questions/upload_image/`

### 2. **baseURL未定义**
- 错误显示 `/undefined/api/exams/upload-image/`
- 说明 `baseURL` 变量值为 `undefined`

## ✨ 解决方案

### 1. **修复前端URL路径**

**修改前：**
```vue
:action="`${baseURL}/api/exams/upload-image/`"
```

**修改后：**
```vue
:action="`${baseURL}/api/exams/questions/upload_image/`"
```

### 2. **确保baseURL正确设置**

在 `ExamEditor.vue` 的 `setup()` 函数中：
```javascript
const baseURL = 'http://localhost:8000'
```

### 3. **验证API端点配置**

后端 `QuestionViewSet` 中的配置：
```python
@action(detail=False, methods=['post'])
def upload_image(self, request):
    """上传题目图片"""
    # ... 实现代码
```

## 🧪 测试验证

### 1. **使用测试脚本**
```bash
python test_image_upload.py
```

### 2. **手动测试API端点**
```bash
curl -X POST http://localhost:8000/api/exams/questions/upload_image/ \
  -F "image=@test.png" \
  -H "X-Requested-With: XMLHttpRequest"
```

### 3. **前端功能测试**
1. 启动Django服务器
2. 启动前端服务
3. 访问 `http://localhost:8080/exam-editor`
4. 创建试卷并添加问题
5. 尝试上传图片

## 📋 API端点详情

### 图片上传端点
- **URL**: `POST /api/exams/questions/upload_image/`
- **Content-Type**: `multipart/form-data`
- **参数**: `image` (文件)
- **响应**: 
  ```json
  {
    "image": "question_images/uuid.png",
    "image_url": "http://localhost:8000/media/question_images/uuid.png",
    "message": "图片上传成功"
  }
  ```

### 支持的图片格式
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

### 文件大小限制
- 最大文件大小：5MB

## 🔧 技术实现

### 1. **后端实现**
```python
@action(detail=False, methods=['post'])
def upload_image(self, request):
    """上传题目图片"""
    try:
        if 'image' not in request.FILES:
            return Response({'error': '没有找到图片文件'}, status=400)
        
        image_file = request.FILES['image']
        
        # 验证文件类型和大小
        # 生成唯一文件名
        # 保存文件
        # 返回文件信息
        
    except Exception as e:
        return Response({'error': f'上传失败: {str(e)}'}, status=500)
```

### 2. **前端实现**
```vue
<el-upload
  :action="`${baseURL}/api/exams/questions/upload_image/`"
  :headers="uploadHeaders"
  :on-success="handleImageSuccess"
  :on-error="handleImageError"
  :before-upload="beforeImageUpload"
  accept="image/*"
>
  <!-- 上传界面 -->
</el-upload>
```

## ⚠️ 注意事项

1. **确保Django服务器运行在8000端口**
2. **确保媒体文件配置正确**
3. **检查文件权限和存储路径**
4. **验证CORS配置（如果前后端分离）**

## 🎉 修复结果

修复后，图片上传功能将正常工作：
- ✅ 正确的API端点路径
- ✅ 文件类型验证
- ✅ 文件大小限制
- ✅ 图片预览功能
- ✅ 错误处理机制

现在可以正常使用图片上传功能了！
