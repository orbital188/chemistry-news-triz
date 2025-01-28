from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import json
from datetime import datetime
import time
import random
import os
from dotenv import load_dotenv
import logging
from selenium.common.exceptions import TimeoutException, WebDriverException
import backoff

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

class ArticleScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.articles_scraped = 0
        self.max_retries = 3
        
    def setup_driver(self):
        options = Options()
        
        # Set Firefox-specific options
        options.set_preference("general.useragent.override", self.ua.firefox)
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("privacy.trackingprotection.enabled", False)
        
        # Additional privacy and performance settings
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("network.http.use-cache", False)
        
        # Create Firefox driver instance
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
        
        return driver

    @backoff.on_exception(
        backoff.expo,
        (TimeoutException, WebDriverException),
        max_tries=3,
        max_time=300
    )
    def scrape_article(self, url):
        driver = None
        try:
            # Respect rate limits
            if self.articles_scraped > 0:
                wait_time = random.uniform(120, 150)  # Doubled from 60-75 to 120-150 seconds between requests
                logging.info(f"Waiting {wait_time:.2f} seconds before next request...")
                time.sleep(wait_time)
            
            driver = self.setup_driver()
            logging.info(f"Starting to scrape: {url}")
            
            # Random delay before accessing the page (10-30 seconds, doubled from 5-15)
            time.sleep(random.uniform(10, 30))
            
            driver.get(url)
            logging.info("Page loaded successfully")
            
            # Wait for the main article content to load
            wait = WebDriverWait(driver, 10)
            article = wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
            logging.info("Found article element")
            
            # Extract article information
            title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
            logging.info(f"Found title: {title}")
            
            # Get the article text
            article_text = article.find_element(By.CLASS_NAME, "article-main").text
            logging.info("Found article text")
            
            # Get publication date
            try:
                date_element = driver.find_element(By.CLASS_NAME, "text-gray-500")
                pub_date = date_element.text
            except:
                pub_date = datetime.now().isoformat()
            logging.info(f"Found publication date: {pub_date}")
            
            # Create article data structure
            article_data = {
                "title": title,
                "url": url,
                "publication_date": pub_date,
                "content": article_text,
                "scraped_at": datetime.now().isoformat(),
                "scraping_method": "firefox"
            }
            
            self.articles_scraped += 1
            return article_data
            
        except Exception as e:
            logging.error(f"Error scraping article {url}: {str(e)}")
            if driver:
                logging.error(f"Page source: {driver.page_source}")
            return None
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def process_feed_articles(self, input_file='chemistry_news.json', output_dir='scraped_articles'):
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Load articles from RSS feed JSON
            with open(input_file, 'r', encoding='utf-8') as f:
                feed_data = json.load(f)
            
            articles = feed_data.get('articles', [])
            total_articles = len(articles)
            logging.info(f"Found {total_articles} articles to process")
            
            # Process each article
            for i, article in enumerate(articles, 1):
                url = article.get('link')
                if not url:
                    continue
                
                # Create a filename based on the article title or URL
                filename = f"article_{i}.json"
                output_path = os.path.join(output_dir, filename)
                
                # Skip if already scraped
                if os.path.exists(output_path):
                    logging.info(f"Article {i}/{total_articles} already scraped, skipping...")
                    continue
                
                logging.info(f"Processing article {i}/{total_articles}")
                article_data = self.scrape_article(url)
                
                if article_data:
                    # Save individual article data
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(article_data, f, ensure_ascii=False, indent=4)
                    logging.info(f"Saved article data to {output_path}")
                
                # Random additional delay between articles (10-30 seconds, doubled from 5-15)
                time.sleep(random.uniform(10, 30))
                
        except Exception as e:
            logging.error(f"Error processing feed articles: {str(e)}")

def main():
    scraper = ArticleScraper()
    scraper.process_feed_articles()

if __name__ == "__main__":
    main()
