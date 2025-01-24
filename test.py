from random import randint
import json
import time

from botasaurus.browser import Driver, browser, Wait
from botasaurus.soupify import soupify
from botasaurus.user_agent import UserAgent
from botasaurus.profiles import Profiles




if __name__ == "__main__":
    driver = Driver()
    driver.get('https://www.google.com')
    time.sleep(5)
