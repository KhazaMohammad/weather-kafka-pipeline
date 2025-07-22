from kafka import KafkaConsumer
from settings import Settings
import json

# Load settings
kafka_settings_obj = Settings()

# Create Kafka Consumer
consumer = KafkaConsumer(
    kafka_settings_obj.topic,
    bootstrap_servers=kafka_settings_obj.kafka_bootstrap_servers,
    security_protocol=kafka_settings_obj.kafka_security_protocol,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="consumer-grp"
)

print(f"topic name : {kafka_settings_obj.topic}")

# display messages
for message in consumer:
    print(f"Key: {message.key}")
    print(f"Value: {message.value}")
    print(f"Partition: {message.partition}, Offset: {message.offset}")