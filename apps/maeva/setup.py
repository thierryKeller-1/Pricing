import sys
import os
from datetime import datetime
from colorama import Fore

from toolkits.loggers import show_message
from toolkits import file_manager as fm, loggers
from core import constants as ct

def maeva_intial_setup() -> None:
    """initialize maeva for new week scrap
    Args:
        weekscrap (str): date of week to start scrap with format 'DD/MM/YYYY
    """
    config:dict = {
        "config_name": "",
        "week_scrap": "",
        "start_date":"",
        "end_date":"",
        "last_index": 0,
        "end_at": "",
    }

    sources = fm.get_path("maeva", "dests") + "setups/sources/"
    sources_dests = fm.combine_file_content(sources, 'json')
    show_message('info', f"{len(sources_dests)} sources loaded")

    # config_name
    while True:
        loggers.show_message('info',"config_name to be used")
        name:str = loggers.get_input('config_name')
        if name and name.isalnum():
            config['config_name'] = name
            break
        loggers.show_message('error',"config_name invalid")

    # week_scrap
    while True:       
        loggers.show_message('info',"week scrap (date with format 'DD/MM/YYYY')")
        date:str = loggers.get_input('week_scrap')
        try:
            date = datetime.strptime(date, ct.DATE_FORMAT)
            if date.weekday() == 0:
                config['week_scrap'] = date.strftime(ct.DATE_FORMAT)
                break
            else:
                loggers.show_message('info',"week scrap should be monday")
        except:
            loggers.show_message('error',"week scrap date invalid")

    # start_date
    while True:       
        loggers.show_message('info',"start date of scrap (date with format 'DD/MM/YYYY')")
        date:str = loggers.get_input('start date')
        try:
            date = datetime.strptime(date, ct.DATE_FORMAT)
            if date >= datetime.now():
                config['start_date'] = date.strftime(ct.DATE_FORMAT)
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

    # end_date
    while True:       
        loggers.show_message('info', "end date of scrap (date with format 'DD/MM/YYYY')")
        end_date:str = loggers.get_input("end date")
        try:
            date = datetime.strptime(end_date, ct.DATE_FORMAT)
            if date > datetime.strptime(config['start_date'], ct.DATE_FORMAT):
                config['end_date'] = date.strftime(ct.DATE_FORMAT)
                break
            else:
                loggers.show_message('error',"end date should be uper date than start date")
        except Exception as e:
            loggers.show_message('error',f"end date invalid {e}")

    # start_from
    while True:
        loggers.show_message('info', "start scrap from index")
        start_from: int = loggers.get_input("start from index")
        try:
            config["last_index"] = int(start_from)
            break
        except:
            loggers.show_message('error',"start index invalid")

    # end_at
    while True:
        loggers.show_message('info', "end scrap at index index")
        end_at: int = loggers.get_input("end at index")
        try:
            config["end_at"] = int(end_at)
            config
            break
        except:
            loggers.show_message('error',"end index invalid")

        #number of config files
    while True:
        loggers.show_message('info',"number of config files")
        number:str = loggers.get_input('numbers')
        if number and number.isnumeric():
            
            break
        loggers.show_message('error',"config_name invalid")

    loggers.show_message('info',f"config will be \n\t{config}")
    response:str = loggers.get_input("yes or no")
    if response.lower() == 'yes':
        log_file_path = fm.get_path("maeva", "logs") + config["week_scrap"].replace("/", "_")
        dest_file_path = fm.get_path("maeva", "dest") + config["week_scrap"].replace("/", "_")
        result_file_path = fm.get_path("maeva", "results") + config["week_scrap"].replace("/", "_")
        files = [log_file_path, dest_file_path, result_file_path]
        fm.create_folder_if_not_exist()

    else:
        loggers.show_message('info', 'please relaunch program')
        sys.exit()