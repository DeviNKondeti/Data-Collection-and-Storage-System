import logging
from datetime import datetime
from config import config
from collectors.api_collector import APICollector
from collectors.web_scraper import WebScraper

def configure_logging():
    """Configure logging system"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_DIR / 'data_collection.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def collect_api_data(logger):
    """Collect data from APIs"""
    try:
        collector = APICollector()
        logger.info("Collecting from JSONPlaceholder API")
        
        # Example API call - no API key needed for this endpoint
        data = collector.fetch_data("https://jsonplaceholder.typicode.com/posts")
        if data:
            filename = f"posts_{datetime.now().strftime('%Y%m%d')}.json"
            collector.save_raw_data(data, filename)
    except Exception as e:
        logger.error(f"API collection failed: {e}")

def collect_web_data(logger):
    """Collect data through web scraping"""
    try:
        # Initialize with base URL
        scraper = WebScraper(base_url="https://en.wikipedia.org")
        
        logger.info("Scraping Wikipedia Data Science page")
        html = scraper.fetch_page("https://en.wikipedia.org/wiki/Data_science")
        if html:
            paragraphs = scraper.extract_data(html, 'p', 'text')
            if paragraphs:
                filename = f"wikipedia_paragraphs_{datetime.now().strftime('%Y%m%d')}.csv"
                scraper.save_raw_data(paragraphs, filename)
    except Exception as e:
        logger.error(f"Web scraping failed: {e}")

def main():
    """Main application entry point"""
    logger = configure_logging()
    
    try:
        logger.info("=== Starting Data Collection ===")
        collect_api_data(logger)
        collect_web_data(logger)
        logger.info("=== Data Collection Completed ===")
    except Exception as e:
        logger.critical(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()