from confluent_kafka import Consumer, KafkaException
from app.model import update_model_incremental
import json

def consume_feedback():
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'recommender-group',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = Consumer(conf)
    consumer.subscribe(['feedback-events'])
    
    print("Listening for feedback...")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            event = json.loads(msg.value().decode('utf-8'))
            user_id, item_id, rating = event["userId"], event["itemId"], event["rating"]
            update_model_incremental(user_id, item_id, rating)

    
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

