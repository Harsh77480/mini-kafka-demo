#python -m venv venv
#venv\Scripts\activate
#pip install confluent-kafka

import json
import uuid
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})

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
# wait for any outstanding messages to be delivered and delivery reports to be received
# ensures we dont have any messages that are not sent to kafka broker yet.
