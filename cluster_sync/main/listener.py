import time
import random

from config import cluster_config
from models import queue, connection 

class Listener:
    def __init__(self) -> None:
        redis_connection = connection.RedisConnection(cluster_config["REDIS_HOST"], cluster_config["REDIS_PORT"], cluster_config["REDIS_DB"])
        self.__redis_queue_pub = queue.RedisQueue(redis_connection.connect(), cluster_config["REDIS_QUEUE_PUB"])
        self.__redis_queue_sub = queue.RedisQueue(redis_connection.connect(), cluster_config["REDIS_QUEUE_SUB"])

        self.__msgs_stack = []
        
    def listen(self) -> None:
        while True:
            message = self.__redis_queue_sub.pop()
            
            #Check if the menssage is empty or if is from this cluster and is a release
            if not "EMPTY" in message.values() or not (msg["cluster_id"] == cluster_config["CLUSTER_ID"] and msg["state"] == "RELEASE"):
                self.__msgs_stack.insert(0, message)   
                self.__enter_critical()
                
    # Checks if this cluster can enter the critical section, based on message order        
    def __enter_critical(self) -> None:
        acquire_count = 0 #Init count
        
        for msg in self.__msgs_stack:
            
            if msg["state"] == "ACQUIRE":
                acquire_count += 1
                
                #Check if this cluster can enter the critical section
                if msg["cluster_id"] == cluster_config["CLUSTER_ID"] and acquire_count == 1:
                    
                    #This cluster enters the critical section
                    print("cluster_sync_" + str(cluster_config["CLUSTER_ID"]) + " entrou em seção critica", flush = True)
                    time.sleep(random.uniform(0.2, 1.0))
                    
                    #Notify others that this cluster have left the critical section
                    msg["state"] = "RELEASE"
                    self.__redis_queue_pub.push(msg)
                    
                    #Remove from the stack
                    self.__msgs_stack.remove(msg)
                    
                    break

            #If a RELEASE resolves a previous ACQUIRE
            elif msg["state"] == "RELEASE": 
                acquire_count -= 1