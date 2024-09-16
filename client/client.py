import requests
import random
import time
from cofig import client_config
class Client:
    def __init__(self, client_id: int = 1, cluster_url: str = "localhost"):
        self.__client_id = client_id
        self.__cluster_url = "http://" + cluster_url + ":5000/" #define o link da rede
        self.__qnt_msgs = random.randint(10, 50)
        self.__start()
        
    def __start(self):
        for i in range(self.__qnt_msgs):
            timestamp = time.time()
            
            message = {
                    "client_id" : self.__client_id,
                    "timestamp" : timestamp,
                }
            
            response = requests.post(self.__cluster_url, json = message)
            
            if response.status_code == 200:
                
                response_json = response.json()

                if response_json.get("menssage") == "COMMITTED":
                     time.sleep(random.randint(1, 5))
                     
                else: 
                    raise Exception("Server not return a menssage")
                    
            else:
                raise Exception("Server not receive the menssage")
                       

if __name__ == "__main__":
    client = Client(client_config["CLIENT_ID"], client_config["CLUSTER_SYNC"])
