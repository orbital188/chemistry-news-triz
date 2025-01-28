import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import json
from datetime import datetime
import time
import random

def setup_driver():
    options = uc.ChromeOptions()
    ua = UserAgent()
    options.add_argument(f'user-agent={ua.random}')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Use version_main to specify the Chrome version
    driver = uc.Chrome(options=options, version_main=131)
    return driver

def scrape_article(url):
    driver = setup_driver()
    
    try:
        # Add random delay before accessing the page (2-5 seconds)
        time.sleep(random.uniform(2, 5))
        
        driver.get(url)
        print("Loaded page successfully")
        
        # Wait for the main article content to load
        wait = WebDriverWait(driver, 10)
        article = wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
        print("Found article element")
        
        # Extract article information with updated selectors
        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        print(f"Found title: {title}")
        
        # Get the article text - updated selector
        article_text = article.find_element(By.CLASS_NAME, "article-main").text
        print("Found article text")
        
        # Get publication date - try different approaches
        try:
            date_element = driver.find_element(By.CLASS_NAME, "text-gray-500")
            pub_date = date_element.text
        except:
            # If we can't find the date, use the current date
            pub_date = datetime.now().isoformat()
        print(f"Found publication date: {pub_date}")
        
        # Create article data structure
        article_data = {
            "title": title,
            "url": url,
            "publication_date": pub_date,
            "content": article_text,
            "scraped_at": datetime.now().isoformat()
        }
        
        # Save to JSON file
        with open('article_data.json', 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully scraped article: {title}")
        return article_data
        
    except Exception as e:
        print(f"Error scraping article: {str(e)}")
        print("Page source:", driver.page_source)  # Print page source for debugging
        return None
        
    finally:
        # Add random delay before closing (1-3 seconds)
        time.sleep(random.uniform(1, 3))
        driver.quit()

if __name__ == "__main__":
    url = "https://phys.org/news/2025-01-experimental-quantum-technologies-closer-students.html"
    article_data = scrape_article(url)
    if article_data:
        print("Article data has been saved to article_data.json")
