class Settings:
    def __init__(self):
        #self.kafka_bootstrap_servers = "localhost:9092"
        self.kafka_bootstrap_servers = "host.docker.internal:9092"
        self.kafka_security_protocol = "PLAINTEXT"
        self.topic = "code_check_01"
        self.api_key = "e825daf14c584975b38124833253004"