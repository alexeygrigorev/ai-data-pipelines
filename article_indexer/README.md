# Article Indexer

Extract and index articles and blog posts from multiple sources, creating a searchable content repository in MinSearch.

## 📋 Overview

This pipeline aggregates articles from various sources, processes the content for consistency, and indexes it for comprehensive search capabilities.

## 🎯 Data Sources

- News websites and RSS feeds
- Blog platforms (Medium, Substack, WordPress)
- Academic article repositories
- Company blogs and announcements
- Newsletter archives
- Content aggregation platforms

## 🛠️ Tools & Libraries

- **RSS/Atom Parsers**: Feed processing
- **Web Scrapers**: Direct article extraction
- **MinSearch**: Target indexing system
- **Content Processing**: Text cleaning and deduplication
- **API Clients**: Platform-specific access

## 🚀 Usage

```python
from article_indexer import ArticleIndexer

indexer = ArticleIndexer(
    minsearch_config="config.json"
)

# Index RSS feed
indexer.index_rss_feed("https://blog.example.com/rss")

# Index specific article
indexer.index_article("https://medium.com/@author/article")

# Batch index multiple sources
sources = [
    "https://blog1.com/rss",
    "https://blog2.com/feed"
]
indexer.batch_index(sources)
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "articles",
        "host": "localhost",
        "port": 9200
    },
    "sources": {
        "rss_feeds": [
            "https://blog.example.com/rss"
        ],
        "medium_publications": [
            "publication-name"
        ]
    },
    "processing": {
        "deduplicate": true,
        "min_article_length": 200,
        "extract_summary": true,
        "categorize": true
    }
}
```

## 📦 Installation

```bash
uv add feedparser requests beautifulsoup4 minsearch newspaper3k
```

## 🔍 Use Cases

- Content research and discovery
- News aggregation systems
- Academic literature indexing
- Competitive content analysis
- Knowledge base creation
- Multi-source Q&A systems