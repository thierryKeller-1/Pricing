
class BaseScraping(object):
    
    def __init__(self) -> None:
        self.logs = {}

    def create_log(self, base_log:dict) -> None:
        pass

    def get_log(self) -> dict | None:
        pass

    def set_log(self, log:dict=None, key:str=None, value:object=None) -> None:
        pass 

    def save_data(self) -> None:
        pass
