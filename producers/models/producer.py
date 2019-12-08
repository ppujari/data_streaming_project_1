"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        #
        #
        # TODO: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        self.broker_properties = {
            # TODO
            # TODO
            # TODO
            #"bootstrap.servers": ",".join(["PLAINTEXT://localhost:9092", "PLAINTEXT://localhost:9093", "PLAINTEXT://localhost:9094"]),
            "bootstrap.servers": ",".join(["PLAINTEXT://kafka0:19092","PLAINTEXT://kafka0:9092","PLAINTEXT://kafka1:9093","PLAINTEXT://kafka2:9094"]),
            #"schema.registry.url": "http://localhost:8081"
            "schema.registry.url": "http://schema-registry:8081"
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        # TODO: Configure the AvroProducer
        self.producer = AvroProducer(
            self.broker_properties,
            default_key_schema=key_schema,
            default_value_schema=value_schema
        )

    def check_topic_exists(self, client, topic_name):
        """Checks if the given topic exists"""
        # Request metadata from cluster with max response_time=5
        topic_metadata = client.list_topics(timeout=5)
        topics = topic_metadata.topics
        print(topics)
        return topic_name in topics

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        #
        #
        # TODO: Write code that creates the topic for this producer if it does not already exist on
        # the Kafka Broker.
        client = AdminClient(
            {"bootstrap.servers": self.broker_properties["bootstrap.servers"]}
        )
        #
        # before creating topic, check if the topic exists
        topic_exsists = self.check_topic_exists(client, self.topic_name)
        if (topic_exsists):
            logger.info("Topic %s already exists", self.topic_name)
            return

        logger.info("Creating topic %s with %s partitions and %s replicas",self.topic_name, self.num_partitions, self.num_replicas)

        futures = client.create_topics([
            NewTopic(self.topic_name, self.num_partitions, self.num_replicas)
        ])

        for topic,future in futures.items():
            try:
                future.result()
                logger.info("topic created")
            except Exception as e:
                print("failed to create topic {topic_name}: {e}")
                raise


        logger.info("topic creation kafka integration complete")

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        # TODO: Write cleanup code for the Producer here
        #
        #
        if self.producer is not None:
            self.producer.flush()
        logger.info("producer close complete")

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
