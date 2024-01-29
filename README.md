# Kafka Event Processing Project

This project demonstrates event processing using Apache Kafka, MongoDB, and Redis. It consists of two main components: a Kafka producer that generates events and sends them to a Kafka topic, and a Kafka consumer that consumes events from the Kafka topic and stores them in MongoDB. Additionally, a process periodically transfers data from MongoDB to Redis.

## Project Structure

The project is structured as follows:

- `kafka-producer`: Contains the code for the Kafka producer.
- `kafka-consumer`: Contains the code for the Kafka consumer.
- `redis-service`: Contains the code for transferring data from MongoDB to Redis.
- `config.ini`: Configuration file containing environment-specific settings.
- `Dockerfile`: Dockerfile for building the project's Docker images.
- `docker-compose.yml`: Docker Compose configuration for orchestrating the containers.
- `.env`: Environment file containing environment variables used by the project.
- `README.md`: This file.

## Prerequisites

Before running the project, ensure you have the following installed:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/richarddanipog/completed.git
   ```

2. Navigate to the project directory:

   ```bash
   cd (navigate where you clone the project)
   ```

3. Build and start the Docker containers:

   ```bash
   docker-compose up
   ```

4. Verify that the containers are running:

   ```bash
   docker-compose ps
   ```

5. You can now send events to Kafka using the Kafka producer and consume them using the Kafka consumer.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
