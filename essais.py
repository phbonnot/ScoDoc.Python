#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:56:41 2024

@author: philippebonnot
"""
import configparser
import requests
import json
import requetes

"""On se connecte"""
config = configparser.ConfigParser()
print("lecture de la configuration")
config.read('config.ini')

print("Récupération du token auprès de {config['server']['Base_Url']}")
print(f"login : {config['credentials']['login']}")

response = requests.post(config['server']['Base_Url']+"api/tokens", auth = (config['credentials']['login'],config['credentials']['password']), verify = False)
                                                                                                                
token = response.json()['token']
print("token : ",token)
header = {"Authorization" : "Bearer " + token}

annee=2022

requete = requetes.etudiantsInscritsDans(21)

response = requests.get(config['server']['Base_Url']+ requete, headers = header, verify = False)

if not response:
    print("Erreur : La chaîne JSON est vide.")
else:
    try:
        data = json.loads(response.content)
        print(json.dumps(data,indent=4)) 
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")



