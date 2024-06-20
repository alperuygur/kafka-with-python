from consumer_opensearch.opensearch_consumer import  KafkaOpenSearchConsumer
from opensearch.opensearch_client import OpenSearchClient
from utils.logger import get_logger


log = get_logger(__name__)


def main():
    opensearch_url = "http://localhost:9200"
    opensearch_client = OpenSearchClient(opensearch_url)
    consumer_group_id = "wikimedia-consumer-group"
    topic = "wikimedia.recentchange"

    kafka_consumer_client = KafkaOpenSearchConsumer(
        topic=topic,
        group_id=consumer_group_id,
        opensearch_client=opensearch_client
    )
    kafka_consumer_client.consume_and_index()


if __name__ == "__main__":
    log.debug("Starting Kafka Consumer")
    main()
