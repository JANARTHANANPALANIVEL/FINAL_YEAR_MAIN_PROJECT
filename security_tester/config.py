import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ZAP_PATH = os.getenv('ZAP_PATH')
    ZAP_API_KEY = os.getenv('ZAP_API_KEY')
    ZAP_PORT = int(os.getenv('ZAP_PORT', 8080))
    SCAN_TIMEOUT = 120  # seconds
    RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    
    @staticmethod
    def init_app():
        os.makedirs(Config.RESULTS_FOLDER, exist_ok=True)