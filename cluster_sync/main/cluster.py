from flask import Flask, request, jsonify
import time
import random
from typing import Dict
import logging
import threading

from config import cluster_config
from models import queue, connection 
from listener import Listener

app = Flask(__name__)

redis_connection = connection.RedisConnection(cluster_config["REDIS_HOST"], cluster_config["REDIS_PORT"], cluster_config["REDIS_DB"])
redis_queue_pub = queue.RedisQueue(redis_connection.connect(), cluster_config["REDIS_QUEUE_PUB"])
            

@app.route('/', methods=['POST'])
def process_json():
    data = request.get_json()
    
    message = {
        "cluster_id": cluster_config["CLUSTER_ID"],
        "message": data,
        "state": "ACQUIRE"
    }
    
    redis_queue_pub.push(message)
    
    response = {"state": "COMMITTED"}
    return jsonify(response)

if __name__ == '__main__':
    listener = Listener()
    listener_thread = threading.Thread(target = listener.listen())
    listener_thread.start()
    app.run(host = cluster_config["CLUSTER_HOST"], port = cluster_config["CLUSTER_PORT"], debug = True)
