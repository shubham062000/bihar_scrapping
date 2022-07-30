import os


BASE_URL = "https://www.eproc.bihar.gov.in/ROOTAPP/Mobility/index.html?dc=encuK824DhVFSmfVet4flvJsA#/home"

WORK_DIR = os.getcwd()
TEMP_DIR = os.path.join(os.getenv('TMP') or '/tmp',
                        'scraper_' + str(os.getpid()))
DL_DIR = os.path.join(TEMP_DIR, 'dl')
LOG_DIR = os.path.join(WORK_DIR, 'logs')
