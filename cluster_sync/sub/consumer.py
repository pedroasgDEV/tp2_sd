import pika
import json

class RabbitConsumer:
    def __init__(self, host: str = "localhost") -> None:
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host = host))
        self.__channel = self.__connection.channel()
        self.__exchange = "r_queue"
        self.__channel.exchange_declare(exchange = self.__exchange, exchange_type='fanout')

        queue = self.__channel.queue_declare(queue='', exclusive=True)
        self.__queue_name = queue.method.queue
        self.__channel.queue_bind(exchange = self.__exchange, queue = self.__queue_name)
        
    def sub(self, callback) -> None:

        self.__channel.basic_consume(queue = self.__queue_name, on_message_callback = callback, auto_ack = True)
        self.__channel.start_consuming()
        
        