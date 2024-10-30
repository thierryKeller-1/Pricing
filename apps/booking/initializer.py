from toolkits.loggers import show_message
from toolkits import fm as fm
from core import constants as ct
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs



class BookingInitializer(object):

    def __init__(self, config:dict) -> None:
        self.config = config
        self.stations = ''
        self.normalized_url = []

    def load_stations(self) -> None:
        """get all stations urls"""
        show_message('info', "loading all stations urls", True)
        station_path = f"{ct.CONFIG_FOLDER_PATH}/booking/old_station.json"
        self.stations = fm.get_json_file_content(station_path)
        show_message('info', f"{len(self.stations)} stations urls loaded")

    def normalize_url_params(self, url:str, start_date:str, end_date:str) -> str:
        """normalize url parameters as needed for data scraping format
        Args:
            url (str): url
            start_date (str): starting date
            end_date (str): ending date
        Returns:
            str: new url with correct parameters
        """
        show_message('info', "normalizing url", True)
        url_params = parse_qs(urlparse(url).query)
        if "lang" not in url_params:
            url += f"&lang=fr"
        if "checkin" not in url_params:
            url += f"&checkin={start_date}"
        if "checkout" not in url_params:
            url += f"&checkout={end_date}"
        if "selected_currency" not in url_params:
            url += "&selected_currency=EUR"
        return url

    def generate_url(self) -> None:
        """generate dynamic urls for any station between interval of given dates {start_date and end_date}"""
        show_message('info', "generating urls", True)
        date_space = int((self.config['end_date'] - self.config['start_date']).days) + 1
        checkin = self.config['start_date']
        checkout = checkin + timedelta(days=self.freq)  

        for _ in range(date_space):
            for station_url in self.stations:
                url = self.normalize_url_params(station_url, checkin.strftime("%Y-%m-%d"), checkout.strftime("%Y-%m-%d"))
                self.normalized_url.append(url)
            checkin += timedelta(days=1)
            checkout += timedelta(days=1)

    def save_destination(self) -> None:
        """save json files contains all urls needed for data scraping"""
        dest_path = f"{ct.STATIC_FOLDER_PATH}/booking/{datetime.strptime(self.config['week_scrap'], '%d/%m/%Y').strftime('%d_%m_%Y')}/{self.config['freq']}/"
        fm.create_folder_if_not_exist(dest_path)
        file_path = f"{dest_path}/{self.config['name']}.json"
        fm.create_or_update_json_file(file_path, self.normalized_url)
        self.config['dest_path'] = file_path
        log_folder_path = f"{ct.LOGS_FOLDER_PATH}/booking/{datetime.strptime(self.config['week_scrap'], '%d/%m/%Y').strftime('%d_%m_%Y')}/"
        fm.create_folder_if_not_exist(log_folder_path)
        log_file_path = f"{log_folder_path}/{self.config['name']}.json"
        fm.create_or_update_json_file(log_file_path, self.config)
        show_message('info', 'configuration finished ...')
        show_message('info', f"run command -> python3 pricing -p booking -a start -w {self.config['week_scrap']} -n {self.config['name']}")

    def initialize(self) -> None:
        """initialise scraps"""
        show_message('info', 'Initializing ...')
        self.load_stations()
        self.generate_url()
        self.save_destination()


def booking_initializer_task(config:dict):
    booking = BookingInitializer(config)
    booking.initialize()

        