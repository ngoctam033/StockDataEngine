# Sử dụng image Node.js chính thức từ Docker Hub
FROM node:20

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file package.json và package-lock.json vào thư mục làm việc
COPY package*.json ./

# Cài đặt các dependencies cần thiết
RUN npm install

# Cài đặt Nodemon cho môi trường phát triển
RUN npm install -g nodemon

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Lệnh để chạy ứng dụng Node.js
CMD ["nodemon", "server.js"]