from faker import Faker
from datetime import datetime
import configparser

class Event:
    fake = Faker()
    
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        self.reporter_counter = int(self.config.get('Event', 'reporterId_counter_start', fallback=0))
        self.reporter_counter_increment = int(self.config.get('Event', 'reporterId_counter_increment_number', fallback=1))
        self.metric_id_min = int(self.config.get('Event', 'metricId_min', fallback=1))
        self.metric_id_max = int(self.config.get('Event', 'metricId_max', fallback=1000))
        self.metric_value_min = int(self.config.get('Event', 'metric_value_min', fallback=1))
        self.metric_value_max = int(self.config.get('Event', 'metric_value_max', fallback=100))

    def generate_event(self):
        self.reporter_counter += self.reporter_counter_increment
        
        return {
            "reporterId": self.reporter_counter,
            "timestamp": datetime.strftime(datetime.now(), '%Y-%m-%d-%H:%M:%S'),
            "metricId": self.fake.random_int(min=self.metric_id_min, max=self.metric_id_max),
            "metricValue": self.fake.random_int(min=self.metric_value_min, max=self.metric_value_max),
            "message": self.fake.text(),
        }
