#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:43:53 2024

@author: philippebonnot
"""
from pylatex import Document, Section, Tabular

class documentLatex:
    

    def __init__(self, titre):
        
        self.titre = "Récapitulatif du jury : "+titre
        self.message=""
        self.geometry_options = {"head": "40pt","margin": "0.5in","bottom": "0.6in"}
        self.document = Document(titre,geometry_options=self.geometry_options)
        
        
    def compte_rendu_jury(self, tableau):
        longueurTableaux = len(tableau)+2#En plus des UES et du code nip on ajoute les nom et prénom
        for index,elem in enumerate(tableau[::-1]):
            comp = len(tableau)-1-index
            grp_nominal=""
            grp_verbal = "validé"
            grp_comp = "compétence"
            nbEtud=len(tableau[comp])
            if comp == 0:
                grp_comp = "aucune "+grp_comp
                if nbEtud == 0 or nbEtud == 1:
                    grp_verbal = "n'a "+grp_verbal
            elif comp == 1:
                grp_comp = "1 "+grp_comp
            else:
                grp_comp = str(comp)+" "+grp_comp+"s"
            if nbEtud == 0:
                grp_nominal = "Aucun étudiant n'"
                grp_verbal = "a validé"
            elif nbEtud == 1:
                grp_nominal = "1 étudiant"
                grp_verbal = "a validé"
            else:
                grp_nominal = str(nbEtud)+" étudiants"
                grp_verbal = "ont validé"
                if comp == 0:
                    grp_verbal = "n'"+grp_verbal
            self.message = grp_nominal+" "+grp_verbal+" "+grp_comp
            print()
            with self.document.create(Section(self.message)):
                with self.document.create(Tabular("|c" * longueurTableaux + "|")) as data_table:
                    data_table.add_hline()
                    data_table.add_row(["code_nip","nom","prénom","comp 1","comp 2","comp 3","comp 4","comp 5","comp 6"])
                    data_table.add_hline()
                    for etudiant in range(len(tableau[comp])):
                        data_table.add_row(tableau[comp][etudiant])
                        data_table.add_hline()
        self.document.generate_tex()
        self.document.generate_pdf("compte-rendu : "+self.titre,clean_tex=False)






