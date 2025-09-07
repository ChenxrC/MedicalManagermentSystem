# 管理系统API集成说明

## 概述

本系统已经完成了前端与后端API的集成，学员管理和试卷管理的数据现在从后端数据库中读取。

## 后端API端点

### 学员管理API
- `GET /api/students/` - 获取学员列表
- `POST /api/students/` - 创建新学员
- `PUT /api/students/{id}/` - 更新学员信息
- `DELETE /api/students/{id}/` - 删除学员

### 试卷管理API
- `GET /api/exams/` - 获取试卷列表
- `POST /api/exams/` - 创建新试卷
- `PUT /api/exams/{id}/` - 更新试卷信息
- `PATCH /api/exams/{id}/` - 更新试卷状态
- `DELETE /api/exams/{id}/` - 删除试卷

### 试卷分配API
- `GET /api/exam-assignments/` - 获取分配列表
- `POST /api/exam-assignments/` - 创建试卷分配
- `POST /api/exam-assignments/{id}/remove_assignment/` - 移除试卷分配

## 运行步骤

### 1. 启动后端服务

```bash
# 激活conda环境
conda activate lungshired

# 进入后端目录
cd backend

# 应用数据库迁移
python manage.py migrate

# 启动Django服务器
python manage.py runserver
```

### 2. 测试API

```bash
# 在backend目录下运行测试脚本
python test_api.py
```

### 3. 启动前端服务

```bash
# 进入前端目录
cd frontend

# 安装依赖（如果还没安装）
npm install

# 启动开发服务器
npm run dev
```

## 数据模型

### Student模型
- `user` - 关联的Django用户
- `student_id` - 学号
- `name` - 姓名
- `email` - 邮箱
- `phone` - 电话
- `department` - 院系
- `major` - 专业
- `grade` - 年级
- `created_at` - 创建时间
- `updated_at` - 更新时间

### Exam模型
- `title` - 试卷标题
- `description` - 试卷描述
- `is_active` - 是否启用
- `start_time` - 开始时间
- `end_time` - 结束时间
- `created_at` - 创建时间
- `updated_at` - 更新时间

### ExamStudentAssignment模型
- `exam` - 关联的试卷
- `student` - 关联的学员
- `assigned_at` - 分配时间
- `assigned_by` - 分配人
- `is_active` - 是否有效

## 前端组件更新

### 主要修改内容

1. **StudentManagement.vue**
   - 从后端API获取学员数据
   - 实现学员的增删改查操作
   - 添加错误处理和回退机制

2. **ExamManagement.vue**
   - 从后端API获取试卷数据
   - 实现试卷状态切换
   - 实现试卷删除功能
   - 更新状态字段为`is_active`

3. **AssignmentManagement.vue**
   - 从后端API获取分配数据
   - 实现试卷分配功能
   - 实现分配移除功能

4. **新增API工具文件**
   - `frontend/src/utils/api.js` - 统一的API调用工具

## 错误处理

系统实现了完善的错误处理机制：

1. **API调用失败时自动回退到模拟数据**
2. **详细的错误日志记录**
3. **用户友好的错误提示**

## 注意事项

1. **确保后端服务器运行在8000端口**
2. **确保数据库迁移已应用**
3. **如果API调用失败，系统会自动使用模拟数据**
4. **所有API请求都包含适当的错误处理**

## 测试建议

1. 先运行后端测试脚本验证API是否正常
2. 检查浏览器控制台是否有API错误
3. 验证数据的增删改查功能
4. 测试错误处理机制

## 故障排除

### 常见问题

1. **CORS错误**
   - 确保后端CORS配置正确
   - 检查前端请求URL是否正确

2. **数据库错误**
   - 确保已运行`python manage.py migrate`
   - 检查数据库文件是否存在

3. **API 404错误**
   - 确保后端服务器正在运行
   - 检查URL配置是否正确

4. **前端无法连接后端**
   - 检查端口配置
   - 确保防火墙设置正确
