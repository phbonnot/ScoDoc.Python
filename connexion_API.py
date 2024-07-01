

import configparser
import requests
import json

class connexion_API:
    
    def __init__(self):
        
        self.config = configparser.ConfigParser()
        print("Lecture de la configuration")
        self.config.read('config.ini')
        
    
        response = requests.post(self.config['server']['Base_Url'] + "api/tokens", auth = (self.config['credentials']['login'],self.config['credentials']['password']), verify = False)
        
        # print(response)
        self.token = response.json()['token']
        # print(response.content)
        self.header = {"Authorization": "Bearer " + self.token}
        # print(header)
        response = requests.get(self.config['server']['Base_Url'] + "Informatique/api/etudiants/courants", headers = self.header, verify = False)
       
    def get_config(self):
        return self.config
    
    def get_token(self):
        return self.token
    
    def get_header(self):
        return self.header
    
