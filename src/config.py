import os
from pathlib import Path
from dotenv import load_dotenv
import logging

class Config:
    """Central configuration manager using environment variables"""
    
    def __init__(self):
        # Set base directory
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        
        # Configure paths
        self.LOG_DIR = self.BASE_DIR / "logs"
        self.DATA_DIR = self.BASE_DIR / "data"
        self.RAW_DATA_DIR = self.DATA_DIR / "raw"
        self.PROCESSED_DATA_DIR = self.DATA_DIR / "processed"
        self.ENV_FILE = self.BASE_DIR / ".env"
        
        # Load environment variables
        load_dotenv(self.ENV_FILE)
        
        # Initialize API keys
        self.API_KEYS = {
            'jsonplaceholder': os.getenv('JSONPLACEHOLDER_API_KEY', ''),
            'weather': os.getenv('WEATHER_API_KEY', ''),
            'wikipedia': os.getenv('WIKIPEDIA_API_KEY', '')
        }
        
        # Create directories
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize config instance
config = Config()