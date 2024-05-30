from confluent_kafka import Consumer, KafkaError
import json

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

        register_id = json.loads(msg.value().decode('utf-8'))
        msg = msg.value().decode('utf-8')
        print(msg)

finally:
    consumer.close()
