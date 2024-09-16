from redis import Redis

class RedisConnection:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.__host = host
        self.__port = port
        self.__db = db
        self.__connection = None

    def connect(self) -> Redis:
        self.__connection = Redis(
            host=self.__host,
            port=self.__port,
            db=self.__db
        )
        return self.__connection

    def get_conn(self) -> Redis:
        return self.__connection