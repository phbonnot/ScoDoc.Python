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
    for sem in data:
        ids.append(sem["formsemestre_id"])
    return ids

def id_semestre_pair(data):
    ids_sem_pair=[]
    for sem in data:
        
        if sem['annee_scolaire']==annee and sem['session_id'].split('-')[3][1] in [str(2),str(4),str(6)]:
            ids_sem_pair.append(sem)
    return ids_sem_pair


connexion = connexion_API()

annee=2023



requete = requetes.formsemestresAnnee(annee)

response = requests.get(connexion.get_config()['server']['Base_Url']+ requete, headers = connexion.get_header(), verify = False)

if not response:
    print("Erreur : La chaîne JSON est vide.")
else:
    try:
        data = json.loads(response.content)
        
        data_sem_pair=id_semestre_pair(data)
        
        data_sem_pair_ids = []
        for sem_pair in data_sem_pair:
            data_sem_pair_ids.append(sem_pair['formsemestre_id'])
            print(sem_pair['formsemestre_id'])
            print(sem_pair['annee_scolaire'])
            print(sem_pair['session_id'])
        #nb_comptes_rendus = len(data_sem_pair_ids)
        #for i in range(nb_comptes_rendus):
            compte_rendu =int(int(sem_pair['session_id'].split('-')[3][1])/2)
            print("compte-rendu : ",compte_rendu)
            requete_decision = requetes.decisionJury(sem_pair['id'])
            response_decision = requests.get(connexion.get_config()['server']['Base_Url']+ requete_decision, headers = connexion.get_header(), verify = False)
            requete_etudiant = requetes.etudiantsInscritsDans(sem_pair['id'])
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
                                if len(etudiant['groups'])>0:
                                    parcours = etudiant['groups'][0]['group_name']
                                    etudiant_2["parcours"]=parcours
                    print(json.dumps(data_decision,indent=4))
                    recap_jury = recap_jury_API(annee,compte_rendu,data_decision,fichier_etudiants)
                    document = documentLatex("BUT "+str(compte_rendu))
                    document.compte_rendu_jury( recap_jury.tableauValidationRCUEs())
                    #print(recap_jury.tableau_stats())
                except json.JSONDecodeError as er:
                    print(f"Erreur de décodage JSON : {er}")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")


