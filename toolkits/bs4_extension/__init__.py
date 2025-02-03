from core import constants as ct
from toolkits.loggers import show_message


def check_element_by_locator(element:object, locator:dict) -> bool:
    """check bs4 element by it's locator from an element
    Args:
        element (object): bs4 parent element
        locator (dict): locator of element to search
    Returns:
        bool: True if found or False
    """
    show_message('info', "checking element by locator", True)
    element_found = False
    if locator['by_tag_only']:
        element_found = bool(element.find(locator['tag']))
    else:
        element_found = bool(element.find(locator['tag'], {locator['attr_key']:locator['attr_value']}))
    show_message('info', f" element found ==> {element_found} ", True)
    return element_found

def check_all_element_by_locator(element:object, locator:dict) -> bool:
    """check bs4 element by it's locator from an element
    Args:
        element (object): bs4 parent element
        locator (dict): locator of element to search
    Returns:
        bool: True if found or False
    """
    show_message('info', "checking element by locator", True)
    element_found = False
    if locator['by_tag_only']:
        element_found = bool(element.find_all(locator['tag']))
    else:
        element_found = bool(element.find_all(locator['tag'], {locator['attr_key']:locator['attr_value']}))
    show_message('info', f" element found ==> {element_found} ", True)
    return element_found

def create_selector(locator:dict) -> str:
    """create a locator from element selector
    Args:
        locator (dict): all element information in a dict like tag name, class ,...
    Returns:
        str: a selector like div[class='my_class']
    """
    show_message('info', f"creating selector locator", True)
    return f"{locator['tag']}[{locator['attr_key']}='{locator['attr_value']}']"

def get_element_by_locator(element:object, locator:dict) -> object | None:
    """get element by locator
    Args:
        element (object): bs4 parent element
        locator (dict): all element information in a dict like tag name, class ,...
    Returns:
        object | None: bs4 element if found or None
    """
    show_message('info', "getting element by locator", True)
    if locator['by_tag_only']:
        element_found = element.find(locator['tag'])
        return element_found
    else:
        element_found = element.find(locator['tag'], {locator['attr_key']:locator['attr_value']})
        return element_found
    
def get_all_element_by_locator(element:object, locator:dict) -> object | None:
    """get all element by locator in a parent element
    Args:
        element (object): bs4 parent element
        locator (dict): all element information in a dict like tag name, class ,...
    Returns:
        object | None: list of all bs4 element if found or None
    """
    show_message('info', "getting all element by locator")
    if locator['by_tag_only']:
        element_found = element.find_all(locator['tag'])
        return element_found
    else:
        element_found = element.find_all(locator['tag'], {locator['attr_key']:locator['attr_value']})
        return element_found

def extract_element_by_locator(element:object, locator:dict) -> object | None:
    """extract bs4 element data by it's locator
    Args:
        element (object): bs4 element
        locator (dict): all element information in a dict like tag name, class ,...
    Returns:
        object | None: element data
    """
    def clean_text(source:str) -> str:
        """remove encoding in text
        Args:
            source (str): text string
        Returns:
            str: text cleaned
        """
        try:
            text = source.replace('\xa0', ' ').replace('\u00e9', 'é').replace('\u00a0', '').replace('\u00f3','ó').replace('\u2022', '').strip()
        except:
            pass
        show_message('info', text, True)
        return text
    
    
    print(f"extracting element by locator {locator}")
    element_value = ""
    if locator.get('multiple', False):
        elements = get_all_element_by_locator(element, locator)
        element_value = elements[locator.get('index')]
    else:
        element_value = get_element_by_locator(element, locator)

    if element_value:
        match locator['target']:
            case "text":
                return clean_text(element_value.get_text())
            case "attribute":
                return clean_text(element_value[locator['value_attr']])
            case "child":
                sub_element = ''
                if locator['child']['by_tag_only']:
                    sub_element = element_value.find(locator['child']['tag'], href=True if locator['child']['value_attr'] == 'href' else False)
                else:
                    sub_element = element_value.find(locator['child']['tag'], {locator['child']['attr_key']:locator['child']['attr_value']}, href=True if locator['child']['target'] == 'href' else False)
                if locator['child']['target'] == 'attribute':
                    cleaned_text = clean_text(sub_element[locator['child']['value_attr']])
                    show_message('info', cleaned_text, True)
                    return cleaned_text if cleaned_text else locator.get('default_value', '')
                else:
                    try:
                        return clean_text(sub_element.get_text().strip())
                    except Exception as e:
                        return locator.get('default_value', '')

    else:
        show_message('info', 'element not found')
        return
    
