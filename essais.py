#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:56:41 2024

@author: philippebonnot
"""
from connexion_API import connexion_API
import requetes
import requests
import json

def formsemestres_ids(data):
    ids=[]
    for i,sem in data:
        ids.append(sem["formsemestre_id"])
    return ids

def id_semestre_pair(data):
    ids_sem_pair=[]
    for i in range(len(data)):
        
        if data[i]['session_id'].split('-')[3][1] in [str(2),str(4),str(6)]:
            ids_sem_pair.append(data[i])
    return ids_sem_pair

connexion = connexion_API()

annee = 2022
requete = requetes.formsemestresAnnee(annee)


response = requests.get(connexion.get_config()['server']['Base_Url']+ requete, headers = connexion.get_header(), verify = False)

if not response:
    print("Erreur : La chaîne JSON est vide.")
else:
    try:
        data = json.loads(response.content)
        data_sem_pair=id_semestre_pair(data)
        
        data_sem_pair_ids = []
        for i in range(len(data_sem_pair)):
            data_sem_pair_ids.append(data_sem_pair[i]['formsemestre_id'])
    
        nb_comptes_rendus = len(data_sem_pair_ids)
        print(nb_comptes_rendus)
        for i in range(nb_comptes_rendus):
            print("i : ",i)
            requete_decision = requetes.decisionJury(data_sem_pair_ids[i])
            response_decision = requests.get(connexion.get_config()['server']['Base_Url']+ requete_decision, headers = connexion.get_header(), verify = False)
            data_decisions = json.loads(response_decision.content)
            #requete_etudiant = requetes.etudiantsInscritsDans(data_sem_pair_ids[i])
            #response_etudiant = requests.get(connexion.get_config()['server']['Base_Url']+ requete_etudiant, headers = connexion.get_header(), verify = False)
            print(json.dumps(data_decisions,indent=4))
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")



