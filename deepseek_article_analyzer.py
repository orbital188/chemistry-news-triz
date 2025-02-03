import os
import json
from openai import OpenAI
from datetime import datetime
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with DeepSeek configuration
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

def create_output_directory():
    """Create the output directory if it doesn't exist"""
    output_dir = Path("deepseek_processed")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def load_article(file_path):
    """Load article from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_article_with_deepseek(article):
    """Analyze an article using DeepSeek API"""
    prompt = f"""Article Title: {article['title']}
Article Content: {article['content']}
Article URL: {article['url']}

Rewrite the articles in the lens of analysis on TRIZ principles following the guidance:
What is the main idea of the research work? Explain how it is innovative. 
If apply TRIZ principles reflected in this work, which TRIZ principles have been used. Explain. 
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # Using DeepSeek-V3 model
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert in analyzing scientific research through the lens of TRIZ principles. Provide detailed analysis of research papers focusing on innovation and TRIZ principles application."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing article: {str(e)}"

def save_analysis(output_dir, article, analysis):
    """Save the DeepSeek analysis to a file"""
    # Create a safe filename from the article title
    safe_title = "".join(c for c in article['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{safe_title[:100]}.txt"
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Original Article Title: {article['title']}\n")
        f.write(f"Original Article URL: {article['url']}\n")
        f.write(f"Publication Date: {article['publication_date']}\n")
        f.write("\nOriginal Content:\n")
        f.write(article['content'])
        f.write("\n\nDeepSeek Analysis:\n")
        f.write(analysis)

def main():
    # Create output directory
    output_dir = create_output_directory()
    
    # Get all article files from scraped_articles directory
    articles_dir = Path("scraped_articles")
    article_files = sorted(articles_dir.glob("article_*.json"))
    
    # Process each article
    for i, article_file in enumerate(article_files, 1):
        print(f"\nProcessing article {i}/{len(article_files)}: {article_file.name}")
        
        # Load article
        article = load_article(article_file)
        
        # Analyze with DeepSeek
        analysis = analyze_article_with_deepseek(article)
        
        # Save the analysis
        save_analysis(output_dir, article, analysis)
        
        # Add a small delay to avoid rate limits
        time.sleep(1)
        
        print(f"Analysis completed and saved for: {article['title']}")

if __name__ == "__main__":
    main()
