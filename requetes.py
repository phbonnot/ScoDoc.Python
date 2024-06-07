#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 17:36:07 2024

@author: bonnot
"""

#Infos administratives d'un étudiant dont le code_nip est donné en paramètre
def infosEtudiant(code_nip):
    return "Informatique/api/etudiant/nip/"+str(code_nip)

#identifiants des semestres suivis par un étudiant donné par le code_nip
def semestres_suivis_par(code_nip):
    return "Informatique/api/etudiant/nip/"+code_nip+"/formsemestres"

def semestresEnCours(annee):
    return "Informatique/api/formsemestres/query?annee_scolaire="+str(annee)

def infosEtudiantParNom(nom):
    return "Informatique/api/etudiants/name/"+nom

def decisionJury(formsemestre_id):
    return "Informatique/api/formsemestre/"+str(formsemestre_id)+"/decisions_jury"

def formsemestresAnnee(annee):
    return "Informatique/api/formsemestres/query?annee_scolaire="+str(annee)

"""Avec cette requête : print(data[i]['date_debut_iso']," ",data[i]['date_fin_iso']," ",data[i]['titre_num']," ",data[i]['formsemestre_id']," ",data[i]['session_id'])
renvoie 
2023-02-01   2023-07-15   BUT Informatique semestre 2   40   INFORMATIQUE-BUT-FI-S2-2022
2023-01-30   2023-08-31   BUT Informatique semestre 4   41   INFORMATIQUE-BUT-FI-S4-2022
2022-09-01   2023-01-31   BUT Informatique semestre 1   19   INFORMATIQUE-BUT-FI-S1-2022
2022-09-01   2023-01-28   BUT Informatique semestre 3   21   INFORMATIQUE-BUT-FI-S3-2022"""

def etudiantsCourants():
    return "Informatique/api/etudiants/courants/long"

def etudiantsInscritsDans(formsemestre_id):
    return "Informatique/api/formsemestre/"+str(formsemestre_id)+"/etudiants/long"