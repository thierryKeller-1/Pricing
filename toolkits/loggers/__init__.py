# import logging
# import os
# import smtplib
# from colorama import Fore
# from core import constants as ct


# class IgnoreRefusedConnectionFilter(logging.Filter):  
#     def __init__(self, name = "IgnoreRefusedConnectionFilter"):
#         super().__init__(name)

#     def filter(self, record):  
#         return "Connection refused - goodbye" not in record.getMessage()  


# logging.basicConfig(encoding='utf-8', level=logging.INFO, format=Fore.GREEN + '%(asctime)s - %(levelname)s - %(message)s', errors="errors")

# logging.Filterer().addFilter(filter=IgnoreRefusedConnectionFilter)  

# def show_message(msg_type:str, message:str, hide_in_prod:bool=False) -> None:
#     if hide_in_prod and ct.DEBUG == False:
#         return
#     match msg_type.lower():
#         case 'info':
#             logging.info(Fore.GREEN + message)
#         case 'debug':
#             logging.debug(Fore.CYAN + message)
#         case 'warnning':
#             logging.warning(Fore.BLUE + message)
#         case 'error':
#             logging.error(Fore.RED + message)
#         case 'critical':
#             logging.critical(message)

# def get_input(message:str) -> object:
#     response = input(Fore.GREEN + f"$ {message} ==> ") 
#     return response

# def report_bug(data:object) -> None:
#     pass

# def get_log(plateform:str, week_date:str, file_name:str) -> object:
#     pass

# def report_status():
#     pass

import logging
from colorama import Fore
from core import constants as ct


class IgnoreRefusedConnectionFilter(logging.Filter):
    """
    Custom logging filter to exclude unwanted log messages.
    """
    def filter(self, record):
        # Exclude logs containing "Connection refused - goodbye"
        if "Connection refused - goodbye" in record.getMessage():
            return False
        return True


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    errors="ignore"
)

# Get the root logger
logger = logging.getLogger()

# Add the custom filter to the logger
logger.addFilter(IgnoreRefusedConnectionFilter())


def show_message(msg_type: str, message: str, hide_in_prod: bool = False) -> None:
    """
    Display log messages with color coding based on the message type.
    Optionally hide the message in production.
    """
    if hide_in_prod and not ct.DEBUG:
        return

    match msg_type.lower():
        case 'info':
            logger.info(Fore.GREEN + message)
        case 'debug':
            logger.debug(Fore.CYAN + message)
        case 'warning':
            logger.warning(Fore.BLUE + message)
        case 'error':
            logger.error(Fore.RED + message)
        case 'critical':
            logger.critical(Fore.RED + message)


def get_input(message: str) -> object:
    """
    Prompt the user for input and return the response.
    """
    response = input(Fore.GREEN + f"$ {message} ==> ")
    return response


def report_bug(data: object) -> None:
    """
    Placeholder for bug reporting functionality.
    """
    pass


def get_log(platform: str, week_date: str, file_name: str) -> object:
    """
    Placeholder for retrieving logs.
    """
    pass


def report_status():
    """
    Placeholder for status reporting functionality.
    """
    pass


