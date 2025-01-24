import sys
from datetime import datetime
from toolkits import file_manager as fm, loggers
from colorama import Fore
from core import constants as ct


def maeva_initializer(weekscrap:str) -> None:
    """initialize maeva for new week scrap
    Args:
        weekscrap (str): date of week to start scrap with format 'DD/MM/YYYY
    """
    config:dict = {
        "name": "",
        "start_date":"",
        "end_date":"",
        "date_price": weekscrap
    }

    while True:
        loggers.show_message('info',"name to be used for file name")
        name:str = loggers.get_input('name')
        if name and name.isalnum():
            config['name'] = name
            break
        loggers.show_message('error',"name invalid")

    while True:       
        loggers.show_message('info',"start date of scrap (date with format 'DD/MM/YYYY')")
        date:str = loggers.get_input('start date')
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
            if date >= datetime.now():
                config['start_date'] = date
                break
            else:
                loggers.show_message('info',"start date is a past date which we can't scrap a complete data anymore. Do you want start it from current date ?")
                response:str = loggers.get_input("yes or no")
                if response.lower() == 'yes':
                    config['start_date'] = datetime.now()
                    break
                else:
                    continue
        except:
            loggers.show_message('error',"start date invalid")

    while True:       
        loggers.show_message('info', "end date of scrap (date with format 'DD/MM/YYYY')")
        end_date:str = loggers.get_input("end date")
        try:
            date = datetime.strptime(end_date, "%d/%m/%Y")
            if date > config['start_date']:
                config['end_date'] = date
                break
            else:
                loggers.show_message('error',"end date should be uper date than start date")
        except:
            loggers.show_message('error',"end date invalid")

    loggers.show_message('info',f"config will be \n\t{config}")
    response:str = loggers.get_input("yes or no")
    if response.lower() == 'yes':
        pass
        
    else:
        loggers.show_message('info', 'please relaunch program')
        sys.exit()


def maeva_starter(weekscrap:str, name:str) -> None:
    pass