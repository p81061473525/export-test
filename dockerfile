# 使用官方的 Python 3 映像作為基礎映像
FROM python:3

# 將工作目錄設置為 /app
WORKDIR /app

# 複製 Python 腳本到容器中的 /app 目錄
COPY redis_exporter.py .

# 安裝依賴的 Python 模組
RUN pip install prometheus_client requests
# 安裝依賴的 Python 模組

# 暴露容器內部監聽的端口
EXPOSE 51921

# 使用 python 命令執行 Python 腳本
CMD ["python", "redis_exporter.py"]

