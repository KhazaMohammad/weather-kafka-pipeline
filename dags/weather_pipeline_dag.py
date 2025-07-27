from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
        dag_id='weather_kafka_pipeline',
        default_args=default_args,
        description='Run weather data producer and consumer using Kafka',
        schedule_interval=None,  # Trigger manually or use e.g., '*/30 * * * *' for every 30 mins
        start_date=datetime(2025, 7, 21),
        dagrun_timeout=timedelta(seconds=5000),
        catchup=False,
) as dag:

    run_producer = DockerOperator(
        task_id='run_producer',
        image='weather-kafka-app:latest',  # This should match the image used in your docker-compose
        api_version='auto',
        auto_remove=True,
        command='python3 src/data_producer.py',
        docker_url='tcp://host.docker.internal:2375',
        network_mode='weather-kafka-pipeline_default',
    )

    run_consumer = DockerOperator(
        task_id='run_consumer',
        image='weather-kafka-app:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 src/data_consumer.py',
        docker_url='tcp://host.docker.internal:2375',
        network_mode='weather-kafka-pipeline_default',
    )

    run_producer >> run_consumer
