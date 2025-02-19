import json
import re
from random import randint
from datetime import datetime, timedelta

from botasaurus.browser import Driver, browser, Wait
from botasaurus.soupify import soupify
from botasaurus.user_agent import UserAgent
from botasaurus.profiles import Profiles

from apps import ip_manager as ip
from apis import G2A_API, load_maeva_station_list
from core import constants as ct
from toolkits import bs4_extension as bs4_ex
from toolkits import file_manager as fm
from toolkits.loggers import show_message
from toolkits.utils import get_page


class MaevaPageExtractor(object):

    def __init__(self, config:dict, page_data:dict):
        self.config = config
        self.selectors = config.get('selectors')
        self.stations = config.get('stations')
        self.page_type = page_data.get('page_type')
        self.page_data = page_data
        self.uncleaned_datas = []
        self.cleaned_datas = []
        self.required_field = self.selectors.get('required_fields')
        
        del self.selectors['page_type']
        del self.selectors['required_fields']

    def clean_nom(self, name:str) -> dict | None:
        if name != "" and name is not None:
            return {"nom": name.strip()}
        return None
        
    def clean_n_offre(self, n_offre:str) -> dict | None:
        try:
            n_offre = n_offre.split(': ')[-1]
            return {"n_offre": int(n_offre)}
        except:
            return None

    def clean_date(self, date:str) -> dict | None:
        if self.page_type == 'pages':
            date = date.lower().replace('du ', '').split(' au ')
            start_date = date[0].split(' ')
            start_date = f"{start_date[0]}/{ct.MONTH_FR_DICT.get(start_date[1][:3])}/{start_date[2]}"
            try:
                datetime.strptime(start_date, "%d/%m/%Y")
            except Exception as e:
                print('datetime format invalid')
            end_date = (datetime.strptime(start_date, "%d/%m/%Y") + timedelta(days=6)).strftime("%d/%m/%Y")
            return {"date_debut": start_date, "date_fin": end_date}
        else:
            print(date)
            date = date.lower().split(' au ')
            start_date = date[0].replace('du ', '').split(' ')
            month = ct.MONTH_FR_DICT.get(start_date[1][:3]) if 'juin' not in start_date[1].lower() else ct.MONTH_FR_DICT.get('jun')
            start_date = f"{start_date[0]}/{month}/{datetime.now().year}"
            try:
                datetime.strptime(start_date, "%d/%m/%Y")
            except Exception as e:
                print(f'datetime format invalid {date}')
            end_date = (datetime.strptime(start_date, "%d/%m/%Y") + timedelta(days=6)).strftime("%d/%m/%Y")
            return {"date_debut": start_date, "date_fin": end_date}

    def clean_nom_station(self, nom_station:str) -> dict | None:
        return {"nom_station": nom_station}
    
    def clean_cle_station(self, cle_station:str) -> dict | None:
        print(f"cle_station: {cle_station}")
        if self.page_type == 'others':
            station_key = cle_station.split(',')[1].replace('.html', '')
            return {"cle_station": station_key}
        else:
            station_key = self.stations[cle_station.upper()] if cle_station.upper() in self.stations.keys() else ''
            return {"cle_station": station_key}

    def clean_localite(self, locality:str) -> None:
        if locality != "" and locality is not None:
            return {"localite":locality}
        return None

    def clean_typologie(self, typologie:str) -> dict | None:
        if typologie != "" and typologie is not None:
            typologie = typologie.replace(',', '-').replace('/', ' ou ') 
            return {"typologie":typologie}
        return None

    def clean_prix_init(self, prix:str) -> dict | None:
        if prix:
            prix = prix.split('€')[0].replace(',', '.')
            return {"prix_init": prix}
        return None
    
    def clean_prix_actuel(self, prix:str) -> dict | None:
        if prix:
            print(prix)
            prix = prix.split('€')[0].replace(',', '.')
            return {"prix_actuel": prix}
        return None
    
    def extract(self) -> None:
        match self.page_type:

            case "pages":
                data_source = {}
                for key in list(self.selectors.keys()):
                    show_message('info', f"{key}", True)
                    data_source[key] = bs4_ex.extract_element_by_locator(self.page_data.get('web_page'), self.selectors.get(key))
                self.uncleaned_datas.append(data_source)

            case "others":
                container = self.selectors.pop('container')
                datas = self.selectors.pop('datas')
                data = self.selectors.pop('data')
                cle_station = self.selectors.pop('cle_station')
                data_source = {}

                for key in list(self.selectors.keys()):
                    print(key)
                    data_source[key] = bs4_ex.extract_element_by_locator(self.page_data.get('web_page'), self.selectors.get(key))
                data_source['cle_station'] = bs4_ex.extract_element_by_locator(self.page_data.get('web_page'), cle_station)
                
                container_el = bs4_ex.get_element_by_locator(self.page_data.get('web_page'), container)
                datas_els = bs4_ex.get_all_element_by_locator(container_el, datas)
                for data_el in datas_els:
                    new_data_source = data_source

                    for content_key in list(data.keys()):
                        show_message('info', f"{content_key}", True)
                        new_data_source[content_key] = bs4_ex.extract_element_by_locator(data_el, data.get(content_key))
                    self.uncleaned_datas.append(new_data_source)

    def validate_data(self, data:dict) -> bool:
        return True

    def normalize_data(self) -> list:
        print("normalizing data")
        for uncleaned_data in self.uncleaned_datas:
            clean_data = {}
            for item in list(uncleaned_data.keys()):
                print(item)
                clean_func = getattr(self, f"clean_{item}")
                new_value = ""
                if clean_func == "clean_cle_station" and self.page_type == "pages":
                    new_value = clean_func(clean_data["nom_station"])
                else:
                    new_value = clean_func(uncleaned_data.get(item))

                if bool(new_value):
                    for key in list(new_value.keys()):
                        clean_data[key] =  new_value[key]

            clean_data["date_price"] = self.config.get('week_scrap')
            clean_data["date_debut-jour"] = ""
            clean_data["Nb semaines"] = datetime.strptime(
                        clean_data["date_debut"], '%d/%m/%Y').isocalendar()[1]

            if clean_data.get('prix_init', 0) == 0: 
                clean_data['prix_init'] = clean_data['prix_actuel']
            self.cleaned_datas.append(clean_data)
    
    def save_data(self) -> None:
        show_message("info", f"saving {len(self.cleaned_datas)} new data")
        fm.save_data_to_csv(self.config.get("ouput_file"), ct.MAEVA_FIELDS, self.cleaned_datas)

