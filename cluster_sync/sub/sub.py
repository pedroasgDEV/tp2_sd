import json

from config import sub_config
from models import queue, connection 
from consumer import RabbitConsumer

def callback(ch, method, properties, body):
    redis_queue.push(json.loads(body))

if __name__ == '__main__':
    redis_connection = connection.RedisConnection(sub_config["REDIS_HOST"], sub_config["REDIS_PORT"], sub_config["REDIS_DB"])
    redis_queue = queue.RedisQueue(redis_connection.connect(), sub_config["REDIS_QUEUE"])

    rabbit = RabbitConsumer(sub_config["RABBIT_HOST"])
    
    rabbit.sub(callback)