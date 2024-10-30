import os
import csv
from datetime import datetime, timedelta
from random import randint

from botasaurus.browser import browser, Driver, Wait
from botasaurus.soupify import soupify
from botasaurus.profiles import Profiles
from botasaurus.user_agent import UserAgent


class AnnonceCampingExtrator:
    def __init__(self, page_data:dict, week_scrap:str) -> None:
        self.url = page_data['url']
        self.page = page_data['web_page']
        self.week_scrap = week_scrap
        self.data = []
        self.storage_file = 'camping_data.csv'

    def get_link_data(self) -> tuple:
        """ Fonction pour extraire les informations de date à partir de l'URL """
        data = self.url.replace("https://www.campings.com/fr/camping/", '').split('?')
        station_key = data[0][:-1]
        
        checkin_date = self.extract_date_from_url(data[1])
        checkout_date = (datetime.strptime(checkin_date, "%d/%m/%Y") + timedelta(days=7)).strftime("%d/%m/%Y")
        
        return station_key, checkin_date, checkout_date

    def extract_date_from_url(self, query_string: str) -> str:
        """ Extraire la date d'enregistrement à partir de la chaîne de requête """
        try:
            return datetime.strptime(query_string[23:33].replace('-', '/'), "%Y/%m/%d").strftime("%d/%m/%Y")
        except Exception:
            return datetime.strptime(query_string[12:22].replace('-', '/'), "%Y/%m/%d").strftime("%d/%m/%Y")


    def extract(self) -> None:
        """ Fonction pour extraire les données de la page des campings """
        soup = self.get_page(self.url)
        if not soup:
            return

        name = soup.select_one('h1.product__name').text.strip() if soup.select_one('h1.product__name') else ''
        localite = self.get_locality(soup)

        results = soup.select('div.dca-result--accommodation')
        station_key, date_debut, date_fin = self.get_link_data()
        
        for result in results:
            date_string = result.select_one('div.dates__values').text.strip()
            if date_debut in date_string:
                self.data.append(self.parse_result(result, name, localite, date_debut, date_fin, station_key))

    def get_locality(self, soup) -> str:
        """ Extraire la localité à partir du soup """
        try:
            return soup.select_one('div.product__localisation').text.strip().split('-')[1].replace(", FRANCE", "")
        except IndexError:
            return ''

    def parse_result(self, result, name, localite, date_debut, date_fin, station_key) -> dict:
        """ Parser les informations d'un résultat """
        typologie = result.select_one('h3.result__name').text.strip() if result.select_one('h3.result__name') else ''
        adulte = result.select_one('div[data-property="adults"]').text.strip() if result.select_one('div[data-property="adults"]') else ''
        prix_actuel = self.clean_price(result.select_one('div.best-offer__price-value').text.strip()) if result.select_one('div.best-offer__price-value') else ''
        prix_init = self.clean_price(result.select_one('div.best-offer__price-old').text.strip()) if result.select_one('div.best-offer__price-old') else prix_actuel

        return {
            'web-scrapper-order': '',
            'date_price': self.week_scrap,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'prix_init': prix_init,
            'prix_actuel': prix_actuel,
            'typologie': typologie.replace('\n', ' '),
            'nom': name.replace('\n', ' '),
            'Nb personnes': adulte.replace('\n', ' '),
            'localite': localite.replace('\n', ' '),
            'n_offre': '',
            'date_debut-jour': '',
            'Nb semaines': datetime.strptime(date_debut, '%d/%m/%Y').isocalendar()[1],
            'cle_station': station_key,
            'nom_station': '',
            'url': self.url
        }

    def clean_price(self, price_string: str) -> str:
        """ Nettoyer la chaîne de prix """
        return ''.join(filter(str.isdigit, price_string))

    def create_file(self) -> None:
        """ Créer un fichier CSV pour stocker les données """
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w', newline='') as file:
                fields_name = [
                    'web-scrapper-order', 'date_price', 'date_debut', 'date_fin',
                    'prix_init', 'prix_actuel', 'typologie', 'n_offre', 'nom',
                    'Nb personnes', 'localite', 'date_debut-jour', 'Nb semaines',
                    'cle_station', 'nom_station'
                ]
                writer = csv.DictWriter(file, fieldnames=fields_name)
                writer.writeheader()

    def save_data(self) -> bool:
        """ Fonction pour sauvegarder les données dans le fichier CSV """
        if self.data:
            try:
                with open(self.storage_file, 'a', newline='') as f_object:
                    writer = csv.DictWriter(f_object, fieldnames=self.data[0].keys())
                    writer.writerows(self.data)
                return True
            except Exception as e:
                print(f"Erreur lors de l'enregistrement des données : {e}")
                return False



urls = [
    "https://www.campings.com/fr/camping/example",
    "https://www.campings.com/fr/camping/example"
]


@browser(user_agent=UserAgent.RANDOM, headless=False, block_images=True)
def campings_scraper_task(driver: Driver, data:list):
    driver.get("https://www.campings.com/fr/camping/camping-le-petit-robinson-77079#?checkInDate%3D2024-11-02", wait=randint(3, 5))
    page_data = {'url': driver.current_url, 'web_page': driver.page_html}
    c = AnnonceCampingExtrator(page_data=page_data, week_scrap='01/10/2024')
    c.extract()
    c.create_file()
    c.save_data()




# Utilisation
if __name__ == "__main__":
    campings_scraper_task()