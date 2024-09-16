from os import environ as env

sub_config = {
    "REDIS_HOST": env["REDIS"],
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "REDIS_QUEUE": "msgs_queue_sub",
    "RABBIT_HOST": "broker"
}