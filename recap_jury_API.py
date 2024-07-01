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
        self.ues_suivies_parcours=[[1,2,6],[4,5,6]]

        for etudiant in self.fichier_etudiants:
            self.dict_etudiants_code_nip_nom[etudiant['code_nip']]=etudiant['sort_key']   
        """if but==3:
            self.nbUEs=3
        else:
            self.nbUEs=6"""
        self.nbUEs = 6
        self.tab_stats = np.zeros((5,7))
        self.longueurTab_stats = 5
        self.types_de_bac_gene = ["S","Général","Géné(RéoL1,L2)","G\u00c9N\u00c9","GENE(REOR L1)"]
        self.dict_types_de_bac = {"géné":[],"techno":[],"autre":[]}
        self.tab_admis=[]
       
        
        
    def index_de(self,n,tab):
        for i,x in enumerate(tab):
            if x==n:
                return i
            
    def afficher_data(self):
        print(json.dumps(self.data,indent=4))
        
    def tableauValidationRCUEs(self):
        tabRCUEs = []
        for i in range(self.nbUEs+1):
            tabRCUEs.append([])
            
        for ind_etudiant,etudiant in enumerate(self.data_decisions):
            resultEtudiant=[]
            if self.but in [1,2]:
                ues_suivies = [1,2,3,4,5,6]
            else:
                if "parcours" in etudiant.keys():
                    if etudiant["parcours"]=="A":
                        ues_suivies = self.ues_suivies_parcours[0]
                    elif etudiant['parcours']=="C":
                        ues_suivies = self.ues_suivies_parcours[1]
                    else:
                        ues_suivies = [1,2,3,4,5,6]
                else:
                    ues_suivies = [1,2,3,4,5,6]
            
            code_etudiant=self.data_decisions[ind_etudiant]['code_nip']
            if code_etudiant in self.dict_etudiants_code_nip_nom:
                nom_etudiant = self.dict_etudiants_code_nip_nom[code_etudiant].split(';')[0]
                prenom_etudiant = self.dict_etudiants_code_nip_nom[code_etudiant].split(';')[1]
                resultEtudiant.append(self.data_decisions[ind_etudiant]['code_nip'])
                resultEtudiant.append(nom_etudiant)
                resultEtudiant.append(prenom_etudiant)
                nbRcues = 0
                nbRcues_entre_huit_et_dix =0
                for index in range(self.nbUEs):
                    j=index+1
                    if j in ues_suivies:
                        moyenne = self.data_decisions[ind_etudiant]['rcues'][self.index_de(j,ues_suivies)]['moy']
                        if moyenne >= 10:
                            nbRcues = nbRcues + 1
                        elif moyenne >= 8:
                            nbRcues_entre_huit_et_dix = nbRcues_entre_huit_et_dix +1
                        resultEtudiant.append(round(moyenne,2))
                    else:
                        resultEtudiant.append("-")
                    
                tabRCUEs[nbRcues].append(resultEtudiant)
                if (nbRcues + nbRcues_entre_huit_et_dix) == len(ues_suivies):
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
                
                
        
  