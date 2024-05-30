import json
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9094',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Crear una instancia del consumidor
consumer = Consumer(**conf)

# Suscribirse al topic
consumer.subscribe(['monitor_system'])

# MONGO Confs
mongo_client = MongoClient('localhost', 27017, username='admin', password='admin_password')
db = mongo_client['local_system_monitor']
collection = db['monitor_data']


try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        msg_value_str = msg.value().decode('utf-8')
        msg_value_dict = json.loads(msg_value_str)
        collection.insert_one(msg_value_dict)

        print(msg_value_str)

finally:
    consumer.close()
