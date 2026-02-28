# 使用 Docker Hub 官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

RUN echo "deb http://mirrors.aliyun.com/debian/ trixie main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ trixie-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security/ trixie-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list

RUN rm /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件到容器中
COPY . /app

# 设置环境变量（包含子模块路径）
ENV PYTHONPATH=/app:/app/perfectPixel/src

# 升级pip并安装依赖
RUN pip install --upgrade pip && pip install -r requirements.txt

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# 运行应用
CMD ["python", "api/main.py"]
