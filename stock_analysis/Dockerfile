# Sử dụng image Python chính thức làm base image
FROM python:3.12-slim

# Đặt biến môi trường để buffer output
ENV PYTHONUNBUFFERED 1

# Tạo thư mục làm việc
WORKDIR /app

# Cài đặt các gói phụ thuộc Python
RUN pip install --no-cache-dir fastapi uvicorn

# Sao chép mã nguồn vào thư mục làm việc
COPY . /app/

# Định nghĩa lệnh chạy khi container khởi động
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]