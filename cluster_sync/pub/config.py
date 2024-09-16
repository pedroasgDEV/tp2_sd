from os import environ as env

pub_config = {
    "REDIS_HOST": env["REDIS"],
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "REDIS_QUEUE": "msgs_queue_pub",
    "RABBIT_HOST": env["RABBIT"],
    "RABBIT_PORT": 5672,
}