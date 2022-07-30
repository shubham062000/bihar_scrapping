import os
import time
import pandas as pd
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from pytz import timezone
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from typing import Dict, Union
from urllib import request
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException

from .model import TenderHeader, TenderFeeDetails, ImportantDates


def launch_driver(driver_path: str):
    options = webdriver.ChromeOptions()
    options.add_argument('no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    # Set screen size to 1080p
    options.add_argument('--window-size=1920,1080')
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    options.headless = False
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Global objects
driver: webdriver.Chrome = None
log = logging.getLogger(__name__)



def scraper():
    path = ChromeDriverManager(path=os.getcwd()).install()
    # url = "https://www.eproc.bihar.gov.in/ROOTAPP/Mobility/index.html?dc=encuK824DhVFSmfVet4flvJsA#/home"
    # driver = launch_driver(path)
    # # driver.get(url)
    # Close the information banner
    close_btn_class_name = 'sha-pg010-close'
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, close_btn_class_name)))
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, close_btn_class_name).click()
    # Click on the Tenders link and then switch to the tab
    # Close the previous tab as we don't need that
    driver.find_element(By.CLASS_NAME, 'sha-pg001-02-menu-item-title-icon').click()
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])

# For converting Data Type
def format_date(date_str: str) -> datetime:
    format = '%d-%m-%Y %H%M'
    return datetime.strptime(date_str, format).astimezone(timezone('Asia/Kolkata'))


def get_table_data(keys, values):
    timestamp_regex = re.compile(
        r"^((\d{2})-(\d{2})-(\d{4})) ((\d{2}):(\d{2}) ([APM]{2}))$")
    d = {}
    for i in range(len(keys)):
        if keys[i].text and values[i].text:
            val = clean_text(values[i].text)
            if timestamp_regex.match(val):
                d[format_key(clean_text(keys[i].text))] = format_date(val)
            else:
                d[format_key(clean_text(keys[i].text))] = (
                    clean_text(values[i].text))
    return d




# Key formatter
def format_key(text: str) -> str:
    return clean_text(text).replace('.', '').replace(' ', '_').replace('/', '').replace('₹', 'rs').replace('(', '_').replace(')', '').replace('__', '_').lower().strip()



def clean_text(text: str):
    text = ' '.join(filter(lambda x: x, text.replace(
        '\n', ' ').replace('\t', ' ').replace(':', '').split()))
    if text == '':
        return None
    return text.strip()

def format_key(text: str):
    return clean_text(text).replace('.', '').replace(' ', '_').replace('/', '').replace('₹', 'rs').replace('(', '_').replace(')', '').replace('__', '_').lower().strip()

# Loop through the pages
def next_page():
    paginate = driver.find_element(By.CLASS_NAME, 'paginationLinks')
    page_links = list(filter(lambda x: 'page' in x.get_attribute('class'), paginate.find_elements(By.TAG_NAME, 'a')))
    for page_link in page_links:
        if page_link.get_attribute('class') == 'page current':
            try:
                nxt_pg = page_links[page_links.index(page_link) + 1]
                driver.execute_script('arguments[0].scrollIntoView();', nxt_pg)
                return nxt_pg
            except IndexError:
                pass
            
# Loop through the tenders in a page
def tender_link():
    t_links = driver.find_element(By.ID, 'tblSummary').find_elements(By.CLASS_NAME, 'alink')
    try:
        link = t_links[link_index]
        driver.execute_script('arguments[0].scrollIntoView();', link)
        return link
    except IndexError:
        pass
    
df = pd.DataFrame()
while True:
    link_index = 0
    while tender_link():
        main_window = driver.current_window_handle
        tender_link().click()
        link_index += 1
        driver.switch_to.window(driver.window_handles[-1])

        # Wait till the tender detail loads up
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'tenderDetail')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tender_detail = soup.find('table', {'id': 'tenderDetail'})
        dept_name = soup.find('div', {'class': 'info'}).find('td').text
        data = {'department': dept_name}
        is_test_tender = False

        # This part scrapes all the tender data as key:value pair
        for i in tender_detail.find_all('tr', {'class': 'odd'}):
            for j in i.find_all('td', {'class': 'right b'}):
                key = format_key(list(filter(lambda x: x is not None and 'class' not in x.attrs, j.find_all('span')))[0].text)
                val = clean_text(j.find_next('td').text)
                if key == 'cot' and val.lower() == 'test':
                    # Add a flag for skipping test tenders
                    is_test_tender = True
                data[key] = val
        
        if not is_test_tender:
            df = df.append(data, ignore_index=True)
            
            

        driver.close()
        driver.switch_to.window(main_window)

    if next_page():
        next_page().click()
    else:
        break
    
print(df)
