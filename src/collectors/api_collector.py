import requests
import json
from pathlib import Path
import logging
from config import config

class APICollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def fetch_data(self, api_url, params=None, headers=None):
        """Fetch data from API endpoint"""
        try:
            response = requests.get(
                api_url,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching data: {e}")
            return None
    
    def save_raw_data(self, data, filename):
        """Save raw API data to file"""
        try:
            file_path = config.RAW_DATA_DIR / filename
            with open(file_path.with_suffix('.json'), 'w') as f:
                json.dump(data, f)
            self.logger.info(f"Data saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")