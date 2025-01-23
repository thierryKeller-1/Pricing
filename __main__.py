import argparse
from datetime import datetime, timedelta
from botasaurus.browser import Driver 
from botasaurus.soupify import soupify

from apps.booking.initializer import booking_initializer_task
from apps.booking.command import booking_initializer, booking_starter
from apps.maeva.initializer import maeva_initializer_task, get_page, get_page_length, generate_url
from apps.maeva.setup import maeva_intial_setup
from apps.maeva.scraper import maeva_scraper_task

from apis import load_maeva_station_list

from toolkits import file_manager as fm
from toolkits.loggers import show_message
from toolkits.utils import split_data
from core import constants as ct


def main_arguments() -> object:

    def get_monday():
        return str((datetime.now() - timedelta(days = datetime.now().weekday())).strftime("%d/%m/%Y"))

    def validate_params(args:object) -> None:
        pass

    parser = argparse.ArgumentParser(description="Pricing program",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--platform', '-p', dest='platform', help="Site source")
    parser.add_argument('--action', '-a', dest='action', help="""TAction to do: \n \t 'init': initialize destination's urls. | 'start': Launch scraps. | 'clean': clean scrapped datas""")
    parser.add_argument('--week_scrap', '-w', dest='week_scrap', default=get_monday(), help="Monday date of the week to scrap 'dd/mm/YYYY'")
    parser.add_argument('--name', '-n', dest='name', help="name to be used for this instance like output file name")
    # parser.add_argument('--engine', '-e', default=ct.ENGINE, dest='engine', help="number of engine to launch")
    
    return parser.parse_args()

args = main_arguments()

# if args.engine:
#     ct.ENGINE = args.engine

match args.platform:
    case 'booking':
        if args.action == 'init':
            booking_initializer(args.weekscrap)
        # if args.action == 'setup':
        #     booking_initial_setup(args.weekscrap, args.name)
        if args.action == 'start':
            #add driver number to the params
            booking_starter(args.weekscrap, args.name)
        if args.action == 'clean':
            pass
    case 'maeva':
        if args.action == 'init':
            metadata = {}
            metadata["week_scrap"] = args.week_scrap
            metadata["config_name"] = args.name
            show_message('info', "initialization")
            data = []
            data = fm.get_stations("maeva")

            show_message("info", f"{len(data)} stations url loaded")

            base_log = metadata
            base_log["last_index"] = 0
            base_log["last_page"] = 0
            base_output = []

            log_file_path = fm.get_path("maeva", "logs") + f"init/{metadata.get('week_scrap').replace('/',  '_')}/"
            output_file_path = fm.get_path("maeva", "dests") + f"initialization/{metadata.get('week_scrap').replace('/',  '_')}/"

            fm.create_folder_if_not_exist(log_file_path)
            fm.create_folder_if_not_exist(output_file_path)

            log_file = f"{log_file_path}{metadata.get('config_name')}.json" 
            output_file = f"{output_file_path}{metadata.get('config_name')}.json" 

            if not fm.is_file_exist(log_file):
                fm.create_or_update_json_file(log_file, base_log)

            if not fm.is_file_exist(output_file):
                fm.create_or_update_json_file(output_file, base_output)

            metadata["ouput_file"] = output_file

            logs = fm.get_json_file_content(log_file)
            show_message('info',f"logs {logs}")
            
            stations_base = fm.get_stations("maeva")
            base_selectors:dict = fm.get_selectors('maeva', 'initializer')
            result_count_selector = base_selectors.get("result_count")

            for i in range(logs.get("last_index"), len(stations_base)):
                data_url = stations_base[i]

                web_driver = get_page(data_url.get('url'))
                page_nb = get_page_length(soupify(web_driver.page_html), result_count_selector[0])
                base_urls = generate_url(data_url.get('url'), page_nb)

                if len(base_urls) >= ct.ENGINE:
                    base_urls = split_data(base_urls, ct.ENGINE)

                show_message('info', f"new logs : {logs}")

                last_page_index = logs.get("last_page", 0)
                web_driver.delete_cookies_and_local_storage()
                web_driver.close()

                show_message('info', f"urls : {len(base_urls)}")

                for k in range(last_page_index, len(base_urls)):
                    show_message('info', f"{k + 1} / {len(base_urls)}")
                    maeva_initializer_task(
                        driver=Driver,
                        data=base_urls[k], 
                        metadata=metadata
                    )
                    last_page_index += 1
                    logs["last_page"] = last_page_index
                    fm.create_or_update_json_file(log_file, logs)

                last_page_index = 0
                logs["last_page"] = last_page_index 
                logs["last_index"] = i + 1
                fm.create_or_update_json_file(log_file, logs)

        if args.action == 'setup':
            maeva_intial_setup()

        if args.action == 'scrap':
            metadata = {}
            metadata["week_scrap"] = args.week_scrap
            metadata["config_name"] = args.name
            show_message('info', "scraping...")
            data = []

            show_message("info", f"{len(data)} destination url loaded")

            base_log:dict = metadata
            base_log["last_index"] = 0
            base_log["finished"] = False
            # base_log["last_page"] = 0
            base_output:list = []

            log_file_path:str = fm.get_path("maeva", "logs") + f"scrap/{metadata.get('week_scrap').replace('/',  '_')}/"
            output_file_path:str = fm.get_path("maeva", "results") + f"scrap/{metadata.get('week_scrap').replace('/',  '_')}/"
            dest_file_path:str = fm.get_destination_path("maeva", args.wee_scrap.replace('/', '_'), args.name)

            fm.create_folder_if_not_exist(log_file_path)
            fm.create_folder_if_not_exist(output_file_path)

            log_file:str = f"{log_file_path}{metadata.get('config_name')}.json" 
            output_file:str = f"{output_file_path}{metadata.get('config_name')}.csv" 

            if not fm.is_file_exist(log_file):
                fm.create_or_update_json_file(log_file, base_log)

            if not fm.is_file_exist(output_file):
                fm.save_data_to_csv(output_file, base_output)

            metadata["ouput_file"] = output_file

            logs = fm.get_json_file_content(log_file)
            show_message('info',f"logs {logs}")
            
            metadata["stations"] = load_maeva_station_list()
            base_selectors:dict = fm.get_selectors('maeva', 'scraper')
            dest_count:int = len(fm.get_json_file_content(dest_file_path))

            while not logs["finished"]:
                if logs["last_index"] > dest_count:
                    # show scrap status here
                    show_message("info", "scraping finished")
                    break

                new_dest:list = fm.get_dest_from_index(dest_file_path, logs['last_index'])






    case 'campings':
        pass
    case 'edomizil':
        pass