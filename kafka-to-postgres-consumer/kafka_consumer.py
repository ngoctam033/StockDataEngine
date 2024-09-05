# import thư viện psycopg2 để kết nối với PostgreSQL
import psycopg2
import json
# import thư viện confluents_kafka để kết nối với Kafka
from confluent_kafka import Consumer, KafkaException

# tạo hàm chính
def main():
    # đầu tiên, kết nối với PostgreSQL
    conn = psycopg2.connect(
        host="postgresql",
        database="stock_db",
        user="postgres",
        password="postgres",
        port="5432"
    )
    print("Kết nối với PostgreSQL thành công")

    # tạo một con trỏ để thực thi các câu lệnh SQL
    cur = conn.cursor()
    # cho biết tạo cursor thành công
    print("Tạo cursor thành công")

    # tạo một consumer để kết nối với Kafka
    consumer = Consumer({
        'bootstrap.servers': 'kafka-1:9093',
        'group.id': 'kafka-to-postgres-consumer',
        'auto.offset.reset': 'earliest'
    })
    # subscribe vào topic 'stock'
    consumer.subscribe(['stock_topic'])
    # sau đó, bắt đầu vòng lặp để lấy dữ liệu từ Kafka
    try:
        while True:
            try:
                # lấy dữ liệu từ Kafka
                msg = consumer.poll(timeout=1.0)
                # nếu có dữ liệu
                if msg is not None:
                    # lấy dữ liệu từ Kafka
                    data = json.loads(msg.value())
                    
                    # tạo một vòng lặp duyệt list data
                    for record in data:
                        ticker = record['ticker']
                        date = record['date']
                        vol = record['vol']
                        now = record['now']

                        # thực thi câu lệnh SQL để insert dữ liệu vào bảng stock
                        try:
                            cur.execute("INSERT INTO stock_data (ticker, date, vol, now) VALUES (%s, %s, %s, %s)", (ticker, date, vol, now))
                            # commit dữ liệu
                            conn.commit()
                            print("Insert dữ liệu thành công")
                        except Exception as e:
                            print("Lỗi khi insert dữ liệu:")
                            print(e)
                            # rollback nếu có lỗi
                            conn.rollback()
            except Exception as e:
                print("Lỗi không xác định:")
                print(e)
    finally:
        # đóng consumer
        consumer.close()
        # đóng cursor
        cur.close()
        # đóng kết nối
        conn.close()

# chạy hàm chính
main()
