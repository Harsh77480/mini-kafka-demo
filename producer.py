#python -m venv venv
#venv\Scripts\activate
#pip install confluent-kafka

import json
import uuid
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092', "linger.ms": 5}) 
 # linger.ms : 5  means "Wait up to 5 milliseconds before actually sending the message over the network.". It acts like a bus waiting at a stop. Instead of sending 10 separate network requests for 10 wallet transactions that happened almost instantly, the producer waits 5 milliseconds, groups all 10 transactions into a single "batch", and sends them in one go.

# event to be sent to kafka topic 'orders'
order = {  
    'order_id': str(uuid.uuid4()),
    'user': 'Ravi',
    'item' : 'Chicken Burger',
    'quantity': 2
}


# we have to convert the order dictionary to bit string before sending
value = json.dumps(order).encode('utf-8')


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()}, partition : {msg.partition()}, value : {msg.value().decode("utf-8")}, offset : {msg.offset()}')
        
# producer is connected to kafka broker and sending the event to topic 'orders'
# if the topic does not exist, kafka will create it automatically
producer.produce(topic='orders', value=value, callback=delivery_report)

producer.flush()  
#When you write producer.produce(topic, message) in your code, the message does not instantly go over the network. Instead, it is placed into a local memory buffer inside your Python application, and a background thread takes care of actually sending it to Kafka (respecting that linger.ms wait time).
#This makes your application super fast because it doesn't have to pause and wait for the network every time it generates a transaction. But it introduces a risk: What if your application shuts down while messages are still sitting in that local memory buffer? They would be deleted and lost forever.
#This is where producer.flush() comes in:
#It acts as a roadblock: When you call producer.flush(), it blocks your current Python thread.
#It empties the buffer: It forces the producer to instantly send any messages currently sitting in the local memory buffer to Kafka.
#It waits for confirmation: It will pause your code until Kafka Broker replies with the acks (that broker has saved the messages) for all those remaining messages. 
#On receieving acks(acknoledgement) only callback is called 
