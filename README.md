#############**Weather Kafka Pipeline**###############  

This project demonstrates how to fetch the data in real-time from weather API using Kafka.  
It fetches current weather information from WeatherAPI and produces the data to a Kafka topic, making it available for downstream consumers to process.  
Complete pipeline is orchestrated through Apache Airflow  
  

#NOTE:
Kafka and Zookeeper services are invoked from localhost  
Python code triggered from Docker  
  
**Features:**  
> Fetch live weather data for any city using WeatherAPI.
> Produce weather data to Apache Kafka topic.
> Simple Kafka Consumer to read weather updates.
> Clean Python code with requests, kafka-python.
> Configurable Kafka settings using a Python class.  

  

**Project Structure:**  

weather-kafka-pipeline/  
.  
├── README.md  
├── Dockerfile  
├── Kafka_check_01.iml  
├── dags  
│   └── weather_pipeline_dag.py  
├── docker-compose.yml  
├── kafka_environment  
│   ├── kafka-console-consumer.cmd  
│   ├── kafka-server-start.cmd  
│   ├── kafka-topics-create.cmd  
│   └── zookeeper-start.cmd  
├── requirements.txt  
├── src  
│   ├── __pycache__  
│   ├── api_extract.py  
│   ├── data_consumer.py  
│   ├── data_producer.py  
│   ├── settings.py  
│   └── venv  
└── venv  
    ├── bin  
    ├── include  
    ├── lib  
    ├── lib64 -> lib  
    └── pyvenv.cfg  
    


docker build -t weather-kafka-app .
