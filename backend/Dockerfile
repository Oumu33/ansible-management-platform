# 使用官方Python 3.11镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    sshpass \
    build-essential \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装Ansible
RUN pip install --no-cache-dir ansible ansible-core

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/data/files/config \
    /app/data/files/inventory \
    /app/data/files/playbooks \
    /app/data/logs

# 设置权限
RUN chmod +x /app/scripts/start.sh || echo "start.sh not found, skipping"

# 创建非root用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHEK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]