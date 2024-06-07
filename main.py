#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:43:02 2024

@author: bonnot
"""

import configparser
import requests
import json
import requetes
from recap_jury_API import recap_jury_API
from documentLatex import documentLatex

"""permet de retrouver la liste des ids de tous les semetres de l'année
à insérer en paramètre dans la requête concernant la décision de jury"""
def formsemestres_ids(data):
    ids=[]
    for i in range(len(data)):
        ids.append(data[i]["formsemestre_id"])
    return ids

def id_semestre_pair(data):
    ids_sem_pair=[]
    for i in range(len(data)):
        
        if data[i]['session_id'].split('-')[3][1] in [str(2),str(4),str(6)]:
            ids_sem_pair.append(data[i])
    return ids_sem_pair

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

requete = requetes.formsemestresAnnee(annee)

response = requests.get(config['server']['Base_Url']+ requete, headers = header, verify = False)
#data = json.loads(response.content)
#for i in range(len(data)):
#    print(data[i]['date_debut_iso']," ",data[i]['date_fin_iso']," ",data[i]['titre_num'],data[i]['formsemestre_id'])
#print(json.dumps(data,indent=4))

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
            requete2 = requetes.decisionJury(data_sem_pair_ids[i])
            response2 = requests.get(config['server']['Base_Url']+ requete2, headers = header, verify = False)
            requeteEtudiant = requetes.etudiantsInscritsDans(data_sem_pair_ids[i])
            response3 = requests.get(config['server']['Base_Url']+ requeteEtudiant, headers = header, verify = False)
            if not response2 or not response3:
                print("Erreur : La chaîne JSON est vide.")
            else:
                try:
                    data2 = json.loads(response2.content)
                    fichier_etudiants = json.loads(response3.content)
                    recap_jury = recap_jury_API(annee,(i+1),data2,fichier_etudiants)
                    #compteRendu = documentLatex("année 2022 BUT"+str(i+1))
                    #compteRendu.compte_rendu_jury(recap_jury.tableauValidationRCUEs())
                    print(json.dumps(recap_jury.repartition_bacs()))
                except json.JSONDecodeError as er:
                    print(f"Erreur de décodage JSON : {er}")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")


