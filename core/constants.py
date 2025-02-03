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

# Maeva csv fields
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

# Maeva csv fields
MAEVA_FIELDS = [
    "web-scrapper-order",
    "date_price",
    "date_debut",
    "date_fin",
    "prix_init",
    "prix_actuel",
    "typologie",
    "n_offre",
    "nom",
    "localite",
    "date_debut-jour",
    "Nb semaines",
    "cle_station",
    "nom_station"
]

# transformation variables
MONTH_FR_DICT = {  
        'jan': '01',
        'fév': '02',
        'mar': '03',
        'avr': '04',
        'mai': '05',
        'jun': '06',
        'jui': '07',
        'aoû': '08',
        'sep': '09',
        'oct': '10',
        'nov': '11',
        'déc': '12' 
        }  

# date format in file
DATE_FORMAT = "%d/%m/%Y"

# web scraping plateform list
PLATEFORM = ['booking', 'maeva', 'edomizil', 'campings', 'yellohvillage']
