import json
import redis
from pymongo import MongoClient
from datetime import datetime
import time
import configparser
import threading

# Load configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Connect to MongoDB
mongo_client = MongoClient(config['MongoDb']['connection_string'])
mongo_db = mongo_client[config['MongoDb']['db_name']]
mongo_collection = mongo_db[config['MongoDb']['db_collection_name']]

# Connect to Redis
redis_client = redis.Redis(
    host=config['Redis']['redis_host_name'],
    port=config.getint('Redis', 'redis_port'),
    decode_responses=True
)

def get_latest_timestamp():
    """Retrieve the latest timestamp from Redis."""
    latest_timestamp = redis_client.get('latest_timestamp')
    if latest_timestamp:
        return datetime.strptime(latest_timestamp, '%Y-%m-%d-%H:%M:%S')
    
    return None

def update_latest_timestamp(timestamp):
    """Update the latest timestamp in Redis."""
    redis_client.set('latest_timestamp', timestamp.strftime('%Y-%m-%d-%H:%M:%S'))

    print(f"Updated latest timestamp in Redis: {timestamp}")

def process_new_objects():
    """Process new objects from MongoDB and store them in Redis."""
    latest_timestamp = get_latest_timestamp()

    query = {"timestamp": {"$gt": latest_timestamp}} if latest_timestamp else {}
    new_objects = list(mongo_collection.find(query).sort("timestamp", 1))

    for obj in new_objects:
        key = f"{obj['reporterId']}:{datetime.strftime(obj['timestamp'], '%Y-%m-%d-%H:%M:%S')}"
        obj_json = json.dumps(obj, default=str)
        redis_client.set(key, obj_json)

        print(f"Inserted new object into Redis: {obj_json}")
        
        update_latest_timestamp(obj['timestamp'])

def run_process_new_objects():
    """Wrapper function to run process_new_objects in a separate thread."""
    while True:
        process_new_objects()
        time.sleep(config.getint('Redis', 'redis_sleep_time'))

def main():
    """Main function to start the thread."""
    thread = threading.Thread(target=run_process_new_objects)
    thread.start()

    try:
        thread.join()
    except KeyboardInterrupt:
        print("Exiting...")
        thread.join()

if __name__ == "__main__":
    main()
