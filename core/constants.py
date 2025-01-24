import os  
from dotenv import load_dotenv  


envs = os.path.join(os.path.dirname(__file__), './../', '.env')  
load_dotenv(envs)


# Environment variables
LOGS_FOLDER_PATH = os.environ.get('LOGS_FOLDER_PATH')
OUTPUT_FOLDER_PATH = os.environ.get('OUTPUT_FOLDER_PATH')
APPS_FOLDER_PATH = os.environ.get('APPS_FOLDER_PATH')
EMAIL_HOST_ADRESS = os.environ.get('EMAIL_HOST_ADRESS')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
G2A_API_TOKEN = os.environ.get('G2A_API_TOKEN')
G2A_API_URL = os.environ.get('G2A_API_URL')
DEBUG = os.environ.get('DEBUG')
ENGINE = 2


#list of developer or user email to notify
USER_EMAIL_TO_NOTIFY = [
    "test@gmail.com",
    "test@gmail.com",
    "test@gmail.com",
    "test@gmail.com",
    "test@gmail.com",
]

# booking csv fields
BOOKING_FIELDS = [
            'web-scraper-order',
            'date_price',
            'date_debut', 
            'date_fin',
            'prix_init',
            'prix_actuel',
            'typologie',
            'n_offre',
            'nom',
            'localite',
            'date_debut-jour',
            'Nb semaines'
        ]


# transformation variables
MONTH_FR_DICT = {  
            "jan": "01",  
            "feb": "02",  
            "mar": "03",  
            "apr": "04",  
            "may": "05",  
            "jun": "06",  
            "jul": "07",  
            "aug": "08",  
            "sep": "09",  
            "oct": "10",  
            "nov": "11",  
            "dec": "12"  
        }  

# date format in file
DATE_FORMAT = "%d/%m/%Y"

# web scraping plateform list
PLATEFORM = ['booking', 'maeva', 'edomizil', 'campings', 'yellohvillage']
