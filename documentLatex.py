#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:43:53 2024

@author: philippebonnot
"""
from pylatex import Document, Section, Tabular, PageStyle, MiniPage, NoEscape, Head,StandAloneGraphic,LargeText


class documentLatex:
    

    def __init__(self, titre):
        
        self.titre = "Récapitulatif du jury : "+titre
        self.message=""
        self.geometry_options = {"head": "40pt","margin": "0.4in","bottom": "0.6in","includeheadfoot": True}
        self.document = Document(self.titre,geometry_options=self.geometry_options)
        self.tab_stats_lignes=["néo bac géné","néo bac techno","néo autre","étranger","réorientation"]
        self.document.add_color("bleu","RGB","84,201,227")
        self.document.add_color("vert","RGB","176,228,135")
        self.document.add_color("jaune","RGB","255,187,0")
        print("titre ",titre)
        if titre == "BUT 1":
            self.color = "jaune"
        elif titre == "BUT 2":
            self.color = "vert"
        else:
            self.color = "bleu"
        
    def generateHeader(self):
        header = PageStyle("header")
        with header.create(Head("L")) as header_left:
           with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c')) as logo_wrapper:
               logo_wrapper.append(StandAloneGraphic(image_options="width=80px", filename="Logo_iut.png"))
        with header.create(Head("C")) as header_center:
            with header_center.create(MiniPage(width=NoEscape(r"0.6\textwidth"), align='c')) as title_wrapper:
                title_wrapper.append(LargeText(self.titre))

        return header
            
            
    def compte_rendu_jury(self, tableau):
        self.document.preamble.append(self.generateHeader())
        self.document.change_document_style("header")
        
        longueurTableaux = len(tableau)+3#En plus des UES et du code nip on ajoute les nom et prénom et bac
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
            
            with self.document.create(Section(self.message, numbering = False)):
                with self.document.create(Tabular("|c|l|l|c|c|c|c|c|c|c|")) as data_table:
                    data_table.add_hline()
                    data_table.add_row(["code_nip","nom","prénom","bac","comp 1","comp 2","comp 3","comp 4","comp 5","comp 6"],color=self.color)
                    data_table.add_hline()
                    for etudiant in range(len(tableau[comp])):
                        data_table.add_row(tableau[comp][etudiant])
                        data_table.add_hline()
                        
        with self.document.create(Section("STATISTIQUES",numbering = False)):
            with self.document.create(Tabular("|p{1.5cm}"*8+"|")) as stats_table:
                stats_table.add_hline()
                stats_table.add_row(["","F","F/adm","G","G/adm","%F","%G","Total"])
                stats_table.add_hline()
                for rubrique in self.tab_stats_lignes:          
                    stats_table.add_row([rubrique,"","","","","","",""])
                    stats_table.add_hline()
                
        
        self.document.generate_tex()
        self.document.generate_pdf(self.titre,clean_tex=False)






