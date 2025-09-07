# 故障排除指南

## 常见问题及解决方案

### 1. "data2 is not iterable" 错误

**问题描述：**
点击管理试卷时出现 `TypeError: data2 is not iterable` 错误。

**原因：**
Element Plus表格组件期望接收数组数据，但API返回的数据格式不正确。

**解决方案：**

1. **检查后端API是否正常运行：**
   ```bash
   # 激活conda环境
   conda activate lungshired
   
   # 进入后端目录
   cd backend
   
   # 启动Django服务器
   python manage.py runserver
   ```

2. **测试API端点：**
   ```bash
   # 在backend目录下运行测试脚本
   python test_api.py
   ```

3. **使用API测试页面：**
   - 访问 `http://localhost:5173/api-test`
   - 点击各个测试按钮检查API状态

4. **检查浏览器控制台：**
   - 打开浏览器开发者工具 (F12)
   - 查看Console标签页的错误信息
   - 查看Network标签页的API请求状态

### 2. API返回404错误

**问题描述：**
API请求返回404 Not Found错误。

**解决方案：**

1. **检查Django URL配置：**
   ```python
   # backend/video_viewer/urls.py
   from django.urls import path, include
   
   urlpatterns = [
       path('api/', include('exams.urls')),
   ]
   ```

2. **检查exams应用的URL配置：**
   ```python
   # backend/exams/urls.py
   from django.urls import path, include
   from rest_framework.routers import DefaultRouter
   from . import views
   
   router = DefaultRouter()
   router.register(r'students', views.StudentViewSet)
   router.register(r'exams', views.ExamViewSet)
   router.register(r'exam-assignments', views.ExamStudentAssignmentViewSet)
   
   urlpatterns = router.urls
   ```

3. **确保Django服务器正在运行：**
   ```bash
   python manage.py runserver
   ```

### 3. CORS错误

**问题描述：**
浏览器控制台显示CORS相关错误。

**解决方案：**

1. **检查Django CORS设置：**
   ```python
   # backend/video_viewer/settings.py
   INSTALLED_APPS = [
       # ...
       'corsheaders',
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       # ... 其他中间件
   ]
   
   CORS_ALLOW_ALL_ORIGINS = True
   CORS_ALLOW_CREDENTIALS = True
   ```

2. **安装corsheaders包：**
   ```bash
   pip install django-cors-headers
   ```

### 4. 数据库迁移错误

**问题描述：**
数据库表结构不匹配，出现字段不存在错误。

**解决方案：**

1. **检查迁移状态：**
   ```bash
   python manage.py showmigrations
   ```

2. **应用待处理的迁移：**
   ```bash
   python manage.py migrate
   ```

3. **如果迁移失败，重置数据库：**
   ```bash
   # 删除数据库文件
   rm backend/db.sqlite3
   
   # 重新创建迁移
   python manage.py makemigrations
   
   # 应用迁移
   python manage.py migrate
   ```

### 5. 前端无法连接后端

**问题描述：**
前端页面显示"加载数据失败"错误。

**解决方案：**

1. **检查端口配置：**
   - 后端默认运行在 `http://localhost:8000`
   - 前端默认运行在 `http://localhost:5173`

2. **检查防火墙设置：**
   - 确保8000端口没有被防火墙阻止

3. **检查网络连接：**
   ```bash
   # 测试后端连接
   curl http://localhost:8000/api/
   ```

### 6. 数据格式错误

**问题描述：**
API返回的数据格式与前端期望的格式不匹配。

**解决方案：**

1. **检查API响应格式：**
   ```bash
   curl http://localhost:8000/api/students/
   curl http://localhost:8000/api/exams/
   curl http://localhost:8000/api/exam-assignments/
   ```

2. **查看调试信息：**
   - 打开浏览器控制台
   - 查看调试日志输出
   - 检查API响应的数据结构

3. **使用模拟数据：**
   - 如果API不可用，系统会自动使用模拟数据
   - 检查控制台是否有"使用模拟数据"的警告信息

## 调试步骤

### 1. 系统检查清单

- [ ] 后端Django服务器正在运行
- [ ] 数据库迁移已应用
- [ ] CORS配置正确
- [ ] API端点可访问
- [ ] 前端开发服务器正在运行
- [ ] 浏览器控制台无错误

### 2. 逐步调试

1. **启动后端服务：**
   ```bash
   conda activate lungshired
   cd backend
   python manage.py runserver
   ```

2. **测试API：**
   ```bash
   python test_api.py
   ```

3. **启动前端服务：**
   ```bash
   cd frontend
   npm run dev
   ```

4. **访问API测试页面：**
   - 打开 `http://localhost:5173/api-test`
   - 运行所有测试

5. **检查管理页面：**
   - 访问 `http://localhost:5173/admin`
   - 测试各个功能模块

### 3. 日志分析

1. **Django日志：**
   - 查看后端控制台输出
   - 检查错误堆栈信息

2. **浏览器日志：**
   - 打开开发者工具 (F12)
   - 查看Console和Network标签页

3. **API调试信息：**
   - 查看控制台中的调试输出
   - 检查API响应数据结构

## 联系支持

如果以上解决方案都无法解决问题，请：

1. 收集错误日志和截图
2. 记录复现步骤
3. 提供系统环境信息
4. 联系技术支持团队
