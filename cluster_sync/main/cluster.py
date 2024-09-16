from flask import Flask, request, jsonify
import time
import random
from typing import Dict
import logging
import threading

from config import cluster_config
from models import queue, connection 

app = Flask(__name__)

redis_connection = connection.RedisConnection(cluster_config["REDIS_HOST"], cluster_config["REDIS_PORT"], cluster_config["REDIS_DB"])
redis_queue_pub = queue.RedisQueue(redis_connection.connect(), cluster_config["REDIS_QUEUE_PUB"])
redis_queue_sub = queue.RedisQueue(redis_connection.connect(), cluster_config["REDIS_QUEUE_SUB"])

log = logging.getLogger('werkzeug')
log.disabled = True

def listener() -> None:
    msgs_stack = []
    
    while True:
        message = redis_queue_sub.pop()
        
        if not "EMPTY" in message.values():
            msgs_stack.append(message)
                        
            msgs_stack = enter_critical(msgs_stack)
            
            
def  enter_critical(msgs_stack):
    # Verifica se o cluster pode entrar na seção crítica, baseado na ordem de mensagens
    acquire_count = 0
    
    for msg in msgs_stack:
        
        if msg["state"] == "ACQUIRE":
            acquire_count += 1
            
            # Pode entrar na seção crítica
            if msg["cluster_id"] == cluster_config["CLUSTER_ID"] and acquire_count == 1:
                
                #Entra em seção crítica
                print("cluster_sync" + cluster_config["CLUSTER_ID"] + " entrou em seção critica", flush = True)
                time.sleep(random.uniform(0.2, 1.0))
                
                #Notifica os outros que saiu da seção crítica
                msg["state"] = "RELEASE"
                redis_queue_pub.push(msg)
                
                #Modifica a pilha
                return [msgs for msgs in msgs_stack if msgs["cluster_id"] != cluster_config["CLUSTER_ID"]]

        # Um RELEASE resolve um ACQUIRE anterior
        elif msg["state"] == "RELEASE": 
            acquire_count -= 1
    
    return msgs_stack
            

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
    listener_thread = threading.Thread(target = listener)
    listener_thread.start()
    app.run(host = cluster_config["CLUSTER_HOST"], port = cluster_config["CLUSTER_PORT"], debug = True)
