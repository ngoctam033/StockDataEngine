# Sử dụng image Python chính thức làm base image
FROM python:3.9-slim

# Đặt biến môi trường để buffer output
ENV PYTHONUNBUFFERED 1

# Tạo thư mục làm việc
WORKDIR /app

# Cài đặt các gói phụ thuộc Python
RUN pip install --no-cache-dir psycopg2-binary confluent_kafka

# Sao chép mã nguồn vào thư mục làm việc
COPY . /app/

# Định nghĩa lệnh chạy khi container khởi động
CMD ["python", "kafka_consumer.py"]