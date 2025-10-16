# 教育管理系统 (Education Management System)

这是一个集课件/知识库管理、考试系统和人员管理系统于一体的综合性教育管理平台。

## 功能模块

1. **课件/知识库管理**
   - 课件上传与分类
   - 知识点检索
   - 版本控制

2. **考试系统**
   - 题库管理
   - 试卷生成
   - 在线考试
   - 成绩统计与分析

3. **人员管理系统**
   - 用户信息管理
   - 角色权限分配
   - 组织架构管理

## 技术栈

- **后端**: Python (Flask)
- **前端**: Vue.js, Element Plus
- **数据库**: PostgreSQL
- **其他**: Docker, RESTful API, JWT认证

## 项目启动指南

### 系统要求

- Docker 和 Docker Compose (推荐运行方式)
- 或
- Python 3.8+, Node.js 14+, npm 6+

### 方式一：使用Docker运行（推荐）

#### 步骤1：准备环境
确保已安装Docker和Docker Compose。可以通过以下命令检查：
```bash
docker --version
docker-compose --version
```

#### 步骤2：配置环境变量
在项目根目录创建`.env`文件（如果不存在），并添加以下配置：
```
# 数据库配置
DATABASE_URL=postgresql://admin:password@db:5432/example_db

# JWT配置
JWT_SECRET_KEY=your_jwt_secret_key_here

# Flask配置
FLASK_APP=app.py
FLASK_ENV=development
```

#### 步骤3：启动容器
在项目根目录下运行：
```bash
docker-compose up -d
```

这将启动三个容器：
- 前端应用容器
- 后端API容器
- PostgreSQL数据库容器

#### 步骤4：初始化数据库
```bash
docker exec -it medicalmanagermentsystem_backend_1 python init_admin.py
docker exec -it medicalmanagermentsystem_backend_1 python init_test_data.py
```

#### 步骤5：访问应用
- 前端应用：http://localhost:8080
- 后端API：http://localhost:5000
- 数据库（内部访问）：postgresql://admin:password@db:5432/example_db

### 方式二：本地运行

#### 后端启动步骤

1. **进入backend目录**：
   ```bash
   cd backend
   ```

2. **创建虚拟环境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **安装Python依赖**：
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**：
   创建`.env`文件：
   ```
   DATABASE_URL=postgresql://admin:password@localhost:5432/example_db
   JWT_SECRET_KEY=your_jwt_secret_key_here
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

5. **启动数据库**（确保本地PostgreSQL已运行）：
   如果没有PostgreSQL，可以使用Docker单独启动：
   ```bash
   docker run -d --name postgres-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=example_db -p 5432:5432 postgres:13
   ```

6. **初始化数据库**：
   ```bash
   python init_admin.py
   python init_test_data.py
   ```

7. **运行后端应用**：
   ```bash
   python app.py
   ```

   后端API地址：http://localhost:5000

#### 前端启动步骤

1. **进入frontend目录**：
   ```bash
   cd frontend
   ```

2. **安装Node.js依赖**：
   ```bash
   npm install
   ```

3. **配置API地址**（可选）：
   如果需要修改后端API地址，编辑`src/services/api.js`文件中的基础URL

4. **运行前端应用**：
   ```bash
   npm run serve
   ```

   前端应用地址：http://localhost:8080

## 管理员账户

系统初始化后会自动创建默认管理员账户：

- **用户名**: admin
- **密码**: admin123

首次登录后请立即修改密码。

## 主要API端点

- **认证相关**：
  - POST /api/auth/login - 用户登录
  - POST /api/auth/register - 用户注册
  - GET /api/auth/me - 获取当前用户信息

- **考试管理**：
  - GET /api/exams - 获取考试列表
  - POST /api/exams - 创建考试
  - GET /api/questions - 获取题库
  - POST /api/questions - 添加试题

- **课程管理**：
  - GET /api/courses - 获取课程列表
  - POST /api/courses - 创建课程

- **文档管理**：
  - GET /api/documents - 获取文档列表
  - POST /api/documents - 上传文档

- **用户管理**：
  - GET /api/users - 获取用户列表
  - PUT /api/users/:id - 更新用户信息

## 常见问题与解决方案

### 数据库连接错误
- 确保PostgreSQL服务正在运行
- 检查`.env`文件中的数据库连接字符串是否正确
- 检查数据库用户名和密码是否匹配

### 启动失败
- 检查端口是否被占用（8080, 5000, 5432）
- 使用`docker-compose logs`查看详细错误信息
- 对于Python依赖问题，尝试删除`venv`目录并重新创建虚拟环境

### 文件上传问题
- 确保上传目录权限正确
- 检查文件大小限制配置

### 权限问题
- 确保使用具有正确权限的账户登录
- 管理员功能需要使用管理员账户访问

## 项目结构

```
MedicalManagermentSystem/
├── backend/           # 后端Flask应用
│   ├── app.py         # 应用入口
│   ├── routes.py      # API路由
│   ├── models.py      # 数据库模型
│   ├── requirements.txt # Python依赖
│   └── ...
├── frontend/          # 前端Vue应用
│   ├── src/           # 源代码
│   ├── package.json   # npm依赖
│   └── ...
├── docker-compose.yml # Docker配置
└── README.md          # 项目文档
```

## 开发注意事项

1. **API测试**：可以使用Postman或curl测试API端点
2. **数据库迁移**：对模型修改后需要执行数据库迁移
3. **日志查看**：使用`docker-compose logs -f`实时查看应用日志
4. **环境变量安全**：生产环境中不要使用默认JWT密钥，应使用强随机密钥

## 安全建议

1. 生产环境中禁用开发模式
2. 使用HTTPS协议
3. 定期更新依赖包以修复安全漏洞
4. 实施适当的输入验证防止SQL注入和XSS攻击
5. 为敏感操作添加适当的权限检查

## 维护与更新

### 更新代码
```bash
git pull origin main
# 使用Docker时重新构建容器
docker-compose down
docker-compose build
docker-compose up -d
```

### 数据备份
```bash
docker exec -t medicalmanagermentsystem_db_1 pg_dumpall -c -U admin > dump_$(date +%Y%m%d).sql
```

### 数据恢复
```bash
cat dump_YYYYMMDD.sql | docker exec -i medicalmanagermentsystem_db_1 psql -U admin -d example_db
```

## 许可证

[在此添加项目许可证信息]