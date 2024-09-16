from typing import Dict
import pika
import json

class RabbitPublisher:
    def __init__(self, host: str = "localhost") -> None:
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host = host))
        self.__channel = self.__connection.channel()
        self.__exchange = "r_queue"
        self.__channel.exchange_declare(exchange = self.__exchange, exchange_type='fanout')
        
    def pub(self, message: Dict) -> None:
        msg = json.dumps(message)
        self.__channel.basic_publish(exchange = self.__exchange, routing_key = '', body = msg)