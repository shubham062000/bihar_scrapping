import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
