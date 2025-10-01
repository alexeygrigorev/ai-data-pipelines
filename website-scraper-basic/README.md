# Website Scraper (Basic)

Traditional web scraping pipeline using Beautiful Soup, Scrapy, and Selenium to extract and index web content into MinSearch.

## 📋 Overview

This pipeline provides robust web scraping capabilities for sites that don't offer APIs or require complex interaction handling.

## 🎯 Data Sources

- E-commerce websites
- News and blog sites
- Forums and discussion boards
- Documentation sites
- Dynamic JavaScript applications

## 🛠️ Tools & Libraries

- **Beautiful Soup**: HTML/XML parsing
- **Scrapy**: High-performance web crawling
- **Selenium**: JavaScript-heavy sites
- **MinSearch**: Target indexing system
- **Requests**: HTTP client with session management

## 🚀 Usage

```python
from website_scraper_basic import WebScraperBasic

scraper = WebScraperBasic(
    minsearch_config="config.json",
    rate_limit=1.0  # seconds between requests
)

# Scrape single page
scraper.scrape_page("https://example.com")

# Scrape multiple pages
urls = ["https://site1.com", "https://site2.com"]
scraper.batch_scrape(urls)

# Use Selenium for JavaScript sites
scraper.scrape_with_selenium("https://spa-app.com")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "web_content",
        "host": "localhost",
        "port": 9200
    },
    "scraping": {
        "rate_limit": 1.0,
        "timeout": 30,
        "retries": 3,
        "user_agent": "WebScraperBot/1.0",
        "respect_robots_txt": true
    },
    "selenium": {
        "driver": "chrome",
        "headless": true,
        "wait_timeout": 10
    }
}
```

## 📦 Installation

```bash
uv add beautifulsoup4 scrapy selenium requests minsearch lxml
```

## 🔍 Use Cases

- Content aggregation
- Price monitoring
- News collection
- Forum discussion analysis
- Site content backup
- Competitive analysis