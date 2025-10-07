import yaml
import time
import random
import logging.config
from pykafka import KafkaClient
from pykafka.exceptions import KafkaException

with open("./config/logging_config.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

class KafakProducer:
    def __init__ (self, host, topic):
        self.host = host
        self.topic = topic
        self.client = None
        self.producer = None
        self.connect()
    
    def connect(self):
        while True:
            logger.debug("Trying to connect to Kafka...")
            if self.make_client():
                if self.make_producer():
                    break
        time.sleep(random.randint(500, 1500)/1000)
    
    def make_client(self):
        if self.client is not None:
            return True
        try:
            self.client = KafkaClient(hosts=self.host)
            logger.info("Kafka client created!")
            return True
        except KafkaException as e:
            msg = f"Kafka error when making client: {e}"
            logger.warning(msg)
            self.client = None
            self.producer = None
            return False
        
    def make_producer(self):
        if self.producer is not None:
            return True
        if self.client is None:
            return False
        try:
            topic = self.client.topics[self.topic]
            self.producer = topic.get_sync_producer()
        except KafkaException as e:
            msg = f"Error to make producer: {e}"
            logger.warning(msg)
            self.client = None

    def produce_message(self, message):
        if self.producer is None:
            self.connect()
        try:
            self.producer.produce(message.encode("utf-8"))
            logger.info("Message produced successfully")
        except KafkaException as e:
            logger.warning("Error to product message: {e}")
            self.client = None
            self.producer = None
            self.connect()
