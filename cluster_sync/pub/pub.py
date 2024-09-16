from config import pub_config
from models import queue, connection 
from publisher import RabbitPublisher

def read_queue():
     while True:
        message = redis_queue.pop()
        if not "EMPTY" in message.values():
            rabbit.pub(message)

if __name__ == '__main__':
    redis_connection = connection.RedisConnection(pub_config["REDIS_HOST"], pub_config["REDIS_PORT"], pub_config["REDIS_DB"])
    redis_queue = queue.RedisQueue(redis_connection.connect(), pub_config["REDIS_QUEUE"])

    rabbit = RabbitPublisher(pub_config["RABBIT_HOST"])
    
    read_queue()