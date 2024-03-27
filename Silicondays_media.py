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

Liste_noire = ["infowars.com", "theonion.com", "naturalnews.com",
               "beforeitsnews.com","lesmoutonsrebelles.com","thedailybuzz.com",
               "prntly.com","yournewswire.com","sante-nutrition.org","fawkes-news.com",
               "lesmoutonsenrages.fr","wikistrike.com","les-crises.fr","egaliteetreconciliation.fr",
               "nouvelordremondial.cc","agoravox.fr","legrandsoir.info","panamza.com",
               "boulevardvoltaire.fr","dreuz.info","contrepoints.org","observateurcontinental.fr",
               "reinformation.tv","voltairenet.org",]
#On récupère l'URL
def nom_domaine(url):
    """Fonction intermédiaire qui récupère le nom du domaine"""
    parsed_url = urlparse(url)
    domaine = parsed_url.netloc
    if domaine.startswith('www.'):
        domaine = domaine[4:]  
    return domaine

def test_lb(domaine):
    """Fonction qui test si l'url est présent dans la liste_blanche"""
    if domaine in Liste_blanche:
        return True
    else :
        return False
        
def test_ln(domaine):
    """Fonction qui test si l'url est présent dans la liste_noire"""
    if domaine in Liste_noire:
        return True
    else :
        return False
# Cas si site non présent dans la liste blanche

def rank(url):
    """Fonction qui test donne le rang du domaine si il n'est pas dans une liste"""
    # URL de l'outil de vérification des backlinks
    checker_url = "https://ahrefs.com/fr/backlink-checker?url=" + url
    response = requests.get(checker_url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver l'élément contenant le rang du backlink
        rank_element = soup.find('span', attrs = {'class': "css-1hpl2vh.css-pelz90.css-0.css-gylvem-textDisplay.css-1x5n6ob"})
        
        # Vérifier si l'élément du rang existe
        if rank_element:
            rank = rank_element.text.strip()
            return rank
        else:
            return "Le rang du backlink n'a pas pu être trouvé."
    else:
        return "Impossible de se connecter."

print(rank("https://www.lemonde.fr/"))
def test_media(url):
    source = nom_domaine(url)
    if test_lb(source) == True :
        return "source vérifiée, score :100%"
    elif test_ln(source) == True :
        return "fake news, score : 0%"
    else :
        return rank(source)

print(test_media("https://www.lemonde.fr/"))
     
    