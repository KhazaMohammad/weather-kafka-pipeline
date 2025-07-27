from kafka import KafkaConsumer
from settings import Settings
import json
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
import re
import os
from dotenv import load_dotenv

# Load Kafka settings
kafka_settings_obj = Settings()

# Kafka Consumer
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
load_dotenv()

# Azure ADLS config
account_name = "mypipeline01"
account_key = os.getenv("ADLS_ACCOUNT_KEY")
file_system_name = "mypipelinecontainer-dev"
directory_name = "weather_jsons"

# Setup ADLS Client
service_client = DataLakeServiceClient(
    account_url=f"https://{account_name}.dfs.core.windows.net",
    credential=account_key
)
file_system_client = service_client.get_file_system_client(file_system=file_system_name)

# Ensure directory exists
try:
    directory_client = file_system_client.get_directory_client(directory_name)
    directory_client.create_directory()
except Exception as e:
    print(f"Directory already exists or error: {e}")

    kafka_settings_obj.topic,
    bootstrap_servers=kafka_settings_obj.kafka_bootstrap_servers,
    security_protocol=kafka_settings_obj.kafka_security_protocol,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="consumer-grp"
)

load_dotenv()

# Azure ADLS config
account_name = "mypipeline01"
account_key = os.getenv("ADLS_ACCOUNT_KEY")
file_system_name = "mypipelinecontainer-dev"
directory_name = "weather_jsons"

# Setup ADLS Client
service_client = DataLakeServiceClient(
account_url=f"https://{account_name}.dfs.core.windows.net",
credential=account_key
)
file_system_client = service_client.get_file_system_client(file_system=file_system_name)

# Ensure directory exists
try:
    directory_client = file_system_client.get_directory_client(directory_name)
    directory_client.create_directory()
except Exception as e:
    print(f"Directory already exists or error: {e}")

# Consume messages
for message in consumer:
    city = message.key
    weather_data = message.value

    print(f"Received message for {city}")

    city_directory = directory_client.get_sub_directory_client(city.lower())
    city_directory.create_directory()

    # Unique file name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"{city.lower()}_{timestamp}.json"


    json_data = json.dumps(weather_data, indent=2)
    # Upload to ADLS
    file_client = city_directory.create_file(file_name)
    file_client.append_data(data=json_data, offset=0, length=len(json_data))
    file_client.flush_data(len(json_data))

    print(f"Uploaded {file_name} under folder '{city.lower()}' in ADLS Gen2")