# 使用Python 3.9官方镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt文件到工作目录
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端应用的所有文件到工作目录
COPY . .

# 暴露端口
EXPOSE 5000

# 运行Flask应用
CMD ["python", "app.py"]