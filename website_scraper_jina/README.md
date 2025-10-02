# Website Scraper (Jina AI)

AI-powered web content extraction using Jina Reader API to intelligently extract and index clean content into MinSearch.

## 📋 Overview

This pipeline uses Jina's AI-powered Reader API to extract clean, structured content from web pages without dealing with HTML parsing complexity.

## 🎯 Data Sources

- Blog posts and articles
- Documentation sites
- News websites
- Product pages
- Any web content with readable text

## 🛠️ Tools & Libraries

- **Jina Reader API**: AI-powered content extraction
- **MinSearch**: Target indexing system  
- **Requests**: HTTP client
- **Content Processing**: Text cleaning and structuring

## 🚀 Usage

```python
from website_scraper_jina import JinaWebScraper

scraper = JinaWebScraper(
    jina_api_key="your_jina_key",
    minsearch_config="config.json"
)

# Extract content from URL
content = scraper.extract_url("https://example.com/article")

# Process sitemap
scraper.process_sitemap("https://site.com/sitemap.xml")

# Batch processing
urls = [
    "https://site.com/page1",
    "https://site.com/page2"
]
scraper.batch_extract(urls)
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "jina_api_key": "your_jina_api_key",
    "minsearch": {
        "index_name": "jina_web_content",
        "host": "localhost", 
        "port": 9200
    },
    "extraction": {
        "rate_limit": 0.5,
        "max_tokens": 10000000,
        "include_links": true,
        "clean_html": true,
        "extract_metadata": true
    }
}
```

## 📦 Installation

```bash
uv add requests minsearch python-dotenv
```

## 🔗 API Information

- **Jina Reader API**: Free tier includes 10M tokens
- **Rate Limits**: Built-in rate limiting support
- **API Endpoint**: `https://r.jina.ai/{url}`

## 🌐 Examples

- [Live Demo](https://r.jina.ai/https://alexeygrigorev.com/aihero/)
- [Colab Notebook](https://colab.research.google.com/drive/1uoBy6_7BhxqpFQ45vuhgDDDGwstaCt4P#scrollTo=ingO3kOH_c2D)
- [DataTalks Sitemap](https://datatalks.club/sitemap.xml)

## 🔍 Use Cases

- Clean content extraction
- Article aggregation
- Documentation indexing
- Content research
- Knowledge base creation
- SEO content analysis