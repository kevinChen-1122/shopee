from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import os


class KafkaClient:
    def __init__(self, brokers=None):
        self.brokers = brokers or os.getenv("KAFKA_BROKERS", "localhost:9092")

    # 初始化 Kafka 生产者
    def create_producer(self):
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.brokers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 序列化消息为 JSON 格式
            )
            return producer
        except KafkaError as e:
            print(f"Failed to create Kafka producer: {e}")
            return None

    # 发送消息到 Kafka
    def send_message(self, producer, topic, message):
        try:
            future = producer.send(topic, value=message)
            producer.flush()  # 强制刷新消息
            future.get(timeout=10)  # 确保消息成功发送
            print(f"Message sent to {topic}: {message}")
        except KafkaError as e:
            print(f"Failed to send message: {e}")

    # 初始化 Kafka 消费者
    def create_consumer(self, topic, group_id=None):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.brokers,
                group_id=group_id or "default_group",
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),  # 反序列化 JSON 格式的消息
                auto_offset_reset='earliest',  # 从头开始消费
                enable_auto_commit=True
            )
            return consumer
        except KafkaError as e:
            print(f"Failed to create Kafka consumer: {e}")
            return None

    # 消费消息
    def consume_messages(self, consumer):
        try:
            for message in consumer:
                print(f"Received message: {message.value}")
                # 在这里处理接收到的消息
        except KafkaError as e:
            print(f"Failed to consume messages: {e}")
