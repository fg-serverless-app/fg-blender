# 使用官方Ubuntu镜像作为基础
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    python3-pip \
    libgl1-mesa-glx \
    libegl1-mesa \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    libxkbcommon-x11-0 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

# 安装Blender
RUN wget https://download.blender.org/release/Blender4.3/blender-4.3.2-linux-x64.tar.xz && \
    tar -xf blender-4.3.2-linux-x64.tar.xz && \
    mv blender-4.3.2-linux-x64 /opt/blender && \
    ln -s /opt/blender/blender /usr/local/bin/blender && \
    rm blender-4.3.2-linux-x64.tar.xz

# 安装Python依赖
COPY requirements.txt .
RUN pip3 install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 复制应用文件
COPY --chown=1003:1003 ./data ./data
COPY --chown=1003:1003 ./static ./static
COPY --chown=1003:1003 index.html .
COPY --chown=1003:1003 fastapi_server.py .

# /data/startup.blend /data/output/mp4_

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]