import os
import openai
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def load_processed_article(file_path):
    """Load and parse a processed article file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content into sections
    sections = content.split('\n\n')
    article_info = {}
    
    for line in content.split('\n'):
        if line.startswith('Original Article Title:'):
            article_info['title'] = line.replace('Original Article Title:', '').strip()
        elif line.startswith('Original Article URL:'):
            article_info['url'] = line.replace('Original Article URL:', '').strip()
    
    # Find GPT Analysis section
    analysis_start = content.find('GPT Analysis:')
    if analysis_start != -1:
        article_info['analysis'] = content[analysis_start:].replace('GPT Analysis:', '').strip()
    
    return article_info

def generate_article(article_info):
    """Generate a new article using GPT-4"""
    prompt = f"""Based on the following analysis of a scientific research paper, write a comprehensive article that focuses on the innovation through the lens of TRIZ principles.

Title: {article_info['title']}
Original URL: {article_info['url']}
Analysis: {article_info['analysis']}

Write a well-structured article that includes:
1. An engaging title that highlights the innovation
2. An detailed introduction that sets the context and problem being solved. Talk more about the problem. Why it is a problem and what is the traditional attempt to solve it?
3. A detailed explanation of the innovative solution and its significance, how it is different and more innovative than the traditional solutions?
4. Analysis of the TRIZ principles applied in the research
5. A conclusion that emphasizes the broader impact

Format the article with appropriate sections and maintain a professional yet engaging tone.
Include references to the original research paper.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert science and technology writer specializing in innovation analysis. Write engaging articles that explain complex innovations through the lens of TRIZ principles in a way that's accessible to a technical audience."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error generating article: {str(e)}"

def save_generated_article(output_dir, title, content):
    """Save the generated article to a file"""
    # Create a safe filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    filename = f"{safe_title[:100]}.md"
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path

def main():
    # Create output directory for generated articles
    output_dir = Path("generated_articles")
    output_dir.mkdir(exist_ok=True)
    
    # Get all processed article files
    processed_dir = Path("gpt_processed")
    processed_files = sorted(processed_dir.glob("*.txt"))
    
    print(f"Found {len(processed_files)} processed articles to generate from.")
    
    # Process each article
    for i, proc_file in enumerate(processed_files, 1):
        print(f"\nProcessing file {i}/{len(processed_files)}: {proc_file.name}")
        
        # Load the processed article
        article_info = load_processed_article(proc_file)
        
        # Generate new article
        generated_content = generate_article(article_info)
        
        # Save the generated article
        output_path = save_generated_article(output_dir, article_info['title'], generated_content)
        
        print(f"Generated article saved to: {output_path}")
        
        # Add a small delay to avoid rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()
