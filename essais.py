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

requete = requetes.etudiantsCourants()

response = requests.get(config['server']['Base_Url']+ requete, headers = header, verify = False)

if not response:
    print("Erreur : La chaîne JSON est vide.")
else:
    try:
        data = json.loads(response.content)
        dict_etudiants_code_nip_nom ={}
        for etudiant in data:
            dict_etudiants_code_nip_nom[etudiant['code_nip']]=etudiant['sort_key']           
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")

for etudiant_key in dict_etudiants_code_nip_nom:
    print (dict_etudiants_code_nip_nom[etudiant_key].split(';')[0])