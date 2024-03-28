from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime



# For data
def extract_news_data(url: str, affichage=False) -> list:
    """
    extrait les données de l'url données et renvoie une
    liste correspondant au format

    [title,url,date]
    si une valeur n'est pas dispo -> valeur null
    affichage par principe montré si True
    """

    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, "html.parser")

    # cherche dans le html la balise <title>
    titre = soup.find_all("title")

    # cherche dans le html les balises <time>
    dates = soup.find_all("time")
    date = ''
    if dates:
        date = dates[-1].text
    else:
        date = None

    donnee = [titre[0].text, url, date]

    if affichage:
        print(titre[0].text)
        print('\n')

        for date in dates:
            print(date.text)

        print('\n\n\n la recherche est : ', '"' + titre[0].text + '"', '\n\n')

    return donnee



# For date
def standardiser_date(date_string):
    date_string = re.sub(r'^.*le ', '', date_string)
    date_string = re.sub(r'^.*at ', '', date_string)
    date_string = re.sub(r'^.*publié ', '', date_string)
    date_string = re.sub(r'\s+à.*$', '', date_string)
    date_string = re.sub(r'\s+\d{2}:\d{2}$', '', date_string)

    # Convertir les mois en anglias pour pouvoir le filtrer avec datetime
    months_fr_to_en = {
        'janvier': 'January',
        'février': 'February',
        'mars': 'March',
        'avril': 'April',
        'mai': 'May',
        'juin': 'June',
        'juillet': 'July',
        'août': 'August',
        'septembre': 'September',
        'octobre': 'October',
        'novembre': 'November',
        'décembre': 'December',

        'janv' : 'January',
        'févr': 'February',
        'mar': 'March',
        'avr': 'April',
        'juill': 'July',
        'sept': 'September',
        'oct': 'October',
        'nov': 'November',
        'déc': 'December'
    }

    date_string = date_string.lower()
    for fr_month, en_month in months_fr_to_en.items():
        date_string = date_string.replace(fr_month, en_month)

    format_date = [
        "%d/%m/%Y",
        "%d %m %Y",
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

def date_to_timestamp(date):
    # string -> datetime obj
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')

    # datetime -> timestamp
    timestamp = datetime.timestamp(date_time_obj) * 1000
    return timestamp
