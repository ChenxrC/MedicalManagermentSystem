# 视频和PDF浏览系统

一个功能完整的视频和PDF浏览系统，支持文件上传、视频播放、PDF查看和分屏对照功能，具有现代化的科技风格UI设计。

## 🚀 功能特性

- 🎥 **视频播放**: 支持多种视频格式(.mp4, .avi, .mov, .wmv, .flv, .webm, .mkv)
- 📄 **PDF查看**: 完整的PDF文档查看功能，支持缩放、翻页
- 🖥️ **全屏播放**: 视频全屏播放和页面全屏模式
- ⚡ **分屏对照**: 视频和PDF各占一半屏幕进行对照查看
- 📤 **文件上传**: 拖拽上传，支持大文件(50MB)
- 🎨 **科技风格**: 现代化的UI设计，毛玻璃效果和渐变背景
- 📱 **响应式**: 适配不同屏幕尺寸
- 🔄 **实时预览**: 文件上传后立即显示

## 🛠️ 技术栈

### 前端
- **Vue.js 3** - 渐进式JavaScript框架
- **Element Plus** - Vue 3 UI组件库
- **Video.js** - 专业视频播放器
- **PDF.js** - PDF文档渲染引擎
- **Axios** - HTTP客户端
- **SCSS** - CSS预处理器

### 后端
- **Django 4.2** - Python Web框架
- **Django REST Framework** - API开发框架
- **Django CORS Headers** - 跨域请求处理
- **Pillow** - 图像处理库

## 📁 项目结构

```
educationSystem/
├── backend/                 # Django后端
│   ├── media/              # 上传文件存储
│   ├── files/              # 文件管理应用
│   │   ├── models.py       # 数据模型
│   │   ├── views.py        # API视图
│   │   ├── serializers.py  # 序列化器
│   │   └── urls.py         # URL配置
│   ├── video_viewer/       # Django项目配置
│   ├── manage.py           # Django管理脚本
│   └── requirements.txt    # Python依赖
├── frontend/               # Vue.js前端
│   ├── public/             # 静态资源
│   ├── src/                # 源代码
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面组件
│   │   ├── stores/         # 状态管理
│   │   ├── styles/         # 样式文件
│   │   └── router/         # 路由配置
│   ├── package.json        # Node.js依赖
│   └── vue.config.js       # Vue配置
├── start_backend.bat       # 后端启动脚本
├── start_frontend.bat      # 前端启动脚本
└── README.md               # 项目说明
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 1. 克隆项目
```bash
git clone <repository-url>
cd educationSystem
```

### 2. 启动后端
```bash
# Windows
start_backend.bat

# 或手动执行
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. 启动前端
```bash
# Windows
start_frontend.bat

# 或手动执行
cd frontend
npm install
npm run serve
```

### 4. 访问应用
- 前端应用: http://localhost:8080
- 后端API: http://localhost:8000
- 管理后台: http://localhost:8000/admin

## 📖 使用说明

### 文件上传
1. 点击"上传文件"按钮
2. 拖拽文件到上传区域或点击选择文件
3. 输入文件标题和描述（可选）
4. 点击"开始上传"

### 视频播放
1. 从左侧文件列表选择视频文件
2. 使用Video.js播放器控制播放
3. 支持全屏播放和播放速度调节

### PDF查看
1. 选择PDF文件
2. 使用工具栏进行翻页和缩放
3. 支持鼠标滚轮缩放（Ctrl+滚轮）

### 分屏模式
1. 点击"分屏模式"按钮
2. 左侧显示视频，右侧显示PDF
3. 可以同时查看两种文件类型

## 🎨 设计特色

### 科技风格UI
- 深色主题配色
- 毛玻璃效果背景
- 渐变色彩搭配
- 流畅的动画过渡
- 现代化的图标设计

### 交互体验
- 悬停效果和反馈
- 平滑的动画过渡
- 直观的操作界面
- 响应式布局设计

## 🔧 配置说明

### 后端配置
- 文件上传大小限制：50MB
- 支持的文件类型：视频和PDF
- 数据库：SQLite（可配置为其他数据库）

### 前端配置
- 开发服务器端口：8080
- API代理配置：自动代理到后端
- 构建输出：dist目录

## 📝 API接口

### 文件管理
- `GET /api/files/` - 获取文件列表
- `POST /api/files/` - 上传文件
- `DELETE /api/files/{id}/` - 删除文件
- `GET /api/files/videos/` - 获取视频文件
- `GET /api/files/pdfs/` - 获取PDF文件

## 🐛 故障排除

### 常见问题
1. **文件上传失败**
   - 检查文件大小是否超过50MB
   - 确认文件格式是否支持

2. **视频无法播放**
   - 检查浏览器是否支持该视频格式
   - 确认视频文件是否损坏

3. **PDF无法加载**
   - 检查PDF文件是否损坏
   - 确认网络连接正常

### 日志查看
- 后端日志：控制台输出
- 前端日志：浏览器开发者工具

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 项目讨论区

---

**享受您的视频和PDF浏览体验！** 🎉
