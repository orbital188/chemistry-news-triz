import feedparser
import json
from datetime import datetime
import requests
from fake_useragent import UserAgent
import time
import random

class RSSFeedScraper:
    def __init__(self, rss_url):
        self.rss_url = rss_url
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/rss+xml, application/xml, application/atom+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def get_feed(self):
        try:
            # Add random delay to mimic human behavior
            time.sleep(random.uniform(1, 3))
            
            # Fetch RSS feed content
            response = requests.get(self.rss_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse the feed
            feed = feedparser.parse(response.content)
            
            # Process feed entries
            articles = []
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'published_parsed': time.strftime('%Y-%m-%d %H:%M:%S', entry.get('published_parsed')) if entry.get('published_parsed') else None,
                    'authors': [author.get('name', '') for author in entry.get('authors', [])],
                    'tags': [tag.get('term', '') for tag in entry.get('tags', [])],
                }
                articles.append(article)
            
            # Create feed metadata
            feed_data = {
                'feed_title': feed.feed.get('title', ''),
                'feed_link': feed.feed.get('link', ''),
                'feed_description': feed.feed.get('description', ''),
                'feed_language': feed.feed.get('language', ''),
                'last_updated': datetime.now().isoformat(),
                'articles': articles
            }
            
            return feed_data
            
        except Exception as e:
            print(f"Error fetching RSS feed: {str(e)}")
            return None

    def save_to_json(self, data, output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {output_file}")
            return True
        except Exception as e:
            print(f"Error saving data to JSON: {str(e)}")
            return False

def main():
    # RSS feed URL
    rss_url = "https://phys.org/rss-feed/breaking/chemistry-news/"
    
    # Create scraper instance
    scraper = RSSFeedScraper(rss_url)
    
    # Get feed data
    print("Fetching RSS feed...")
    feed_data = scraper.get_feed()
    
    if feed_data:
        # Save to JSON file
        output_file = 'chemistry_news.json'
        if scraper.save_to_json(feed_data, output_file):
            print(f"Successfully scraped {len(feed_data['articles'])} articles")
            
            # Print some basic stats
            print("\nFeed Statistics:")
            print(f"Feed Title: {feed_data['feed_title']}")
            print(f"Number of Articles: {len(feed_data['articles'])}")
            print(f"Last Updated: {feed_data['last_updated']}")
    else:
        print("Failed to fetch RSS feed data")

if __name__ == "__main__":
    main()
