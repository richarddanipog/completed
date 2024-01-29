import json
import logging
import os
from datetime import datetime
from kafka import KafkaConsumer
from pymongo import MongoClient
import configparser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_kafka(config):
    try:
        consumer = KafkaConsumer(
            config['Kafka']['topic'],
            bootstrap_servers=config['Kafka']['kafka_server'],
            api_version=(0, 11, 5),
            auto_offset_reset=config['Kafka']['auto_offset_reset'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        return consumer
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        raise

def connect_to_mongodb(config):
    try:
        mongo_client = MongoClient(config['MongoDb']['connection_string'])
        db = mongo_client[config['MongoDb']['db_name']]
        collection = db[config['MongoDb']['db_collection_name']]

        return collection
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def process_message(message, collection):
    try:
        event_data = message.value
        event_data["timestamp"] = datetime.strptime(event_data["timestamp"], '%Y-%m-%d-%H:%M:%S')
        collection.insert_one(event_data)

        logger.info("Inserted event into MongoDB")
    except Exception as e:
        logger.error(f"Failed to process message: {e}")

def main():
    try:
        # Load configuration from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')

        consumer = connect_to_kafka(config)

        collection = connect_to_mongodb(config)

        for message in consumer:
            logger.info("Received message from Kafka")
            process_message(message, collection)
    except KeyboardInterrupt:
        logger.info("Exiting...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
