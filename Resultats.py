#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:04:47 2024

@author: philippebonnot
"""
import requests
import requetes 
import json

class Resultats:
    
    def __init__(self,annee,compte_rendu,data_decisions,fichier_etudiants):
        self.annee = annee
        self.compte_rendu = compte_rendu
        if compte_rendu ==3:
            self.nbUEs=3
        else:
            self.nbUEs=6
        self.data_decisions = data_decisions
        self.fichier_etudiants = fichier_etudiants
        self.ids_semestres_pairs = []
        self.ids_semestres_impairs = []
        
        
    def id_semestre_pair(self,data):
        for sem in data:
            if sem['annee_scolaire'] == self.annee and sem['session_id'].split('-')[3][1] in [str(2),str(4),str(6)]:
                self.ids_semestres_pairs.append(sem['formsemestre_id'])
                #print(sem['formsemestre_id'])
        

    def id_semestre_impair(self,data):
        for sem in data:
            if sem['annee_scolaire'] == self.annee and sem['session_id'].split('-')[3][1] in [str(1),str(3),str(5)]:
                self.ids_semestres_impairs.append(sem['formsemestre_id'])
        

    
    def resultats(self):
        infos=[]
        for etudiant in self.data_decisions:
    
            infos_etudiant = []
            infos_etudiant.append(etudiant['code_nip'])
            infos_etudiant.append(etudiant['nom'])
            infos_etudiant.append(etudiant['prenom'])
            infos_etudiant.append(etudiant['bac'])
            infos_etudiant.append(etudiant['parcours'])
            for i in range(len(etudiant['rcues'])):
                ue_1=etudiant['rcues'][i]['ue_1']['moy']
                ue_2=etudiant['rcues'][i]['ue_2']['moy']
                if ue_1 is None or ue_2 is None:
                    infos_etudiant.append(ue_1)
                    infos_etudiant.append(ue_2)
                else:
                    infos_etudiant.append(round(etudiant['rcues'][i]['ue_1']['moy'],2))
                    infos_etudiant.append(round(etudiant['rcues'][i]['ue_2']['moy'],2))
                infos_etudiant.append(etudiant['rcues'][i]['code'])
            infos.append(infos_etudiant)    
        return infos
                
                
                
                
                