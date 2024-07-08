#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 08:41:12 2024

@author: philippebonnot
"""
import configparser
import requests

class connexion_API:
    
    
    def __init__(self):
        """On se connecte"""
        self.config = configparser.ConfigParser()
        print("lecture de la configuration")
        self.config.read('config.ini')

        print("Récupération du token auprès de {config['server']['Base_Url']}")
        print(f"login : {self.config['credentials']['login']}")

        self.reponse = requests.post(self.config['server']['Base_Url']+"api/tokens", auth = (self.config['credentials']['login'],self.config['credentials']['password']), verify = False)
                                                                                                                        
        self.token = self.reponse.json()['token']
        print("token : ",self.token)
        self.header = {"Authorization" : "Bearer " + self.token}
    
    def get_token(self):
        return self.token
    
    def get_reponse(self):
        return self.reponse
    
    def get_header(self):
        return self.header
    
    def get_config(self):
        return self.config
    
    