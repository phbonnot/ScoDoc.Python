#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:44:43 2024

@author: philippebonnot
"""
import csv
import json

class documentCsv:
    
    def __init__(self,titre):
        self.titre = titre
        
                
        
    def generer_csv(self,data):
        print(json.dumps(data,indent=4))
        
        with open(self.titre+'.csv', 'w', newline='') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=';',quotechar='"')
            for etudiant in data:
                ligne = etudiant['code_nip']+","+etudiant['nom']+","+etudiant['prenom']+","+\
                    etudiant['bac']
                for rcue in etudiant['rcues']:
                    for ue in rcue[0]:
                        print(ue['ue_1'])
                        
                        
                file_writer.writerow(ligne)
            #file_writer.writerow(['Spam'] * 5 + ['Baked Beans'])
            #file_writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])"""
            
        
    