# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:19:33 2024

@author: Etienne de Beaucorps
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def nb_recherche(query:str)->int:
    """
    renvoie le nombre de recherche environ donné par google de la recherche
    prend par exemple   "info choc en Russie !"
    
    """

    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={query}")
    driver.implicitly_wait(10)

    # Trouver l'élément contenant le nombre de résultats
    result_count_element = driver.find_element(By.CSS_SELECTOR, "div#result-stats")

    # Extraire le nombre de résultats
    result_count_text = result_count_element.text.strip()
    

    
    #récupération de la valeur du nombre de recherche entre " " sous forme de int 
    nombre=''
    compteur_de_r=0
    for k in result_count_text:
        
        if k=='r' and compteur_de_r==0:
            compteur_de_r+=1
        elif k=='r' and compteur_de_r==1:
            break
        elif k in ['1','2','3','4','5','6','7','8','9','0']:
            nombre+=k
            
    
    driver.quit()

    return (int(nombre))


def essai_manuel_nb_recherche()->str:
    
    url = input("Entrez votre requête de recherche : ")
    nombre_recherche = nb_recherche(url)
    return(f"Nombre de résultats pour '{url}' : {nombre_recherche}")




url_1 = 'https://www.lemonde.fr/international/article/2024/03/26/attentat-du-crocus-city-hall-apres-avoir-accuse-kiev-moscou-designe-les-occidentaux_6224318_3210.html'
url_2 = 'https://www.francetvinfo.fr/monde/europe/manifestations-en-ukraine/guerre-en-ukraine-pourquoi-emmanuel-macron-reitere-t-il-ses-propos-sur-le-possible-envoi-de-troupes-francaises-au-sol_6429946.html'
url_3= 'https://www.tf1info.fr/sciences-et-innovation/jusqu-a-25-fois-plus-polluante-pourquoi-la-viande-de-synthese-n-est-finalement-pas-si-ecolo-2257168.html'

def extraction_donnee(url:str,affichage=True)->list:
    ''' 
    extrait les données de l'url données et renvoie une 
    liste correspondant au format 
    
    [title,text,url,date,nb_recherche]
    si une valeur n'est pas dispo -> valeur null
    affichage par principe montré si True
    '''
    
    reponse = requests.get(url)
    soup = BeautifulSoup ( reponse.content , "html.parser" )
    
    
    #cherche dans le html la balise <title>
    titre = soup.find_all("title")
    
    #cherche dans le html les balises <p>
    paragraphe=soup.find_all("p")
    contenu=''
    if paragraphe:
        for p in paragraphe:
            contenu+=p.text
    else: contenu=None
    
    
    #cherche dans le html les balises <time>
    dates = soup.find_all("time")
    date=''
    if dates: date=dates[-1].text
    else: date = None


    nombre_recherche  = nb_recherche('"'+titre[0].text+'"')
    
    donnee = [titre[0].text,contenu,url,date,nombre_recherche]
    
    
    if affichage:
        print(titre[0].text)
        
        print('\n')
        for p in paragraphe:
            print(p.text)
            
        print('\n')

        for date in dates:
            print(date.text)
        
        print('\n\n\n la recherche est : ','"'+titre[0].text+'"','\n\n')
        print('\nnb_recherche : ',nombre_recherche)
        
    
    return donnee

def traitement_donnee(donnee:list)->(str,bool):
    ''' 
    
    Vérification implémentée : nombre de recherche
    
    à rajouter : 
        vérif sur la date ( probleme d'interprétation de la date entre 
         xx/xx/xxxx ou le 25 mai 2023 18h43 )
        
    '''
    if donnee[4]!=None:
        if donnee[4]<10:
            return ('trop peu cité',False)
    else:
        return ('Il manque le titre pour faire la recherche',False)
    
    return ('vérification passée',True)


def test():
    
    
    print(essai_manuel_nb_recherche())
        
    print(traitement_donnee(extraction_donnee(url_1,False)))
    print(traitement_donnee(extraction_donnee(url_2,False)))
    print(traitement_donnee(extraction_donnee(url_3,False)))
    
#cas de 3 url pour tester le programme
