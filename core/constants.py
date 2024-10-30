import os  
from dotenv import load_dotenv  


envs = os.path.join(os.path.dirname(__file__), './../', '.env')  
load_dotenv(envs)



LOGS_FOLDER_PATH = os.environ.get('LOGS_FOLDER_PATH')
STATIC_FOLDER_PATH = os.environ.get('STATIC_FOLDER_PATH')
CONFIG_FOLDER_PATH = os.environ.get('CONFIG_FOLDER_PATH')
OUTPUT_FOLDER_PATH = os.environ.get('OUTPUT_FOLDER_PATH')
DEST_FOLDER_PATH = os.environ.get('DEST_FOLDER_PATH')
APPS_FOLDER_PATH = os.environ.get('DEST_FOLDER_PATH')

DEBUG = os.environ.get('DEBUG')

BOOKING_FIELDS = {
    "fields": [
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
        ],
    "required_fields": [
        'date_price',
        'date_debut', 
        'date_fin',
        'prix_init',
        'prix_actuel',
        'typologie',
        'nom',
        'localite',
        'Nb semaines'
    ]
}

