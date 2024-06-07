#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 09:52:29 2024

@author: bonnot
c'est un jury à l'année, il faut tenir compte de deux semestres
"""

import numpy as np
import json

class recap_jury_API:
    
    
    
    def __init__(self,annee,but,data,dict_etudiants):
        self.annee=annee
        self.but=but
        self.data = data
        self.dict_etudiants = dict_etudiants
        if but==3:
            self.nbUEs=3
        else:
            self.nbUEs=6
        self.tab_stats = np.zeros((3,4))
        self.longueurTab_stats = 4
        self.tabRCUEs = []
        
        
    def afficher_data(self):
        print(json.dumps(self.data,indent=4))
        
    def tableauValidationRCUEs(self):
        for i in range(self.nbUEs+1):
            self.tabRCUEs.append([])
            
        for etudiant in range(len(self.data)):
            resultEtudiant=[]
            code_etudiant=self.data[etudiant]['code_nip']
            print(code_etudiant)
            if code_etudiant in self.dict_etudiants:
                nom_etudiant = self.dict_etudiants[code_etudiant].split(';')[0]
                prenom_etudiant = self.dict_etudiants[code_etudiant].split(';')[1]
            resultEtudiant.append(self.data[etudiant]['code_nip'])
            resultEtudiant.append(nom_etudiant)
            resultEtudiant.append(prenom_etudiant)
            nbRcues = 0
            for j in range(self.nbUEs):
                if self.data[etudiant]['rcues'][j]['moy'] >= 10:
                    nbRcues = nbRcues + 1
                resultEtudiant.append(round(self.data[etudiant]['rcues'][j]['moy'],2))
            #resultEtudiant.append(nbRcues)
            self.tabRCUEs[nbRcues].append(resultEtudiant)
        return self.tabRCUEs   
