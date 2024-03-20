# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:19:33 2024

@author: User
"""


# librairie 
from bs4 import BeautifulSoup
import requests

#si réponse vaut 200 -> réussi
reponse = requests.get('https://www.francetvinfo.fr/societe/education/education-l-arrete-sur-les-groupes-au-college-en-maths-et-francais-au-journal-officiel_6430009.html')
reponse2 = requests.get('https://www.francetvinfo.fr/monde/europe/manifestations-en-ukraine/guerre-en-ukraine-pourquoi-emmanuel-macron-reitere-t-il-ses-propos-sur-le-possible-envoi-de-troupes-francaises-au-sol_6429946.html')
#parser indique le code a analyser ici html
soup = BeautifulSoup ( reponse2.content , "html.parser" )


#cherche dans le html la balise title
titre = soup.find_all("title")
print(titre[0].text)

print('\n')
#cherche dans le html les balises <p>
contenu=soup.find_all("p")
for paragraphe in contenu:
    print(paragraphe.text)
    
print('\n')
#cherche dans le html les balises <time>
dates = soup.find_all("time")
for date in dates:
    print(date.text)