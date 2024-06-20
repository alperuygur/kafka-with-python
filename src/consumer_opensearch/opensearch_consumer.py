import json
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
from opensearchpy import helpers
from utils.logger import get_logger

log = get_logger(__name__)


class KafkaOpenSearchConsumer:
    def __init__(self, topic, group_id, opensearch_client, bootstrap_servers='localhost:9092'):
        self.topic = topic
        self.group_id = group_id
        self.opensearch_client = opensearch_client
        self.bootstrap_servers = bootstrap_servers
        self.consumer = self.create_consumer()

    def create_consumer(self):
        consumer_conf = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': False
        }
        consumer = Consumer(consumer_conf)
        consumer.subscribe([self.topic])
        log.info(f"Kafka consumer created for topic: {self.topic}, group_id: {self.group_id}")
        return consumer

    def consume_and_index(self):
        try:
            self.opensearch_client.create_index_if_not_exists("wikimedia")

            while True:
                msg = self.consumer.poll(timeout=0.3)  # 300 milliseconds
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        log.info(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                    elif msg.error():
                        log.error(f"Error occurred: {msg.error()}")
                        continue

                record_value = msg.value().decode('utf-8')
                try:
                    doc_id = self.extract_id(record_value)
                    index_doc = {
                        "_index": "wikimedia",
                        "_id": doc_id,
                        "_source": json.loads(record_value)
                    }
                    self.opensearch_client.index_document(index_doc)
                    log.info(f"Document indexed with ID: {doc_id}")
                    self.consumer.commit()
                except Exception as e:
                    log.error(f"Error processing record: {e}")


        except KafkaError as ke:
            log.error(f"Kafka error: {ke}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
        finally:
            self.consumer.close()
            log.info("Kafka consumer closed.")
            self.opensearch_client.close()


    @staticmethod
    def extract_id(record_value):
        """
        GEt unique ID from the records.
        """
        try:
            return json.loads(record_value).get('id', None)
        except json.JSONDecodeError as e:
            log.error(f"JSON decode error: {e}")
            return None
