#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:43:02 2024

@author: bonnot
"""

import requests
import json
import requetes
from recap_jury_API import recap_jury_API
from documentLatex import documentLatex
from connexion_API import connexion_API


"""permet de retrouver la liste des ids de tous les semetres de l'année
à insérer en paramètre dans la requête concernant la décision de jury"""
"""def formsemestres_ids(data):
    ids=[]
    for i in range(len(data)):
        ids.append(data[i]["formsemestre_id"])
    return ids"""
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

"""On se connecte"""
"""config = configparser.ConfigParser()
print("lecture de la configuration")
config.read('config.ini')

print("Récupération du token auprès de {config['server']['Base_Url']}")
print(f"login : {config['credentials']['login']}")

response = requests.post(config['server']['Base_Url']+"api/tokens", auth = (config['credentials']['login'],config['credentials']['password']), verify = False)
                                                                                                                
token = response.json()['token']
print("token : ",token)
header = {"Authorization" : "Bearer " + token}"""

connexion = connexion_API()

annee=2022

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
            requete_etudiant = requetes.etudiantsInscritsDans(data_sem_pair_ids[i])
            response_etudiant = requests.get(connexion.get_config()['server']['Base_Url']+ requete_etudiant, headers = connexion.get_header(), verify = False)
           
            if not response_decision or not response_etudiant:
                print("Erreur : La chaîne JSON est vide.")
            else:
                try:
                    data_decision = json.loads(response_decision.content)
                    fichier_etudiants = json.loads(response_etudiant.content)
                    
                    for etudiant in fichier_etudiants:
                        code_nip = etudiant["code_nip"]
                        for etudiant_2 in data_decision:
                            if code_nip == etudiant_2["code_nip"]:
                                etudiant_2["nom"]=etudiant["nom"]
                                etudiant_2["prenom"]=etudiant["prenom"]
                                etudiant_2["civilite"]=etudiant["civilite"]
                                etudiant_2["bac"]=etudiant["admission"]["bac"]
                                etudiant_2["annee_du_bac"]=etudiant["admission"]["annee"]
                    recap_jury = recap_jury_API(annee,(i+1),data_decision,fichier_etudiants)
                    recap_jury.tableauValidationRCUEs()
                    print(recap_jury.tableau_stats())
                except json.JSONDecodeError as er:
                    print(f"Erreur de décodage JSON : {er}")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")


