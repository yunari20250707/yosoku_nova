# nova_core/config.py

import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NEWS_HISTORY_DIR = os.path.join(BASE_DIR, 'news_history')
PREDICTIONS_DIR = os.path.join(BASE_DIR, 'predictions')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

def timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

from dotenv import load_dotenv
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
