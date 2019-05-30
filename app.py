from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import os
import time


def search_afca():
    # Set Path for selenium FireFox driver
    path = os.getcwd() + r"\geckodriver.exe"
    driver = webdriver.Firefox(executable_path=path)

    for member in members:  # iterate over the members list

        # Load page, fill out the 'Name' form field & then press ENTER to submit the search.
        driver.get("https://apps.afca.org.au/dapweb/idr/")
        input_element = driver.find_element_by_name("ctl00$body$txtName")
        input_element.send_keys(member)
        input_element.send_keys(Keys.ENTER)
        time.sleep(1)  # wait for new elements on page to load

        #  Pass the driver to the scrape function to extract member number & ACN/ABN
        scrape_current_page_source(driver)

    driver.close()
    driver.quit()


def scrape_current_page_source(d):
    current_page_html = BeautifulSoup(d.page_source, 'html.parser')  # parse page src into a bs4 object.

    # scrape the 'member' class & split/strip the text to remove unnecessary information. Then append to relevant list.
    member_numbers.append(current_page_html.findAll('div', {"class": "member"})[0]
                          .get_text().split(":")[1].split('\n')[0].strip())

    member_ABNs.append(current_page_html.findAll('div', {"class": "member"})[0]
                       .get_text().split(":")[2].strip())


# turn excel doc into DataFrame and retrieve values from 'Members' column. return list
def load_column_data_from_spreadsheet(path, column):
    return pd.read_excel(path)[column].values.tolist()


if __name__ == '__main__':
    # initialize lists which will contain all needed data & then used as columns in pandas.
    members = load_column_data_from_spreadsheet('book.xlsx', 'Members')  # path / column name
    member_numbers = []
    member_ABNs = []

    # retrieve information.
    search_afca()

    # create pandas DataFrame using lists & export to csv.
    df = pd.DataFrame({'Member': members, 'Member Number': member_numbers, 'Member ACN/ABN': member_ABNs})
    df.to_csv('afca.csv', encoding='utf-8')


