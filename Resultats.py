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
                    
        return self.data_decisions   
                
                
                
                
                