import yaml
import time
import random
import logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType
from pykafka.exceptions import KafkaException

with open("./config/logging_config.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

class KafkaConsumer:
    def __init__(self, host, topic):
        self.host = host
        self.topic = topic
        self.client = None
        self.consumer = None
        self.connect()
    
    def connect(self):
        while True:
            logger.debug("Trying to connect to Kafka...")
            if self.make_client():
                if self.make_consumer():
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
            self.consumer = None
            return False
            
    def make_consumer(self):
        if self.consumer is not None:
            return True
        if self.client is None:
            return True
        try:
            topic = self.client.topics[self.topic]
            self.consumer = topic.get_simple_consumer(
                consumer_group = b'event_group',
                reset_offset_on_start = False,
                auto_offset_reset = OffsetType.LATEST,
                # auto_commit_enable = False,
                # consumer_timeout_ms = 1000
            )
        except KafkaException as e:
            msg = f"Error to make consumer: {e}"
            logger.warning(msg)
            self.client = None
    
    def consume_message(self):
        if self.consumer is None:
            self.connect()
        while True:
            try:
                for msg in self.consumer:
                    yield msg
            except KafkaException as e:
                msg = f"Kafka issue in consumer: {e}"
                logger.warning(msg)
                self.client = None
                self.consumer = None
                self.connect()

    def commit(self):
        """Commit the offsets of the consumer"""
        if self.consumer is not None:
            self.consumer.commit_offsets()
            logger.debug("Offsets committed!")
        else:
            logger.warning("Consumer is None, cannot commit offsets.")