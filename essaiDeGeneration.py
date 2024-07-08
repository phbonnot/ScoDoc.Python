#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 16:12:06 2024

@author: philippebonnot
"""
from pylatex import Document, PageStyle, Head, MiniPage, StandAloneGraphic, Package
from pylatex.utils import NoEscape

# Création du document
doc = Document()

# Création d'un nouveau style de page pour l'en-tête et le pied de page
header = PageStyle("header")

# Ajout de l'image dans l'en-tête à gauche
with header.create(Head("L")) as header_left:
    with header_left.create(MiniPage(width=NoEscape(r"0.2\textwidth"), align='l')) as logo_wrapper:
        logo_wrapper.append(StandAloneGraphic(image_options="width=80px", filename="Logo_iut.png"))

# Application du style de l'en-tête
doc.preamble.append(header)

# Définition du style de page par défaut
doc.change_document_style("header")

# Ajout de contenu au document pour la démonstration
doc.append("Ceci est un exemple de document avec une image dans l'en-tête.")

doc.add_color("monBleu","RGB","90,161,238")
doc.packages.add("color")
# Génération du PDF
doc.generate_pdf("document_avec_entete", clean_tex=False)
