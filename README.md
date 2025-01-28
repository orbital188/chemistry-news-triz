# Chemistry News Analysis with TRIZ Principles

This project is an automated workflow that scrapes chemistry research articles from phys.org, analyzes them through the lens of TRIZ principles using GPT-4, and presents them in a beautiful Streamlit web interface.

## Workflow Overview

1. **RSS Feed Scraping** (`rss_scraper.py`): 
   - Fetches the latest chemistry news from phys.org's RSS feed
   - Saves article metadata and links to `chemistry_news.json`

2. **Article Scraping** (`batch_article_scraper.py`):
   - Reads article links from `chemistry_news.json`
   - Uses Selenium with Firefox to scrape full article content
   - Saves individual articles to the `scraped_articles` directory

3. **GPT Analysis** (`gpt_article_analyzer.py`):
   - Processes scraped articles using GPT-4
   - Analyzes innovation and TRIZ principles in each article
   - Saves analysis to the `gpt_processed` directory

4. **Article Generation** (`article_generator.py`):
   - Takes GPT-analyzed content and generates comprehensive articles
   - Focuses on innovation analysis and TRIZ principles
   - Saves generated articles to the `generated_articles` directory

5. **Web Interface** (`website/`):
   - Presents articles in a modern Streamlit interface
   - Features latest articles and full archive
   - Provides an engaging reading experience

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**
   Create a `.env` file in the root directory with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Install Firefox Browser**
   - The scraper uses Firefox with Selenium
   - Make sure Firefox is installed on your system

## Running the Workflow

1. **Scrape RSS Feed**
   ```bash
   python rss_scraper.py
   ```

2. **Scrape Articles**
   ```bash
   python batch_article_scraper.py
   ```

3. **Analyze with GPT**
   ```bash
   python gpt_article_analyzer.py
   ```

4. **Generate Articles**
   ```bash
   python article_generator.py
   ```

5. **Run the Website**
   ```bash
   cd website
   streamlit run app.py
   ```

## Directory Structure

```
.
├── rss_scraper.py           # RSS feed scraper
├── chemistry_news.json      # Scraped RSS feed data
├── batch_article_scraper.py # Article content scraper
├── scraped_articles/        # Raw scraped articles
├── gpt_article_analyzer.py  # GPT analysis script
├── gpt_processed/          # GPT-analyzed articles
├── article_generator.py     # Article generation script
├── generated_articles/     # Final generated articles
└── website/                # Streamlit web interface
    ├── app.py             # Main Streamlit application
    ├── pages/            # Additional pages
    ├── static/           # Static assets
    └── templates/        # HTML templates
```

## Important Notes

1. **Rate Limiting**:
   - The scraper includes built-in delays to respect website rate limits
   - GPT API calls are also rate-limited to avoid quota issues

2. **Error Handling**:
   - All scripts include robust error handling and logging
   - Check `scraping.log` for detailed operation logs

3. **Content Storage**:
   - Articles are stored in JSON format for easy processing
   - Generated articles are saved as Markdown files

## Troubleshooting

1. **Selenium Issues**:
   - Ensure Firefox is installed
   - Check if the correct Firefox driver is installed
   - Verify your Firefox version is compatible

2. **GPT API Issues**:
   - Verify your OpenAI API key is correct
   - Check your API quota and usage limits
   - Ensure your network can access OpenAI's API

3. **Streamlit Issues**:
   - Make sure all required packages are installed
   - Check if the port 8501 is available
   - Verify file permissions in the website directory

## Contributing

Feel free to submit issues and enhancement requests!
