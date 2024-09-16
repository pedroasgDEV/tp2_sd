import requests
import random
import time
from os import environ as env

class Client:
    def __init__(self):
        self.client_id = env["CLIENT_ID"]
        self.cluster_url = "http://" + env["CLUSTER_SYNC"] + ":5000/" #define o link da rede
        self.qnt_msgs = random.randint(10, 50)
        
    def start(self):
        for i in range(self.qnt_msgs):
            #hora de envio da mensagem
            timestamp = time.time()
            
            #Gera a mensagem a ser enviada
            message = {
                    "client_id" : self.client_id,
                    "timestamp" : timestamp,
                }
            
            #Envia a mensagem para ao cluster_sync
            response = requests.post(self.cluster_url, json = message)
            
            #verifica envio
            if response.status_code == 200:
                
                # Extrair o JSON da resposta
                response_json = response.json()
                
                if response_json.get("menssage") == "COMMITTED":
                     time.sleep(random.randint(1, 5))
                     
                else: 
                    raise Exception("Server not return a menssage")
                    
            else:
                raise Exception("Server not receive the menssage")
                       

if __name__ == "__main__":
    client = Client()
    client.start()
