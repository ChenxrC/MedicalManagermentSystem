# 学员考试API问题排查指南

## 问题描述
学员界面报错"获取考试列表失败"，后端返回404错误：`Not Found: /api/exams/exams/`

## 问题原因
前端代码中使用了错误的API路径，导致路径重复：
- 错误路径：`/api/exams/exams/`
- 正确路径：`/api/exams/`

## 已修复的文件

### 1. 前端组件修复

#### StudentExamList.vue
- **文件位置**: `frontend/src/components/StudentExamList.vue`
- **修复内容**: 将API路径从 `/api/exams/exams/?student=${studentId}` 改为 `/api/exams/?student=${studentId}`

#### AnswerInterface.vue
- **文件位置**: `frontend/src/components/AnswerInterface.vue`
- **修复内容**: 将API路径从 `/api/exams/exams/${examId}/for_student/?student=${studentId}` 改为 `/api/exams/${examId}/for_student/?student=${studentId}`

#### ExamEditor.vue
- **文件位置**: `frontend/src/components/ExamEditor.vue`
- **修复内容**: 将API路径从 `/api/exams/exams/` 改为 `/api/exams/`

### 2. Store修复

#### examStore.js
- **文件位置**: `frontend/src/stores/examStore.js`
- **修复内容**: 
  - 移除了重复的路径拼接
  - 修正了所有API调用路径
  - 修正了答案提交路径

## 验证步骤

### 1. 检查后端服务
确保后端服务正在运行：
```bash
cd backend
python manage.py runserver
```

### 2. 测试API路径
运行测试脚本验证API路径：
```bash
python test_api_paths.py
```

### 3. 检查数据库数据
运行数据库检查脚本：
```bash
python check_database.py
```

### 4. 测试学员考试API
运行学员考试API测试：
```bash
python test_student_exam_api.py
```

## 常见问题及解决方案

### 1. 404错误
**问题**: API路径不存在
**解决**: 确保使用正确的API路径，不要重复 `/exams/`

### 2. 权限错误
**问题**: 学员没有分配考试
**解决**: 
- 检查数据库中是否有学员数据
- 检查是否有考试分配记录
- 确保学员ID正确

### 3. 数据库为空
**问题**: 没有考试或学员数据
**解决**: 
- 创建测试数据
- 为学员分配考试

### 4. 用户认证问题
**问题**: 用户未登录或认证失败
**解决**: 
- 确保用户已登录
- 检查用户权限

## 测试数据创建

如果需要创建测试数据，可以使用以下脚本：

```python
# 创建测试用户和学员
from django.contrib.auth.models import User
from exams.models import Student, Exam, ExamStudentAssignment

# 创建用户
user = User.objects.create_user(username='test_student', password='test123')

# 创建学员
student = Student.objects.create(
    user=user,
    student_id='S001',
    name='测试学员',
    email='test@example.com'
)

# 创建考试
exam = Exam.objects.create(
    title='测试考试',
    description='这是一个测试考试',
    is_active=True
)

# 分配考试给学员
assignment = ExamStudentAssignment.objects.create(
    exam=exam,
    student=student,
    is_active=True
)
```

## 调试技巧

### 1. 浏览器开发者工具
- 打开Network标签页
- 查看API请求的详细信息
- 检查请求URL和响应状态

### 2. 后端日志
- 查看Django服务器日志
- 检查是否有错误信息
- 验证请求是否到达后端

### 3. 数据库查询
- 使用Django shell检查数据
- 验证模型关系是否正确
- 检查数据完整性

## 预防措施

1. **统一API路径管理**: 使用统一的API基础URL配置
2. **代码审查**: 在修改API调用时进行代码审查
3. **自动化测试**: 编写API测试用例
4. **文档维护**: 保持API文档的更新

## 联系支持

如果问题仍然存在，请提供以下信息：
1. 完整的错误日志
2. 数据库检查结果
3. API测试结果
4. 浏览器开发者工具截图
