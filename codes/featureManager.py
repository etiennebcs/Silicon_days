from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import re


# For feature : nb_title_found
def get_nb_title_found(title):
    query = "\"" + title + "\""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={query}")
    driver.implicitly_wait(11)

    # Trouver l'élément contenant le nombre de résultats
    try:
        result_count_element = driver.find_element(By.CSS_SELECTOR, "div#result-stats")
    except Exception as e:
        print(e)
        driver.quit()
        return None

    # Extraire le nombre de résultats
    result_count_text = result_count_element.text.strip()
    result = result_count_text.replace(",", "")

    nombre = re.findall(r'\d+', result)
    nb = float(nombre[0])

    driver.quit()
    return nb


# For feature : url_rank
def get_url_rank(url):
    pass


# For feature : src_rank
def get_src_rank(src):
    pass
