import pandas as pd
from pathlib import Path
from config import config
import json

class DataLoader:
    @staticmethod
    def load_json_data(filename):
        """Load JSON data from raw data directory"""
        file_path = config.RAW_DATA_DIR / filename
        with open(file_path) as f:
            return json.load(f)
    
    @staticmethod
    def load_csv_data(filename):
        """Load CSV data from raw data directory"""
        file_path = config.RAW_DATA_DIR / filename
        return pd.read_csv(file_path)
    
    @staticmethod
    def get_available_files():
        """List available data files for visualization"""
        return [f.name for f in config.RAW_DATA_DIR.glob('*') if f.is_file()]