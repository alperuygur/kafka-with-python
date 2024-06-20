# Project Name
Wikimedia kafka producer (Python based)

## Description
Wikimedia producer with opensearch consumer demo

## Prerequisites
Ensure you have the following installed and set up before proceeding:

- Virtualenv
- Docker
- Docker Compose
- Python (compatible version)
- Access to modify hosts file (for Kafka setup)

## Setup Instructions

### 1. Create Virtual Environment
Create a Python virtual environment using your preferred method.

### 2. Install Poetry
Install Poetry, a Python dependency management tool.

`pip install poetry`

### 3. Install project dependencies using Poetry.
`poetry install`

### 4. Start Docker Services
Start Docker containers in detached mode

`docker-compose up -d`

### 5. Configure Kafka
Once Docker is up, perform the following steps:

Visit Kafdrop UI to manage Kafka. http://localhost:9000

Create a topic named **"wikimedia.recentchange"** with 3 partitions and replication factor 1 (for local setup).


### 6. Verify OpenSearch (formerly Elasticsearch)
Check if OpenSearch is running properly:

Visit http://localhost:9200 and confirm essential details like name, cluster_name, cluster_uuid, etc.


### 7. Access Kibana Dev Tools
Access Kibana Dev Tools to interact with Elasticsearch:

Visit http://localhost:5601/app/dev_tools#/console 

and execute GET /wikimedia/_doc/523744398 to fetch relevant documents.


## **Additional Configuration (Kafka Host Mapping)**

For proper Kafka functionality on localhost (temporary setup):

Windows:
Run PowerShell as Administrator and add the following line to hosts file:

`Add-Content -Path "C:\Windows\System32\drivers\etc\hosts" -Value "127.0.0.1 kafka"`

Linux:
Use the following command with sudo to append to /etc/hosts:

`echo "127.0.0.1 kafka" | sudo tee -a /etc/hosts`

