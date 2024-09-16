from typing import Dict
import pika
import json

class RabbitPublisher:
    def __init__(self, host: str = "localhost", port: int = 5672) -> None:
        self.__host = host
        self.__port = port
        self.__user = "guest"
        self.__pass = "guest"
        self.__exchange = "r_topic"
        self.__exchange_type = "topic"
        self.__routing_key = "cluster.sync"
        self.__start_server()
        
    def __start_server(self) -> None:
        self.__create_channel()
        self.__create_exchange()
        
    def __create_channel(self) -> None:
        credentials = pika.PlainCredentials(username = self.__user, password = self.__pass)
        parameters = pika.ConnectionParameters(host = self.__host, port = self.__port, credentials = credentials)
        self.__connection = pika.BlockingConnection(parameters)
        self.__channel = self.__connection.channel()
        
    def __create_exchange(self) -> None:
        self.__channel.exchange_declare(
            exchange = self.__exchange,
            exchange_type = self.__exchange_type 
        )
        
    def pub(self, message: Dict) -> None:
        msg = json.dumps(message)
        self.__channel.basic_publish(exchange = self.__exchange,
                                     routing_key = self.__routing_key,
                                     body = msg)