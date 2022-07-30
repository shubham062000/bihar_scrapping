import logging
import os
from pymongo import MongoClient

from .constants import DL_DIR, LOG_DIR
# from scraper.gcs import Bucket
from .configs import MONGO_URI


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
os.makedirs(LOG_DIR, exist_ok=True)  # Creating log dir if it doesn't exist
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(os.path.join(
    LOG_DIR, f'bihar_eproc2_{os.getpid()}.log'))
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

mongo_client = MongoClient(MONGO_URI)
# gcs_bucket = Bucket('bihar_tender_bucket')

# Create download directory
os.makedirs(DL_DIR)
