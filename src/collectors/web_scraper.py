from bs4 import BeautifulSoup
import requests
from pathlib import Path
import logging
from config import config

class WebScraper:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.logger = logging.getLogger(__name__)
    
    def fetch_page(self, url=None):
        """Fetch HTML content from URL"""
        target_url = url or self.base_url
        try:
            response = requests.get(target_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching page: {e}")
            return None
    
    def extract_data(self, html, selector, extract_rule='text'):
        """Extract data from HTML content"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select(selector)
            
            if not elements:
                return None
                
            if extract_rule == 'text':
                return [el.get_text(strip=True) for el in elements]
            elif extract_rule == 'links':
                return [el['href'] for el in elements if el.has_attr('href')]
            else:
                raise ValueError(f"Unsupported extract rule: {extract_rule}")
        except Exception as e:
            self.logger.error(f"Error extracting data: {e}")
            return None
    
    def save_raw_data(self, data, filename):
        """Save scraped data to file"""
        try:
            file_path = config.RAW_DATA_DIR / filename
            with open(file_path.with_suffix('.csv'), 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(f"{item}\n")
            self.logger.info(f"Data saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")