from datetime import datetime
from urllib.parse import urlparse # Permettera de récupérer l'URL

def isEnough_nb_title_found(nb_title_found):
    if nb_title_found < 10:
        return False
    else:
        return True


def isTooRecentDate(date_timestamp):
    today = str(datetime.now().date())

    # Obtain today's timestamp
    date_time_obj = datetime.strptime(today, '%Y-%m-%d')
    today_timestamp = datetime.timestamp(date_time_obj) * 1000

    if date_timestamp + 86400 >= today_timestamp:
        return True
    else:
        return False

def isInBlackList(url):
    Liste_noire = ["infowars.com", "theonion.com", "naturalnews.com",
                   "beforeitsnews.com", "lesmoutonsrebelles.com", "thedailybuzz.com",
                   "prntly.com", "yournewswire.com", "sante-nutrition.org", "fawkes-news.com",
                   "lesmoutonsenrages.fr", "wikistrike.com", "les-crises.fr", "egaliteetreconciliation.fr",
                   "nouvelordremondial.cc", "agoravox.fr", "legrandsoir.info", "panamza.com",
                   "boulevardvoltaire.fr", "dreuz.info", "contrepoints.org", "observateurcontinental.fr",
                   "reinformation.tv", "voltairenet.org", ]

    # Obtain domain
    parsed_url = urlparse(url)
    domaine = parsed_url.netloc
    if domaine.startswith('www.'):
        domaine = domaine[4:]

    if domaine in Liste_noire:
        return True
    else:
        return False

