import json
import os
from time import sleep
from kafka import KafkaProducer
from event import Event
import configparser

# Load configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=config['Kafka']['kafka_server'],
    api_version=(0, 11, 5),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def generate_event_and_send(producer, topic):
    """Generate event data, send it to Kafka, and flush the producer."""
    try:
        event_instance = Event()
        event_data = event_instance.generate_event()

        # Send event data to Kafka
        producer.send(topic, event_data)
        producer.flush()

        print("Event sent successfully:", event_data)
    except Exception as e:
        print("Error sending event to Kafka:", e)

def main():
    """Main function to continuously generate and send events to Kafka."""
    try:
        while True:
            generate_event_and_send(producer, config['Kafka']['topic'])
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
