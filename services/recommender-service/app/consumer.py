from confluent_kafka import Consumer, KafkaException
from app.model import update_model_incremental

def start_consumer(batch_size=100):
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'recommender-group',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = Consumer(conf)
    consumer.subscribe(['feedback-events'])
    
    buffer = []
    print("Listening for feedback...")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            user_id, item_id = msg.value().decode().split(',')
            buffer.append((int(user_id), int(item_id)))
            
            if len(buffer) >= batch_size:
                print(f"Processing {len(buffer)} feedback events...")
                update_model_incremental(buffer)
                buffer.clear()

    
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

