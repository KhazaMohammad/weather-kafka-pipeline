from kafka import KafkaConsumer
from settings import Settings
import json
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

# Azure Key Vault: retrieve secret
key_vault_url = "https://pipeline01secrets.vault.azure.net"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
account_key = secret_client.get_secret("ADLS-ACCOUNT-KEY").value
client_id = secret_client.get_secret("AZURE-CLIENT-ID").value
tenant_id = secret_client.get_secret("AZURE-TENANT-ID").value
client_secret = secret_client.get_secret("AZURE-CLIENT-SECRET").value

# ADLS Config
account_name = "mypipeline01"
file_system_name = "mypipelinecontainer-dev"
directory_name = "weather_jsons"
account_url = f"https://{account_name}.dfs.core.windows.net"

# Initialize ADLS Gen2 Client using DefaultAzureCredential (no shared key needed)
service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
file_system_client = service_client.get_file_system_client(file_system=file_system_name)

# Ensure base directory exists
try:
    directory_client = file_system_client.get_directory_client(directory_name)
    directory_client.create_directory()
except Exception as e:
    print(f"Directory may already exist or error occurred: {e}")

# Kafka Settings
kafka_settings = Settings()

# Kafka Consumer
consumer = KafkaConsumer(
    kafka_settings.topic,
    bootstrap_servers=kafka_settings.kafka_bootstrap_servers,
    security_protocol=kafka_settings.kafka_security_protocol,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="consumer-grp",
    consumer_timeout_ms=10000
)

# Process Kafka messages
for message in consumer:
    city = message.key
    weather_data = message.value

    print(f"Received message for {city}")

    # Create city-level subdirectory if not exists
    city_directory = directory_client.get_sub_directory_client(city.lower())
    try:
        city_directory.create_directory()
    except Exception:
        pass  # Ignore if already exists

    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"{city.lower()}_{timestamp}.json"
    json_data = json.dumps(weather_data, indent=2)

    # Upload JSON to ADLS Gen2
    file_client = city_directory.create_file(file_name)
    file_client.append_data(data=json_data, offset=0, length=len(json_data))
    file_client.flush_data(len(json_data))

    print(f"Uploaded {file_name} under folder '{city.lower()}' in ADLS Gen2")