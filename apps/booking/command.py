import sys
from datetime import datetime
from toolkits.loggers import show_message, get_input
from colorama import Fore
from core import constants as ct


def booking_initializer(weekscrap:str) -> None:
    """initilize booking for new week scrap
    Args:
        weekscrap (str): date of week to start scrap with format 'DD/MM/YYYY'
    """
    config:dict = {
        "freq": "",
        "name": "",
        "start_date": "",
        "end_date": "",
        "date_price": weekscrap
    }
    while True:
        show_message('info',"scrap frequency choices '1' or '3' or '7'")
        freq:int = int(get_input("freq"))
        if freq in [1,3,7]:
            config['freq'] = freq
            break
        show_message('error', Fore.RED + "frequency invalid")
    while True:
        show_message('info',"name to be used for file name")
        name:str = get_input('name')
        if name and name.isalnum():
            config['name'] = name
            break
        show_message('error',"name invalid")
    while True:       
        show_message('info',"start date of scrap (date with format 'DD/MM/YYYY')")
        date:str = get_input('start date')
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
            if date >= datetime.now():
                config['start_date'] = date
                break
            else:
                show_message('info',"start date is a past date which we can't scrap a complete data anymore. Do you want start it from current date ?")
                response:str = get_input("yes or no")
                if response.lower() == 'yes':
                    config['start_date'] = datetime.now()
                    break
                else:
                    continue
        except:
            show_message('error',"start date invalid")
    while True:       
        show_message('info', "end date of scrap (date with format 'DD/MM/YYYY')")
        end_date:str = get_input("end date")
        try:
            date = datetime.strptime(end_date, "%d/%m/%Y")
            if date > config['start_date']:
                config['end_date'] = date
                break
            else:
                show_message('error',"end date should be uper date than start date")
        except:
            show_message('error',"end date invalid")

    show_message('info',f"config will be \n\t{config}")
    response:str = get_input("yes or no")
    if response.lower() == 'yes':
        pass
        
    else:
        show_message('info', 'please relaunch program')
        sys.exit()


def booking_starter(weekscrap:str, name:str) -> None:
    pass