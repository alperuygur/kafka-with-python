import json
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from opensearchpy.exceptions import ConnectionError, TransportError
from utils.logger import get_logger

log = get_logger(__name__)


class OpenSearchClient:
    def __init__(self, opensearch_url):
        self.opensearch_url = opensearch_url
        self.client = self.create_opensearch_client()

    def create_opensearch_client(self):
        try:
            client = OpenSearch(self.opensearch_url)
            log.info(f"Connected to OpenSearch: {client.info()}")
            return client
        except (ConnectionError, TransportError) as e:
            log.error(f"Failed to connect to OpenSearch: {e}")
            raise

    def create_index_if_not_exists(self, index_name):
        try:
            index_exists = self.client.indices.exists(index=index_name)
            if not index_exists:
                self.client.indices.create(index=index_name)
                log.info(f"Created index '{index_name}' in OpenSearch")
            else:
                log.info(f"Index '{index_name}' already exists in OpenSearch")
        except Exception as e:
            log.error(f"Error creating index '{index_name}' in OpenSearch: {e}")

    def index_document(self, document):
        try:
            self.client.index(
                index=document["_index"],
                id=document["_id"],
                body=document["_source"]
            )
        except Exception as e:
            log.error(f"Error indexing document: {e}")

    def bulk_index(self, documents):
        """
        Bulk index the given documents into OpenSearch.
        """
        try:
            log.info("Starting bulk indexing operation.")
            if not documents:
                log.warning("No documents to index.")
                return

            # Send the documents to OpenSearch in bulk
            success, failed = bulk(self.client, documents)

            if failed:
                log.error(f"Failed to index some documents: {failed}")

            log.info(f"Successfully indexed {success} records into OpenSearch.")
            return success
        except Exception as e:
            log.error(f"Error during bulk indexing: {e}")
            return 0

    def close(self):
        try:
            self.client.transport.close()
            log.info("OpenSearch client closed.")
        except Exception as e:
            log.error(f"Error closing OpenSearch client: {e}")
