from confluent_kafka import Producer, KafkaError
from config.settings import KAFKA_PRODUCER_CONFIG
from utils.logger import get_logger
from confluent_kafka.serialization import StringSerializer

log = get_logger(__name__)


class KafkaProducer:
    def __init__(self):
        self.producer = Producer(KAFKA_PRODUCER_CONFIG)
        log.info('Kafka Producer init with config: %s', KAFKA_PRODUCER_CONFIG)

    def delivery_report(self, err, msg):
        # delivery report callback called executes every time a record success sent or an exception is thrown
        if err is not None:
            log.error(f"Message delivery failed: {err}")
            if err.code() == KafkaError.REQUEST_TIMED_OUT:
                log.warning("Message timeout delivery: %s", err)
        else:
            log.info(
                f"Message delivered to topic: {msg.topic()} key: {msg.key().decode('utf-8')} partition: [{msg.partition()}] at offset {msg.offset()}"
            )

    def produce_message(self, topic, key, value):
        serialized_key = StringSerializer(key)
        serialized_value = StringSerializer(value)

        self.producer.produce(
            topic, key=serialized_key, value=serialized_value, callback=self.delivery_report
        )
        log.debug(f"Message '{value}' send to topic '{topic}' with key '{key}'")

    def flush(self):
        # tell the producer to send all data and block until done -- synchronous
        log.info("Flushing producer messages")
        self.producer.flush()

