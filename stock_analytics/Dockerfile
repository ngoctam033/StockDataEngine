# Sử dụng image Python chính thức làm base image
FROM python:3.12-slim

# Đặt biến môi trường để buffer output
ENV PYTHONUNBUFFERED 1

# Tạo thư mục làm việc
WORKDIR /app

# Cài đặt Java và các gói phụ thuộc khác
RUN apt-get update && apt-get install -y openjdk-17-jdk-headless procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập biến môi trường JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# Cài đặt các gói phụ thuộc Python
RUN pip install --no-cache-dir fastapi uvicorn pyspark plotly pandas setuptools

# Sao chép mã nguồn vào thư mục làm việc
COPY . /app/

# Định nghĩa lệnh chạy khi container khởi động
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]