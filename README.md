#############**Weather Kafka Pipeline**###############  

This project demonstrates how to fetch the data in real-time from weather API using Kafka.  
It fetches current weather information from WeatherAPI and produces the data to a Kafka topic, making it available for downstream consumers to process.  


  
**Features:**  
> Fetch live weather data for any city using WeatherAPI.
> Produce weather data to Apache Kafka topic.
> Simple Kafka Consumer to read weather updates.
> Clean Python code with requests, kafka-python.
> Configurable Kafka settings using a Python class.  

  

**Project Structure:**  

weather-kafka-pipeline/  
├── README.md  
├── docker-compose.yml  
├── Dockerfile  
├── requirements.txt  
└── src/  
------├── data_producer.py  
------├── data_consumer.py  
------├── settings.py  
------├── api_extract.py  
└── kafka_environment/    
------├── kafka-console-consumer.cmd    
------├── kafka-server-start.cmd    
------├── kafka-topics-create.cmd    
------├── zookeeper-start.cmd  
