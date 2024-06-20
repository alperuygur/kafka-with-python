import json

from confluent_kafka import Producer, KafkaError
from utils.logger import get_logger

log = get_logger(__name__)


class WikimediaChangeHandler:
    def __init__(self, kafka_producer, topic: str):
        self.kafka_producer = kafka_producer
        self.topic = topic

    def on_open(self):
        pass  # Nothing needed here in Python equivalent

    def on_closed(self):
        self.kafka_producer.flush()  # Ensure all pending messages are delivered
        log.info("Kafka producer flushed all messages.")

    def on_message(self, event: str, message_event: dict):
        # Extract data from the message event
        data = message_event.get('data')
        if data:
            try:
                serialized_data = json.dumps(data)
                self.kafka_producer.producer.produce(self.topic, value=serialized_data, callback=self.delivery_report)
            except KafkaError as e:
                log.error(f"Kafka error: {e}")
        else:
            log.warning(f"Received event '{event}' without 'data' key")


    def on_comment(self, comment: str):
        pass  # Nothing needed here in Python equivalent

    def on_error(self, error: Exception):
        log.error("Error in Stream Reading", exc_info=error)

    def delivery_report(self, err, msg):
        if err is not None:
            log.error(f"Message delivery failed: {err}")
        else:
            log.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")
