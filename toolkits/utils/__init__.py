from botasaurus.browser import Driver, browser, Wait

def get_page(url:str) -> Driver:
    try:
        driver = Driver()
        driver.get(url)   
    except TimeoutError:
        driver.reload()
    driver.short_random_sleep()    
    return driver 


def split_data(data_to_split:list, by:int) -> list:
            """## split a large of list of data in to small list 

            ### Args:
                - `data_to_split (list)`: list of big data to b
                - `by (int)`: number of peace of list

            ### Returns:
                - `list`: list contains splitted list of data
            """
            return [data_to_split[i:i + by] for i in range(0, len(data_to_split), by)]
        