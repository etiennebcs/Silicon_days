import tkinter as tk
from tkinter import messagebox
import urlManager
import featureManager
import preTraitement as pT
import joblib
import csv
import pandas as pd

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
fake_news = 'https://www.slate.fr/story/255099/israel-hamas-information-guerre-desinformation-verification-fake-news-images-reseaux-sociaux-twitter'

def check_url():
    url = url_entry.get()

    
    # pre-traitement : black/white list?
    if pT.isInBlackList(url):
        messagebox.showinfo("Resultat", "le domaine est dans la blacklist")
        return
    if pT.isInWhiteList(url):
        messagebox.showinfo("Resultat", "le lien vient d'un site d'autorité")
        return


    # Obtain datas
    L = urlManager.extract_news_data(url)
    isDateNull = False

    if L[0] is None:
        messagebox.showinfo("Resultat", "nous n'avons pas réussi à obtenir le titre")
        return

    if L[2] is None:
        isDateNull = True
        publish_date = None
    else:
        L[2] = urlManager.standardiser_date(L[2])
        publish_date = urlManager.date_to_timestamp(L[2])

    nb_title_found = featureManager.get_nb_title_found(L[0])

    # Pre-traitement
    """
        if not pT.isEnough_nb_title_found(nb_title_found):
        messagebox.showinfo("Resultat", "Article est trop peu cité")
        return
    """

    if not isDateNull:
            if pT.isTooRecentDate(publish_date):
                messagebox.showinfo("Resultat", "Article est trop récent")
                return


    # data features
    feature_names = ['publish_date', 'nb_title_found', 'publish_date_was_missing']
    X = [publish_date, nb_title_found, isDateNull]
    with open('../src/temp.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        # Écrire le header
        writer.writerow(feature_names)

        # Écrire les données
        writer.writerow(X)
    data = pd.read_csv('../src/temp.csv')
    X = data[feature_names]

    # Model
        # load model
    loaded_model = joblib.load('../src/model.pkl')
        # predict
    proba_preds = loaded_model.predict_proba(X)
    continuous_preds = proba_preds[:, 1]
    prob = "{:.2f}".format(continuous_preds[0]*100)
    messagebox.showinfo("Résultat", f"{prob}% de chances que l'article soit faux")


# Main Scene
root = tk.Tk()
root.title("Vérifier l'article")

# Label :
url_label = tk.Label(root, text="Entrer le lien URL")
url_label.grid(row=0, column=0, padx=10, pady=10)

# TextField
url_entry = tk.Entry(root, width=30)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Confirm Button
confirm_button = tk.Button(root, text="Verifier", command=check_url)
confirm_button.grid(row=1, column=0, columnspan=2, pady=10)

# LOOP
root.mainloop()


