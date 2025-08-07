from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from dotenv import load_dotenv
# Add the Airflow variables before run

load_dotenv(dotenv_path='/opt/airflow/.env')

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
        #schedule_interval=None, 
        schedule_interval='0 * * * *',
        start_date=datetime(2025, 7, 21),
        dagrun_timeout=timedelta(seconds=5000),
        catchup=False,
) as dag:

    run_producer = DockerOperator(
        task_id='run_producer',
        image='weather-kafka-pipeline_weather-app:latest',  # This should match the image used in your docker-compose
        api_version='auto',
        auto_remove=True,
        command='python3 src/data_producer.py',
        environment={
            'AZURE_CLIENT_ID': Variable.get('AZURE_CLIENT_ID'),
            'AZURE_TENANT_ID': Variable.get('AZURE_TENANT_ID'),
            'AZURE_CLIENT_SECRET': Variable.get('AZURE_CLIENT_SECRET'),
            'KAFKA_BOOTSTRAP_SERVERS': Variable.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        },
        docker_url="unix://var/run/docker.sock",
        mount_tmp_dir=False,
        network_mode='weather-kafka-pipeline_default',
    )

    run_consumer = DockerOperator(
        task_id='run_consumer',
        image='weather-kafka-pipeline_weather-app:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 src/data_consumer.py',
        environment={
            'AZURE_CLIENT_ID': Variable.get('AZURE_CLIENT_ID'),
            'AZURE_TENANT_ID': Variable.get('AZURE_TENANT_ID'),
            'AZURE_CLIENT_SECRET': Variable.get('AZURE_CLIENT_SECRET'),
            'KAFKA_BOOTSTRAP_SERVERS': Variable.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        },
        docker_url="unix://var/run/docker.sock",
        mount_tmp_dir=False,
        network_mode='weather-kafka-pipeline_default',
    )

    run_producer >> run_consumer
