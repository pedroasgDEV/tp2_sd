from os import environ as env

cluster_config = {
    "REDIS_HOST": env["REDIS"],
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "REDIS_QUEUE_PUB": "msgs_queue_pub",
    "REDIS_QUEUE_SUB": "msgs_queue_sub",
    "CLUSTER_ID": env["CLUSTER_ID"],
    "CLUSTER_HOST": "0.0.0.0",
    "CLUSTER_PORT": 5000
}