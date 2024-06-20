import time
import json
import threading
from urllib.parse import urlparse

import httpx
import requests
import sseclient
from httpx import AsyncClient, ConnectTimeout, HTTPStatusError
from handler.wikimedia_change_handler import WikimediaChangeHandler
from producer.kafka_producer import KafkaProducer
from utils.logger import get_logger


log = get_logger(__name__)

def with_httpx(url, headers):
    """
    Get a streaming response for the given event feed using httpx.
    """
    with httpx.stream('GET', url, headers=headers) as s:
        yield from s.iter_bytes()

def start_sse_event_source(handler: WikimediaChangeHandler, sse_url: str):
    """
    Start the SSE event source using sseclient-py.
    """
    try:
        headers = {'Accept': 'text/event-stream'}  # https://pypi.org/project/sseclient-py/
        event_source = with_httpx(sse_url, headers)
        client = sseclient.SSEClient(event_source)
        for event in client.events():
            if event.event == 'message':
                try:
                    data_str = event.data
                    data_dict = json.loads(data_str)  # Parse JSON data
                    log.debug(f"Received data: {data_dict}")
                    handler.on_message('wikimedia_change_event', {'data': data_dict})
                except json.JSONDecodeError:
                    log.warning("Received invalid JSON data")
                except UnicodeDecodeError:
                    log.warning("Failed to decode SSE data")
    except KeyboardInterrupt:
        client.close()
        handler.on_closed()  # Ensure the producer is flushed and closed gracefully.
    except Exception as exc:
        log.error(f"Error occurred in SSE client: {exc}")

def main():
    log.debug("Starting Kafka Producer")
    # Initialize Kafka producer
    producer = KafkaProducer()
    topic = "wikimedia.recentchange"
    # Initialize WikimediaChangeHandler
    handler = WikimediaChangeHandler(producer, topic)
    # Wikimedia SSE stream URL
    sse_url = "https://stream.wikimedia.org/v2/stream/recentchange"
    start_sse_event_source(handler, sse_url)
    # Block the main thread for 10 minutes
    time.sleep(600)  # 10 minutes in seconds



if __name__ == "__main__":
    main()
