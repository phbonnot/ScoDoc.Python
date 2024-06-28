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
        self.data_decisions = data
        self.fichier_etudiants = fichier_etudiants#la liste des étudiants inscrits dans l'année
        #self.renseignements_etudiants = renseignements_etudiants#code_nip, nom,prénom,sexe,type_bac et année du bac
        self.dict_etudiants_code_nip_nom ={}
        for etudiant in self.fichier_etudiants:
            self.dict_etudiants_code_nip_nom[etudiant['code_nip']]=etudiant['sort_key']   
        if but==3:
            self.nbUEs=3
        else:
            self.nbUEs=6
        self.tab_stats = np.zeros((5,7))
        self.longueurTab_stats = 5
        self.types_de_bac_gene = ["S","Général","Géné(RéoL1,L2)","G\u00c9N\u00c9","GENE(REOR L1)"]
        self.dict_types_de_bac = {"géné":[],"techno":[],"autre":[]}
        self.tab_admis=[]
        
        
    def afficher_data(self):
        print(json.dumps(self.data,indent=4))
        
    def tableauValidationRCUEs(self):
        tabRCUEs = []
        for i in range(self.nbUEs+1):
            tabRCUEs.append([])
            
        for ind_etudiant,etudiant in enumerate(self.data_decisions):
            resultEtudiant=[]
            code_etudiant=self.data_decisions[ind_etudiant]['code_nip']
            if code_etudiant in self.dict_etudiants_code_nip_nom:
                nom_etudiant = self.dict_etudiants_code_nip_nom[code_etudiant].split(';')[0]
                prenom_etudiant = self.dict_etudiants_code_nip_nom[code_etudiant].split(';')[1]
                resultEtudiant.append(self.data_decisions[ind_etudiant]['code_nip'])
                resultEtudiant.append(nom_etudiant)
                resultEtudiant.append(prenom_etudiant)
                nbRcues = 0
                nbRcues_entre_huit_et_dix =0
                for j in range(self.nbUEs):#on parcourt toutes les ues
                    if self.data_decisions[ind_etudiant]['rcues'][j]['moy'] >= 10:
                        nbRcues = nbRcues + 1
                    elif self.data_decisions[ind_etudiant]['rcues'][j]['moy'] >= 8:
                        nbRcues_entre_huit_et_dix = nbRcues_entre_huit_et_dix +1
                    resultEtudiant.append(round(self.data_decisions[ind_etudiant]['rcues'][j]['moy'],2))
                tabRCUEs[nbRcues].append(resultEtudiant)
                if (nbRcues + nbRcues_entre_huit_et_dix) == self.nbUEs:
                    self.tab_admis.append(resultEtudiant)
                    etudiant["ADM"]=True
                else:
                    etudiant["ADM"]=False
        return tabRCUEs

    def repartition_homme_femme(self):
        dict={"M":[],"F":[]}
        for etudiant in self.fichier_etudiants:
            if etudiant['civilite'] == 'M':
                dict['M'].append(etudiant['nom'])
            else:
                dict['F'].append(etudiant['nom'])
        return dict
    
    def repartition_bacs(self):
        for etudiant in self.fichier_etudiants:
            if etudiant["admission"]["bac"] in self.types_de_bac_gene:
                self.dict_types_de_bac["géné"].append(etudiant['nom']+","+etudiant['prenom'])
            elif etudiant["admission"]["bac"] == "STMG" or etudiant["admission"]["bac"] == "STI2D":
                self.dict_types_de_bac['techno'].append(etudiant['nom']+","+etudiant['prenom'])
            else:
                self.dict_types_de_bac['autre'].append(etudiant['nom']+","+etudiant['prenom'])
        return self.dict_types_de_bac
            
    
    def repartition_neo_reor(self):
        dict={"neo":[],"reor":[]}
        for etudiant in self.renseignements_etudiants:
            if etudiant in self.fichier_etudiants and etudiant["annee_du_bac"]==self.annee:
                dict["neo"].append(etudiant)
            else:
                dict["reor"].append(etudiant)
        return dict
            
    def get_admis(self):
        return self.tab_admis
    
    def tableau_stats(self):
        ligne = 0
        colonne = 0
        adm = 0
        for etudiant in self.data_decisions:
            if etudiant["annee_du_bac"] == self.annee:
                if etudiant["bac"] == "géné":
                    ligne = 1
                elif etudiant["bac"] == "techno":
                    ligne = 2
                else:
                    ligne = 3
            else:
                ligne = 4
            if etudiant["civilite"] == "M":
                colonne = 3
                if etudiant["ADM"]:
                    adm = 4      
            else:
                colonne = 1
                if etudiant["ADM"]:
                    adm = 2 
            self.tab_stats[ligne][colonne] +=1
            self.tab_stats[ligne][adm] +=1
            
                
        return self.tab_stats
                
                
        
  