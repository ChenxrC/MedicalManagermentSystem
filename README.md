# 教育管理系统 (Education Management System)

这是一个集课件/知识库管理、考试系统和人员管理系统于一体的网站。

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
- **前端**: Vue.js
- **数据库**: PostgreSQL
- **其他**: Docker, RESTful API

## 运行方式

### 使用Docker运行（推荐）

1. 确保已安装Docker和Docker Compose
2. 在项目根目录下运行以下命令：
   ```
   docker-compose up -d
   ```
3. 访问前端应用：http://localhost:8080
4. 访问后端API：http://localhost:5000

### 本地运行

#### 后端
1. 进入backend目录：
   ```
   cd backend
   ```
2. 安装Python依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行应用：
   ```
   python app.py
   ```
4. 后端API地址：http://localhost:5000

#### 前端
1. 进入frontend目录：
   ```
   cd frontend
   ```
2. 安装Node.js依赖：
   ```
   npm install
   ```
3. 运行应用：
   ```
   npm run serve
   ```
4. 前端应用地址：http://localhost:8080