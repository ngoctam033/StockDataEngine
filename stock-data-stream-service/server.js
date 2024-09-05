// đậy là file để tạo server
//cài thư viện kafkais
const { Kafka } = require('kafkajs');
//cài thư viện web socket
const WebSocket = require('ws');

//tạo một server web socket
const wss = new WebSocket.Server({ port: 3000 });

//cài đặt các sự kiện cho server web socket
wss.on('connection', function connection(ws) {
    console.log('Có một kết nối mới');

    //khi nhận được dữ liệu từ client
    ws.on('message', function incoming(message) {
        console.log('Đã nhận dữ liệu từ client: %s', message);
    });

    //khi có lỗi xảy ra
    ws.on('error', function error(error) {
        console.error('Có lỗi xảy ra:', error);
    });
});

//tạo một kafka consumer
const kafka = new Kafka({
    clientId: 'websocket-service',
    brokers: ['kafka-1:9093']
});

//tạo một consumer với groupId là websocket-group
const consumer = kafka.consumer(
    {
        groupId: 'stock-data-group',
        // cấu hình thành viên tĩnh
        groupInstanceId: 'stock-data-group-1'
    });

// hàm runConsumer
const runConsumer = async () => {
    //kết nối tới kafka
    await consumer.connect();
    console.log('Kafka Consumer đã kết nối');

    //subscribe tới topic stock_topic
    await consumer.subscribe({ topic: 'stock_topic', fromBeginning: true });


    //chạy consumer
    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            try {
                const stockData = JSON.parse(message.value.toString());
                console.log(`Dữ liệu từ topic: ${topic}, partition: ${partition}, offset: ${message.offset}:`);
    
                const totalClients = wss.clients.size;
                
                const startTime = Date.now();
                // Gửi dữ liệu tới tất cả các client đang kết nối
                wss.clients.forEach(function each(client) {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(stockData));
                    }
                });
    
                const endTime = Date.now();
                const elapsedTime = endTime - startTime;
    
                console.log(`Đã gửi dữ liệu tới tất cả ${totalClients} client(s) trong ${elapsedTime} ms`);
    
            } catch (error) {
                console.error('Lỗi khi xử lý hoặc lưu trữ dữ liệu:', error);
            }
        },
    });
};

//chạy consumer
runConsumer().catch(console.error);