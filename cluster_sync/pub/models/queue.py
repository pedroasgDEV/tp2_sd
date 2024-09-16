from redis import Redis
from typing import Dict
import json

class RedisQueue:
    def __init__(self, redis_connection: Redis, queue_name: str = "msgs_queue") -> None:
        self.__queue_name = queue_name
        self.__redis_connection = redis_connection

    def push(self, value: Dict) -> None:
        json_value = json.dumps(value)
        self.__redis_connection.rpush(self.__queue_name, json_value)

    def pop(self) -> Dict:
        value = self.__redis_connection.lpop(self.__queue_name)
        if value: return json.loads(value)
        else: return {"state": "EMPTY"}