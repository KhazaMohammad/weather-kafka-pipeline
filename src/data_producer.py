from kafka import KafkaProducer
from settings import Settings
import json
from api_extract import fetch_city_weather
import time


# Object creation
kafka_settings_obj = Settings()

# Producer Creation
producer = KafkaProducer(bootstrap_servers=kafka_settings_obj.kafka_bootstrap_servers,
                         security_protocol=kafka_settings_obj.kafka_security_protocol,
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                         retries=3)

cities = ["Mumbai", "Delhi", "Chennai", "Kolkata", "Bangalore"]
for city in cities:
    try:
        data = fetch_city_weather(city_name=city)
        print(f"Fetched data for {city}")
        print(json.dumps(data, indent=2))

        # send the event to broker
        producer.send(topic=kafka_settings_obj.topic,
                      key = data["location"]["name"].encode("utf-8"),
                      value=data
                      )
        time.sleep(1)
    except Exception as e:
        print(f"Error fetching or sending data for {city}: {e}")
producer.flush()
