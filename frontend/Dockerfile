# 使用Node.js 16官方镜像作为基础镜像
FROM node:16-alpine

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json文件到工作目录
COPY package*.json ./

# 安装Node.js依赖
RUN npm install

# 复制前端应用的所有文件到工作目录
COPY . .

# 暴露端口
EXPOSE 8080

# 构建生产版本
RUN npm run build

# 安装serve来运行生产版本
RUN npm install -g serve

# 运行前端应用
CMD ["serve", "-s", "dist", "-l", "8080"]