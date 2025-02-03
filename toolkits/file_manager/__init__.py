import os 
import csv
import json
from toolkits.loggers import show_message
from core import constants as ct
from pathlib import Path



def is_file_exist(file_path:str) -> bool:
    return Path(file_path).exists()


def create_folder_if_not_exist(folder_path:str) -> None:
    """create folder if it doesn't exist yet
    Args:
        folder_path (Path): path of the directory
    """ 
    if not Path(folder_path).exists():
        os.makedirs(folder_path)
        show_message('info', f"folder path {folder_path} created")


def get_json_file_content(json_file_path:str, key:str=None) -> object:
    """get json file content
    Args:
        json_file_path (str): json file path
    Returns:
        object: json file content
    """
    if Path(json_file_path).exists():
        with open(json_file_path, 'r') as openfile:
            file_content = json.load(openfile)
            if file_content and key:
                try:
                    return file_content.get(key)
                except KeyError as e:
                    show_message('error',f"{e}")
            return file_content
    show_message('error', 'file does not found')


def create_or_update_json_file(file_path:str, file_content:object=[]) -> None:
    """create or update file content
    Args:
        file_path (Path): path to the file
        file_content (object): content to be add into the file
    """
    print(file_content)
    if not Path(file_path).exists():
        with open(file_path, 'w') as openfile:
            openfile.write(json.dumps(file_content))
            return
    if file_content:
        with open(file_path, 'w') as openfile:
            openfile.write(json.dumps(file_content))
    show_message('info', "file data updated")

def create_csv_file(file_path:str, fields_name:list) -> None:
    import pandas as pd
    pd.DataFrame(columns=fields_name).to_csv(file_path, index=False)

def save_data_to_csv(file_path:str, field_names:str, data:list=[]) -> None:
    """save data to csv file
    Args:
        file_path (str): csv file path
        data (list): list of data to be saved
        field_names (str): filed names of csv file
    """
    with open(file_path, mode='a', newline='', encoding='utf-8') as outputfile:
        dict_writer_object = csv.DictWriter(outputfile, fieldnames=field_names)
        dict_writer_object.writerows(data)

def save_json_data(file_path:str, data:object, key:str=None) -> None:
    """save data to a json file
    Args:
        file_path (str): json file path
        data (object): list of data to be saved
        key (str, optional): key of data type list to be updated or none in case that all data will be updated. Defaults to None.
    """
    if type(data) is list:
        show_message('info', f"saving data {len(data)}")
    else:
        show_message('info', f"{key}: {data}")
    file_content = get_json_file_content(file_path)
    if file_content and type(file_content) is list:
        file_content += [*data]
        create_or_update_json_file(file_path, file_content)
        return
    elif key:
        if type(file_content[key]) is list:
            file_content[key] += [*data]
            show_message('info', f"Data saved number {key}: {len(file_content[key])}")
            create_or_update_json_file(file_path, file_content)
            return
        else:
            file_content[key] = data
            show_message('info', f"{file_content}")
            create_or_update_json_file(file_path, file_content)
            return
    else:
        file_content += data
        create_or_update_json_file(file_path, file_content)

def check_plateform(plateform:str) -> None:
    if plateform.lower() not in ct.PLATEFORM:
        show_message('error', 'plateform not reconized')

def get_selectors(plateform:str, key:str=None) -> object:
    check_plateform(plateform)
    return get_json_file_content(f"{ct.APPS_FOLDER_PATH}/apps/{plateform}/selectors.json", key=key)
    
def get_stations(plateform:str, key:str=None) -> object:
    check_plateform(plateform)
    if key:
        return get_json_file_content(f"{ct.APPS_FOLDER_PATH}/configs/{plateform}/stations.json", key)
    return get_json_file_content(f"{ct.APPS_FOLDER_PATH}/configs/{plateform}/stations.json")

def get_path(plateform:str, folder_name:str) -> str | None:
    check_plateform(plateform)
    match folder_name:
        case 'configs':
            return f"{ct.APPS_FOLDER_PATH}/configs/{plateform}/"
        case 'statics':
            return f"{ct.APPS_FOLDER_PATH}/statics/{plateform}/"
        case 'dests':
            return f"{ct.APPS_FOLDER_PATH}/dests/{plateform}/"
        case 'logs':
            return f"{ct.LOGS_FOLDER_PATH}/{plateform}/"
        case 'results':
            return f"{ct.OUTPUT_FOLDER_PATH}/"
        

def get_destination_path(plateform:str, week_scrap:str, file_name:str) -> object:
    dest_path = get_path(plateform, "dests")
    return f"{dest_path}scraps/{week_scrap}/{file_name}.json"


def get_dest_from_index(dest_path:str, index:int, engine:int=ct.ENGINE) -> list:
    dest = get_json_file_content(dest_path)
    return dest[index : index + engine]


def get_item_from_index(object_list:list, index:int, by:int=1) -> list:
    return object_list[index : index + by]
        