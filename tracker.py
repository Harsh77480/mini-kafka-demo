from confluent_kafka import Consumer
import json

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-tracker-group',
    # if there 3 instances of tracker, they all have same group id
    'auto.offset.reset': 'earliest'
    # if it don't know where we left off, start reading messages from the beginning of the topic    
}


consumer = Consumer(consumer_config)

consumer.subscribe(['orders']) 
# subscribing to topic 'orders', can subscribe to multiple topics by passing a list of topics

print("🟢Consumer is listening to topic 'orders'...")

try : # this try block is optional, just to handle keyboard interrupt gracefully
    while True:
        msg = consumer.poll(1.0)  
        # wait 1 second for a message in broker, if data exists, fetch it instantly
        # polling allows consumer controll speed of reading messages from broker

        if msg is None:
            continue
        if msg.error(): 
            print(f"Consumer error: {msg.error()}")
            continue

        order = json.loads(msg.value().decode('utf-8'))
        print(f"Received order: {order}")
except KeyboardInterrupt:
    print("🛑 Consumer is shutting down gracefully...")

finally:
    # just like producer.flush()
    consumer.close()
    # close the consumer to commit final offsets and leave the group cleanly
    # crucial for properly releasing resources and ensuring no messages are lost or duplicated
    print("✅ Consumer has been closed.")


