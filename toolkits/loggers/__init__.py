from colorama import Fore
from core import constants as ct

import datetime  

class Logger(object):  
    def __init__(self, log_to_file=True, filename='app.log'):  
        self.log_to_file = log_to_file  
        self.filename = filename  

    def _get_timestamp(self):  
        return datetime.datetime.now().strftime('%d:%m:%Y - %H:%M:%S')  

    def log(self, message, level='INFO'):  
        timestamp = self._get_timestamp()  
        log_message = f"{timestamp} - [{level}] - {message}"  
        # Print to console  
        print(log_message)  

        # Log to file if required  
        if self.log_to_file:  
            with open(self.filename, 'a') as f:  
                f.write(log_message + '\n')  

    def info(self, message):  
        self.log(message, level='INFO')  

    def warning(self, message):  
        self.log(message, level='WARNING')  

    def error(self, message):  
        self.log(message, level='ERROR')  

logger = Logger(False)

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


