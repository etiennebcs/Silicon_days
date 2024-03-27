# -*- coding: utf-8 -*-
"""

@author: erwan
"""
#Nous utilisons des bibliothèques pour simplifier le code
import requests
from bs4 import BeautifulSoup #Permettera d'insérer le lien sur le site
from urllib.parse import urlparse # Permettera de récupérer l'URL

Liste_blanche = ["lemonde.fr", "gouvernement.fr","lequipe.fr","lefigaro.fr",
                 "economie.gouv.fr","liberation.fr","francetvinfo.fr","nytimes.com",
                 "theguardian.com","bbc.com","washingtonpost.com"]
#On récupère l'URL
def nom_domaine(url):
    parsed_url = urlparse(url)
    domaine = parsed_url.netloc
    if domaine.startswith('www.'):
        domaine = domaine[4:]  
    return domaine

# Cas si site non présent dans la liste blanche

def rank(url):
    # URL de l'outil de vérification des backlinks
    checker_url = "https://ahrefs.com/fr/backlink-checker?url=" + url
    response = requests.get(checker_url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver l'élément contenant le rang du backlink
        rank_element = soup.find('span', attrs = {'class': "css-1hpl2vh css-pelz90 css-0 css-gylvem-textDisplay css-1x5n6ob"})
        
        # Vérifier si l'élément du rang existe
        if rank_element:
            rank = rank_element.text.strip()
            return rank
        else:
            return "Le rang du backlink n'a pas pu être trouvé."
    else:
        return "Impossible de se connecter."

print(rank("https://www.lemonde.fr/"))