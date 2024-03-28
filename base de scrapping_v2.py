# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:19:33 2024

@author: Etienne de Beaucorps - silicon days
"""





'''

rajout sur la version de claudiu du cas ou le titre n'est pas trouvé 
-> recherche de titre h1 ou juste None pour éviter les erreurs

'''
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import re

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




# 3 vraies infos de site 'reconnu'
url_1 = 'https://www.lemonde.fr/international/article/2024/03/26/attentat-du-crocus-city-hall-apres-avoir-accuse-kiev-moscou-designe-les-occidentaux_6224318_3210.html'
url_2 = 'https://www.francetvinfo.fr/monde/europe/manifestations-en-ukraine/guerre-en-ukraine-pourquoi-emmanuel-macron-reitere-t-il-ses-propos-sur-le-possible-envoi-de-troupes-francaises-au-sol_6429946.html'
url_3= 'https://www.tf1info.fr/sciences-et-innovation/jusqu-a-25-fois-plus-polluante-pourquoi-la-viande-de-synthese-n-est-finalement-pas-si-ecolo-2257168.html'

# news d'un site pas trop connu mais qui met son nom dans le titre faussant le résultat du nb de recherche
url_4 = 'https://www.slate.fr/story/255885/adobe-vend-images-guerre-israel-hamas-ia-intelligence-artificielle'

#url d'une fake news avec un mauvais score backlink
url_5 = 'https://alloforfait.fr/mobile/apps/news/97090-meta-facebook-interdit-finalement-appels-mort-poutine.html'

# site de fake news mais qui est très connu pour être fake
url_6 = 'https://www.legorafi.fr/2024/03/22/mort-de-frederic-mitterrand-la-thailande-decrete-trois-jours-de-deuil-national/'

# test sur tweeter ne donne rien, le code html est fait pour que tu ne puisses pas trouver de manière générique les infos
# sur reddit on peut récupérer le contenu mais le titre sera reddit -> fausse les résultats de nb recherche et la date 



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
    
    #recherche de titre en balise <h1> ou None 
    if titre:
        non_titre=False
    else: 
        non_titre=True
        titre = soup.find_all("h1")
        if titre:
            non_titre=False
        
            
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
    if dates: 
        date = standardiser_date(dates[-1].text)
    else: date = None

    #cas d'un manque de titre ou non
    if non_titre==False:
        nombre_recherche  = nb_recherche('"'+titre[0].text+'"')
       
        donnee = [titre[0].text,contenu,url,date,nombre_recherche]
    
    else:
        donnee=[None,contenu,url,date,None]
        


    if affichage:
        if non_titre==False:
            print(titre[0].text)

        print('\n')
        for p in paragraphe:
            print(p.text)

        print('\n')

        for date in dates:
            print(date.text)

        if non_titre==False:
            print('\n\n\n la recherche est : ','"'+titre[0].text+'"','\n\n')
            print('\nnb_recherche : ',nombre_recherche)


    return donnee

def traitement_donnee(donnee:list)->(str,bool):
    '''

    Vérification implémentée : nombre de recherche
    + nombre de recherche
    '''
    today = datetime.now().date()
    if donnee[4]!=None:
        if donnee[4]<10:
            return ('trop peu cité',False)
    else:
        return ('Il manque le titre pour faire la recherche',False)

    if donnee[3]!=None:
        date_article = datetime.strptime(donnee[3], '%Y-%m-%d').date()
        if date_article >= datetime.now().date():
            return ('Article trop récent', False)
    return ('vérification passée',True)


def standardiser_date(date_string):
    '''
    Standardisation de la date
    '''

    date_string = re.sub(r'^.*le ', '', date_string)
    date_string = re.sub(r'^.*at ', '', date_string)
    date_string = re.sub(r'^.*publié ', '', date_string)
    date_string = re.sub(r'\s+à.*$', '', date_string)
    date_string = re.sub(r'\s+\d{2}:\d{2}$', '', date_string)

    # Traduire les mois en anglias pour pouvoir le filtrer avec datetime
    months_fr_to_en = {
        'Janvier': 'January',
        'janvier': 'January',
        'Jan': 'January',
        'jan': 'January',
        'février': 'February',
        'Février': 'February',
        'fév': 'February',
        'Fév.': 'February',
        'mars': 'March',
        'Mars': 'March',
        'Mar': 'March',
        'mar': 'March',
        'avril': 'April',
        'Avril': 'April',
        'avr': 'April',
        'Avr': 'April',
        'mai': 'May',
        'Mai': 'May',
        'juin': 'June',
        'Juin': 'June',
        'juillet': 'July',
        'Juillet': 'July',
        'Juil': 'July',
        'juil': 'July',
        'août': 'August',
        'Août': 'August',
        'aou': 'August',
        'Aou.': 'August',
        'septembre': 'September',
        'Septembre': 'September',
        'sep': 'September',
        'Sep.': 'September',
        'octobre': 'October',
        'Octobre': 'October',
        'oct': 'October',
        'Oct': 'October',
        'novembre': 'November',
        'Novembre': 'November',
        'nov': 'November',
        'Nov': 'November',
        'décembre': 'December',
        'Décembre': 'December',
        'déc': 'December',
        'Déc.': 'December'
    }



    for fr_month, en_month in months_fr_to_en.items():
        date_string = date_string.replace(fr_month, en_month)

    format_date = [
        "%d/%m/%Y",
        "%d %B %Y",
        "%d %B %Y à %Hh%M",
        "%Y-%m-%d"
    ]

    for fmt in format_date:
        try:
            return datetime.strptime(date_string, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None




def test():


    print(essai_manuel_nb_recherche())

    print(traitement_donnee(extraction_donnee(url_1,False)))
    print(traitement_donnee(extraction_donnee(url_2,False)))
    print(traitement_donnee(extraction_donnee(url_3,False)))
    print(traitement_donnee(extraction_donnee(url_4,False)))

    
#cas de 3 url pour tester le programme


def test_2():
    
    # print(extraction_donnee(url_1,False)[0],extraction_donnee(url_1,False)[3],extraction_donnee(url_1,False)[4])
    # print(extraction_donnee(url_2,False)[0],extraction_donnee(url_2,False)[3],extraction_donnee(url_2,False)[4])
    # print(extraction_donnee(url_3,False)[0],extraction_donnee(url_3,False)[3],extraction_donnee(url_3,False)[4])
    # print(extraction_donnee(url_4,False)[0],extraction_donnee(url_4,False)[3],extraction_donnee(url_4,False)[4])
    # print(extraction_donnee(url_5,False)[0],extraction_donnee(url_5,False)[3],extraction_donnee(url_5,False)[4])
    # print(extraction_donnee(url_6,False)[0],extraction_donnee(url_6,False)[3],extraction_donnee(url_6,False)[4])
    print('''\nAttentat du Crocus City Hall : après avoir accusé Kiev, Moscou désigne les Occidentaux None 239\n
    Guerre en Ukraine : pourquoi Emmanuel Macron réitère-t-il ses propos sur le possible envoi de troupes françaises au sol ? 2024-03-17 1500\n
    Jusqu'à 25 fois plus polluante : c'est quoi la "viande de synthèse", dans le viseur de la France ?  | TF1 INFO None 1880\n
    Adobe vend des images de la guerre Israël-Hamas générées par IA | Slate.fr 2023-11-06 1550\n
    Meta (Facebook) interdit finalement les appels à la mort de Poutine - alloforfait.fr None 1\n
    Mort de Frédéric Mitterrand - La Thaïlande décrète trois jours de deuil national None 8330''')
