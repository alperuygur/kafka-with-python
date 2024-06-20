KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': 'kafka:9092',  # Change this to your Kafka server address
    'client.id': 'python-producer',
    'acks': 'all',  # Wait for all in-sync replicas to acknowledge the message
    'retries': 3,   # Number of retries if the delivery fails
    'linger.ms': 100,  # Time to wait before sending the batch
    'batch.num.messages': 1000  # Maximum number of messages per batch

}
KAFKA_CONSUMER_CONFIG = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'consumer-opensearch-demo',
    'auto.offset.reset': 'latest'
}


"""
Default Partitioner Behavior
Round-Robin: Kafka's default behavior, when no key is provided for a message, 
is to use a round-robin partitioner. This means messages are evenly distributed across partitions in a topic sequentially.
"""