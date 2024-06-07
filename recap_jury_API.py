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
    
    
    
    def __init__(self,annee,but,data,fichier_etudiants):
        self.annee=annee
        self.but=but
        self.data = data
        self.fichier_etudiants = fichier_etudiants
        self.dict_etudiants_code_nip_nom ={}
        for etudiant in self.fichier_etudiants:
            self.dict_etudiants_code_nip_nom[etudiant['code_nip']]=etudiant['sort_key']   
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
            if code_etudiant in self.dict_etudiants_code_nip_nom:
                nom_etudiant = self.dict_etudiants_code_nip_nom[code_etudiant].split(';')[0]
                prenom_etudiant = self.dict_etudiants_code_nip_nom[code_etudiant].split(';')[1]
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

    def repartition_homme_femme(self):
        dict={"M":[],"F":[]}
        for etudiant in self.fichier_etudiants:
            if etudiant['civilite'] == 'M':
                dict['M'].append(etudiant['nom'])
            else:
                dict['F'].append(etudiant['nom'])
        return dict
    
    def repartition_bacs(self):
        dict = {"gene":[],"Techno":[],"Autre":[]}
        for etudiant in self.fichier_etudiants:
            if etudiant["admission"]["bac"] in ["S","Général", "Géné(RéoL1,L2)","L","G\u00c9N\u00c9","GENE(REOR L1)"]:
                dict["gene"].append(etudiant['nom'])
            elif etudiant["admission"]["bac"] == "STMG" or etudiant["admission"]["bac"] == "STI2D":
                dict['Techno'].append(etudiant['nom'])
            else:
                dict['Autre'].append(etudiant['nom'])
        return dict
            
    
  