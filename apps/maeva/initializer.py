from random import randint

from botasaurus.browser import Driver, browser, Wait
from botasaurus.soupify import soupify
from botasaurus.user_agent import UserAgent
from botasaurus.profiles import Profiles

from core import constants as ct
from toolkits import bs4_extension as bs4_ex
from toolkits import file_manager as fm
from toolkits.loggers import show_message



def extract(page_data:dict, selectors:dict) -> list:
    """function to extract data urls
    Args:
        page_data (dict): web page beautifulsoup element
        selectors (dict): selectors
    Returns:
        list: list of data urls
    """
    urls = []
    show_message('info', 'extracting page', True)
    container = bs4_ex.get_element_by_locator(page_data['web_page'], selectors['container'])
    show_message('info', 'container found', True)
    if container:
        toasts = bs4_ex.get_all_element_by_locator(container, selectors['toasts'])
        show_message('info', f"{len(toasts)} cards found")
        if toasts:
            for toast in toasts:
                url = bs4_ex.get_element_by_locator(toast, selectors['toast'])
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
    total = total_text.strip().split(' ')[6]
    try:
        total = int(total)
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
    show_message('info', 'build selectors', True)
    pass


@browser(user_agent=UserAgent.RANDOM, parallel=3, block_images=True, headless=False)
def maeva_initializer_task(driver: Driver, data:list) -> None:
    driver.get(data['url'], wait=randint(4, 5))
    selectors:dict = fm.get_selectors('maeva', 'initializer')
    soupe = soupify(driver.page_html)
    valid_selectors:dict = build_selectors(soupe, selectors)
    try:
        accept_btn = driver.select(bs4_ex.create_selector(selectors['agreement'][0]))
        accept_btn.click()
        show_message('info', "accept button clicked", True)
    except:
        pass
    page_nb = get_page_length(soupe, valid_selectors['result_count'])
    urls:list = generate_url(data['url'], page_nb)
    for url in urls:
        driver.get(url, wait=randint(2, 4))

    
    



