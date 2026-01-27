# mini-kafka-example
Implemented simple producer/consumer code to understand kafka.
[Tutorial](https://www.youtube.com/watch?v=B7CwU_tNYIE)


## Learnings : 

### Pull model :
- Unlike rabbitmq, where producer controls the speed of sending messages to broker,
- In kafka, consumer controls the speed of reading messages from broker so consumer pulls when ready.  

### Partition : 
- Each topic can have multiple partitions. Each partition is independent log.
- Order is guaranteed only within a partition, not across partitions.
- A partition is consumed by only one consumer within a consumer group at a time.
- A consumer can consume multiple partitions.
- Suppose message A is produced by topic T and A goes to partition P1
- Partition P1 is assigned to consumer C1 in consumer group G1
- Then only C1 will read message A, no other consumer in G1 will read message A

### Offset : 
- A unique, "sequential" id assigned to each message within a partition.
- With `poll()`, consumer fetches messages starting from the last committed offset.
- consumer.commit() means I have successfully processed messages up to this offset.
- If consumer crashes and restarts, it will resume from the last committed offset. These are storeed in kafka itself, accesseed by __consumer_offsets 

### Poll :
- `poll()` is also used to give 'heartbeat' to the broker, if it is not called, by a consumer, the broker thinks it is dead and removes it from the group. And rebalances the partitions among the remaining consumers in the group.
- `max.poll.interval.ms` : the maximum delay between invocations of `poll()` before the consumer is considered failed.

### Usefull commands :
- `kafka-console-consumer` is the "executable" script (.sh) located inside the Kafka container (by default). It acts as consumer temporarily to fetch the messages. Similary we have `kafka-topics.sh` and `kafka-console-producer.sh`.
- see the list of topics in docker,   
`docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list`
- see the details of topic 'orders' in docker,                                                                  
`docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning`
- create a topic,
`docker exec -it kafka kafka-topics --bootstrap-server kafka:9092   --create   --topic wallet.events   --partitions 1  --replication-factor 1` 
- see the metadata of topic 'orders' in docker,                                                 
`docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic orders`

