from flask import Flask, request, jsonify
import logging
import threading

from config import cluster_config
from models import queue, connection 
from listener import Listener

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True

redis_connection = connection.RedisConnection(cluster_config["REDIS_HOST"], cluster_config["REDIS_PORT"], cluster_config["REDIS_DB"])
redis_queue_pub = queue.RedisQueue(redis_connection.connect(), cluster_config["REDIS_QUEUE_PUB"])

listener = Listener()
listener_thread = threading.Thread(target = listener.listen)
listener_thread.start()

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
    app.run(host = cluster_config["CLUSTER_HOST"], port = cluster_config["CLUSTER_PORT"], debug = True)
