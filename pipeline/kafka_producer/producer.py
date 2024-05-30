import uuid
import time
import json
import psutil
import platform
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'localhost:9094'
}

producer = Producer(**conf)


# Callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Error message delivery: {err}")
    else:
        print(f"Message send: {msg.key()}")


def get_stats():
    memory_info = psutil.virtual_memory()
    json_data = {
        "ram": {
            "total": memory_info.total,
            "percent": memory_info.percent,
            "available": memory_info.available
        },
        "cpu": {
            "percent": psutil.cpu_percent(interval=1)
        },
        "platform": {
            "system": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    }

    return json_data


def send_messages():
    while True:
        message = get_stats()
        message_json = json.dumps(message)
        producer.produce('monitor_system', key=str(uuid.uuid4()), value=message_json, callback=delivery_report)

        producer.poll(0)
        time.sleep(1)


if __name__ == '__main__':
    try:
        send_messages()
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
