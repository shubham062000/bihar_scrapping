import os
import time
from typing import Optional
from datetime import datetime
from pytz import timezone
from selenium.common.exceptions import NoSuchElementException

from .constants import DL_DIR


# Clean text data
def clean_text(text: str) -> Optional[str]:
    text = ' '.join(filter(lambda x: x, text.replace(
        '\n', ' ').replace('\t', ' ').split()))
    if text == '':
        return None
    return text.strip()


# Key formatter
def format_key(text: str) -> str:
    return clean_text(text).replace('.', '').replace(' ', '_').replace('/', '').replace('₹', 'rs').replace('(', '_').replace(')', '').replace('__', '_').lower().strip()


# Date formatter
def format_date(date_str: str) -> datetime:
    format = '%d-%m-%Y %H%M'
    return datetime.strptime(date_str, format).astimezone(timezone('Asia/Kolkata'))


def element_exists(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return


def get_downloads():
    ignorables = ['tmp', 'crdownload']
    while True:
        files = os.listdir(DL_DIR)
        download_state = any(any(file.endswith(ignorable)
                             for ignorable in ignorables) for file in files)
        if download_state:
            time.sleep(0.5)
            continue

        return [os.path.join(DL_DIR, file) for file in files]
