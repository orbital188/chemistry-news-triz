import streamlit as st
import os
from pathlib import Path
import markdown
import datetime

# Set page configuration
st.set_page_config(
    page_title="Innovation & TRIZ Research News",
    page_icon="🔬",
    layout="wide"
)

# Load and apply custom CSS
def load_css():
    with open("website/static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_article_metadata(content):
    """Extract title and first paragraph as summary"""
    lines = content.split('\n')
    title = lines[0].replace('#', '').strip()
    
    # Find first paragraph for summary
    summary = ""
    for line in lines[1:]:
        if line.strip() and not line.startswith('#'):
            summary = line.strip()
            break
    
    return title, summary

def display_article(content):
    """Display full article content"""
    st.markdown(content)

def main():
    # Load custom CSS
    load_css()
    
    # Header
    st.markdown("""
        <div class="header">
            <h1>Innovation & TRIZ Research News</h1>
            <p class="subtitle">Exploring Scientific Breakthroughs Through TRIZ Principles</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get all articles
    articles_dir = Path("generated_articles")
    article_files = sorted(articles_dir.glob("*.md"), key=os.path.getmtime, reverse=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    view_mode = st.sidebar.radio("View", ["Home", "All Articles"])
    
    if view_mode == "Home":
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Featured article (most recent)
            if article_files:
                featured_content = read_markdown_file(article_files[0])
                title, summary = get_article_metadata(featured_content)
                
                st.markdown("## Featured Article")
                st.markdown(f"### {title}")
                st.markdown(summary)
                if st.button("Read Full Article", key=f"featured_{title}"):
                    st.markdown("---")
                    display_article(featured_content)
        
        with col2:
            # Latest articles sidebar
            st.markdown("## Latest Articles")
            for file in article_files[1:4]:  # Show next 3 articles
                content = read_markdown_file(file)
                title, summary = get_article_metadata(content)
                
                with st.container():
                    st.markdown(f"### {title}")
                    st.markdown(f"{summary[:150]}...")
                    if st.button("Read Full Article", key=f"latest_{title}"):
                        st.markdown("---")
                        display_article(content)
                st.markdown("---")
    
    else:  # All Articles view
        st.markdown("## All Articles")
        for file in article_files:
            content = read_markdown_file(file)
            title, summary = get_article_metadata(content)
            
            with st.expander(title):
                display_article(content)
            st.markdown("---")

if __name__ == "__main__":
    main()
