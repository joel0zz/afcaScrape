from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import sys
import time


# Set Path for selenium FIreFox driver
path = os.getcwd() + r"\geckodriver.exe"
driver = webdriver.Firefox(executable_path=path)


def scrape():
    driver.get("https://apps.afca.org.au/dapweb/idr/")
    inputElement = driver.find_element_by_name("ctl00$body$txtName")
    inputElement.send_keys("White Knight")
    inputElement.send_keys(Keys.ENTER)
    # driver.close()
    # driver.quit()


if __name__ == '__main__':
    scrape()
