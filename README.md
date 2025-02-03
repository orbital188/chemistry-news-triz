# Chemistry News Analysis with TRIZ Principles

This project is an automated workflow that scrapes chemistry research articles from phys.org, analyzes them through the lens of TRIZ principles using GPT-4 or DeepSeek-Chat, and presents them in a beautiful Streamlit web interface.

## Workflow Overview

1. **RSS Feed Scraping** (`rss_scraper.py`): 
   - Fetches the latest chemistry news from RSS feed
   - Saves article metadata and links to `chemistry_news.json`

2. **Article Scraping** (`batch_article_scraper.py`):
   - Reads article links from `chemistry_news.json`
   - Uses Selenium with Firefox to scrape full article content
   - Saves individual articles to the `scraped_articles` directory

3. **AI Analysis** (`gpt_article_analyzer.py` or `deepseek_article_analyzer.py`):
   - Processes scraped articles using GPT-4 or DeepSeek-Chat
   - Analyzes innovation and TRIZ principles in each article
   - Saves analysis to the `gpt_processed` or `deepseek_processed` directory

4. **Article Generation** (`article_generator.py`):
   - Takes AI-analyzed content and generates comprehensive articles
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

2. **Virtual Environment Setup**
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**

1. **Create Environment File**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   ```

2. **Configure Environment Variables**
   Open `.env` and configure the following variables:
   ```bash
   # OpenAI Configuration (for GPT-4)
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_API_BASE=https://api.openai.com/v1

   # DeepSeek Configuration (for DeepSeek-Chat)
   DEEPSEEK_API_KEY=your_deepseek_api_key

   # Rate Limiting
   MIN_DELAY=60
   MAX_DELAY=75
   INITIAL_DELAY=5
   MAX_DELAY_INITIAL=15
   ```
   
   To get your OpenAI API key:
   1. Go to https://platform.openai.com/api-keys
   2. Create a new API key
   3. Copy the key and paste it in your `.env` file

   To get your DeepSeek API key:
   1. Visit DeepSeek's platform
   2. Create an API key
   3. Copy the key and paste it in your `.env` file

   Note: Never commit your `.env` file or share your API keys publicly.
   Example of env file:
   ```bash
   # OpenAI Configuration (for GPT-4)
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_API_BASE=https://api.openai.com/v1

   # DeepSeek Configuration (for DeepSeek-Chat)
   DEEPSEEK_API_KEY=your_deepseek_api_key

   # Rate Limiting
   MIN_DELAY=60
   MAX_DELAY=75
   INITIAL_DELAY=5
   MAX_DELAY_INITIAL=15
   ```

5. **Install Firefox Browser**
   - The scraper uses Firefox with Selenium
   - Make sure Firefox is installed on your system

   **For Ubuntu Users:**
   ```bash
   # Remove Firefox if it was installed via snap
   sudo snap remove firefox

   # Add Mozilla team PPA
   sudo add-apt-repository ppa:mozillateam/ppa

   # Install Firefox from APT
   sudo apt update
   sudo apt install firefox
   ```

6. **Install GeckoDriver (Required for Selenium)**
   
   **For Ubuntu Users:**
   ```bash
   # Install wget if not already installed
   sudo apt install wget

   # Download the latest geckodriver
   wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz

   # Extract the archive
   tar -xvzf geckodriver-v0.33.0-linux64.tar.gz

   # Make the geckodriver executable
   chmod +x geckodriver

   # Move geckodriver to /usr/local/bin
   sudo mv geckodriver /usr/local/bin/

   # Clean up the archive
   rm geckodriver-v0.33.0-linux64.tar.gz
   ```

   Note: The Firefox version installed through APT is more compatible with Selenium compared to the snap-installed version. If you experience any issues with Firefox or geckodriver, make sure you're using the APT version of Firefox.

## Running the Workflow

1. **Scrape RSS Feed**
   ```bash
   python rss_scraper.py
   ```

2. **Scrape Articles**
   ```bash
   python batch_article_scraper.py
   ```

3. **Analyze with AI**
   
   For GPT-4 analysis:
   ```bash
   python gpt_article_analyzer.py
   ```

   For DeepSeek analysis:
   ```bash
   python deepseek_article_analyzer.py
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
├── deepseek_article_analyzer.py  # DeepSeek analysis script
├── gpt_processed/          # GPT-analyzed articles
├── deepseek_processed/     # DeepSeek-analyzed articles
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

3. **DeepSeek API Issues**:
   - Verify your DeepSeek API key is correct
   - Check your API quota and usage limits
   - Ensure your network can access DeepSeek's API

4. **Streamlit Issues**:
   - Make sure all required packages are installed
   - Check if the port 8501 is available
   - Verify file permissions in the website directory
