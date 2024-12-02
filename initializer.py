from random import randint
import json

from botasaurus.browser import Driver, browser, Wait
from botasaurus.soupify import soupify
from botasaurus.user_agent import UserAgent
from botasaurus.profiles import Profiles

from apps import ip_manager as ip
from core import constants as ct
from toolkits import bs4_extension as bs4_ex
from toolkits import file_manager as fm
from toolkits.loggers import show_message




def extract(page_data:str, selectors:dict) -> list:
    """function to extract data urls
    Args:
        page_data (dict): web page beautifulsoup element
        selectors (dict): selectors
    Returns:
        list: list of data urls
    """
    urls = []
    show_message('info', 'extracting page', True)
    container = bs4_ex.get_element_by_locator(page_data, selectors['container'])
    show_message('info', 'container found', True)
    if container:
        toasts = bs4_ex.get_all_element_by_locator(container, selectors['toasts'])
        show_message('info', f"{len(toasts)} cards found")
        if toasts:
            for toast in toasts:
                url = bs4_ex.extract_element_by_locator(toast, selectors['toast'])
                if url:
                    urls.append(url)
    show_message('info', f"{len(urls)} urls extracted")

    return urls
    

def generate_url(url:str, nb_page:int=1) -> list:
    """generate dynamic url with page parameters
    Args:
        url (str): url
        nb_page (int, optional): number of page. Defaults to 1.
    Returns:
        list: list of urls with number of page in params
    """
    show_message('info', 'generating urls', True)
    urls:list = []
    for i in range(1, (nb_page+1)):
        urls.append(url + f"&page={i}")
    show_message('info', f" {len(urls)} urls generated", True)
    return urls
    
def get_page_length(element:object, selector:dict) -> int:
    """get page number
    Args:
        element (object): Beautifulsoup element
        selector (dict): selectors
    Returns:
        int: number of page
    """
    total_text = bs4_ex.extract_element_by_locator(element, selector)
    print(total_text)
    total = total_text.strip().split(' ')[0]
    try:
        total = int(total)
        print(f'total {total}')
    except Exception as e:
        show_message('errror', f"{e}", True)
        total:int = 0
    if total > 30:
        page_nb:int = (total // 30) if (total % 30 == 0) else ((total // 30) + 1)
        show_message('info', f"website contains {page_nb} pages")
        return page_nb
    show_message('info', f" website contains {1} page")
    return 1


def build_selectors(element:object, selectors:dict) -> dict:
    new_selectors = {}
    for item in selectors['container']:
        if bool(bs4_ex.get_element_by_locator(element, item)):
            new_selectors['container'] = item
            break

    container = bs4_ex.get_element_by_locator(element, new_selectors['container'])
    for item in selectors['toasts']:
        if bool(bs4_ex.get_all_element_by_locator(container, item)):
            new_selectors['toasts'] = item
            break

    toasts = bs4_ex.get_all_element_by_locator(container, new_selectors['toasts'])
    for item in selectors['toast']:
        for content in toasts:
            if bool(bs4_ex.get_element_by_locator(content, item)):
                new_selectors['toast'] = item 
                break
        if new_selectors.get('toast', None):
            break
    
    for item in selectors['result_count']:
        if bool(bs4_ex.get_element_by_locator(element, item)):
            new_selectors['result_count'] = item 

    print(new_selectors)
    return new_selectors

def new_driver(driver: Driver, url:str) -> Driver:
    try:
        driver.get(url, wait=randint(4, 5))
        return driver
    except:
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
                
def get_selectors() -> dict:
    with open('/home/keller/Documents/Jobdev/Jobdev/programs/dev/pricing/pricing/apps/maeva/selectors.json', 'r') as openfile:
        selectors = json.load(openfile)
        return selectors['initializer']


@browser(user_agent=UserAgent.RANDOM, block_images=True, headless=False)
def maeva_initializer_task(driver: Driver, data:list, config:dict=None) -> None:
    try:
        new_driver_instance = new_driver(driver, data['url'])
    except:
        new_driver_instance = new_driver(driver, data['url'])
    # selectors:dict = fm.get_selectors('maeva', 'initializer')
    selectors:dict = get_selectors()
    soupe = soupify(new_driver_instance.page_html)
    valid_selectors:dict = build_selectors(soupe, selectors)
    try:
        accept_btn = new_driver_instance.select(bs4_ex.create_selector(fm.get_selectors('maeva', 'pop-ups')[0]))
        accept_btn.click()
        show_message('info', "accept button clicked", True)
    except:
        pass
    page_nb = get_page_length(soupe, valid_selectors['result_count'])
    urls:list = generate_url(data['url'], page_nb)
    for url in urls:
        print(f" ===> {url}")
        new_driver_instance.get(url, wait=randint(1,4))
        urls = extract(soupify(driver.page_html), valid_selectors)
        fm.save_data_to_json("urls.json", urls)
        new_driver_instance.delete_cookies_and_local_storage()


if __name__ == "__main__":
    data = fm.get_json_file_content("./data.json")
    maeva_initializer_task(data)