def open_driver(driver: Driver, url:str) -> Driver:
    try:
        driver.get(url)
        driver.short_random_sleep()
        return driver
    except TimeoutError:
        if ip.is_in_rotation():
            while not ip.is_connexion_enabled():
                driver.sleep(5)
                driver.delete_cookies_and_local_storage()
                try:
                    driver.reload()
                except:
                    driver.close()
                    driver = Driver()
                    driver.get(url)
                    return driver

def get_page_type(url:str) -> str:
    if '/pages/' in url:
        return 'pages'
    return 'others'

def build_selector(page_type:str, page_source:str, selectors:dict) -> dict:
    def is_selector_valid(selectors:dict, required_fields:list) -> dict:
        for selector in required_fields:
            if not selector.get(selector, False):
                return False
            return True
                
    show_message('info', "building selectors")
    print(selectors)
    new_selectors = {}
    new_selectors['page_type'] = page_type
    new_selectors['required_fields'] = selectors.get('required_fields')
    selectors = selectors.get(page_type)

    match page_type:
        case "pages":
            for item in list(selectors.keys()):
                print(item)
                for item_content in selectors.get(item):
                    if bs4_ex.check_element_by_locator(page_source, item_content):
                        new_selectors[item] = item_content
                        break
                return new_selectors
        case "others":
            for item in list(selectors.keys()):
                if item == 'data':
                    data = selectors.get(item)
                    new_selectors['data'] = {}
                    for item_ in list(data.keys()):
                        print(item_)
                        for item_content in data.get(item_):
                            if bs4_ex.check_element_by_locator(page_source, item_content):
                                new_selectors['data'][item_] = item_content
                                break

                elif item == 'cle_station':
                    for item_content in selectors.get(item):
                        if bs4_ex.check_all_element_by_locator(page_source, item_content):
                            new_selectors[item] = item_content
                            break
                else:
                    for item_content in selectors.get(item):
                        print(item_content)
                        if bs4_ex.check_element_by_locator(page_source, item_content):
                            new_selectors[item] = item_content
                            break

            show_message('info', f"new selectors build", True)
            show_message('info', f" new {new_selectors}")
            return new_selectors
        
        case _:
            show_message('danger', "page type unknown")

@browser(user_agent=UserAgent.RANDOM, block_images=True, headless=True)
def maeva_scraper_task(driver: Driver, data:list, metadata:dict) -> None:
    show_message("info", f"{data}")
    try:
        open_driver_instance = get_page(data)
    except:
        open_driver_instance = get_page(data)
    page_type = get_page_type(data)

    selectors:dict = fm.get_selectors('maeva', 'scraper')

    try:
        for pop_up in fm.get_selectors("maeva", "pop-ups"):
            accept_btn = open_driver_instance.select(bs4_ex.create_selector(pop_up))
            accept_btn.click()
            show_message('info', "accept button clicked", True)
    except:
        pass

    soupe = soupify(open_driver_instance.page_html)
    valid_selectors:dict = build_selector(page_type, soupe, selectors)
    show_message('info', f"valid selectors {valid_selectors}", True)
    metadata["selectors"] = valid_selectors
    print('extraction')

    try:
        m = MaevaPageExtractor(
                config=metadata,
                page_data = {"web_page": soupe, "page_type": page_type, "url":driver.current_url}
            )
        m.extract()
        m.normalize_data()
        m.save_data()
        
        driver.close()
    except Exception as e:
        print(e)
        pass
