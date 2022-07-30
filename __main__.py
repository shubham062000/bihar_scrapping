import shutil
import signal
import sys

from .constants import TEMP_DIR
from .scraper import scraper


def int_handler(a, b):
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    sys.exit(0)


signal.signal(signal.SIGINT, int_handler)
scraper()
