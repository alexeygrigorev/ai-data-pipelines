# Wiki Processor

Extract and index content from various wiki platforms and documentation sites into MinSearch.

## 📋 Overview

This pipeline processes content from different wiki platforms, converting wiki markup to searchable text and extracting structured information.

## 🎯 Data Sources

- MediaWiki installations
- Confluence spaces
- Notion wiki pages
- GitBook documentation
- Custom wiki platforms
- Documentation sites

## 🛠️ Tools & Libraries

- **Wiki APIs**: Platform-specific content access
- **Markup Parsers**: Wiki syntax conversion
- **MinSearch**: Target indexing system
- **Content Processors**: Text cleaning and structuring

## 🚀 Usage

```python
from wiki_processor import WikiProcessor

processor = WikiProcessor(
    minsearch_config="config.json"
)

# Process MediaWiki site
processor.process_mediawiki("https://wiki.example.com")

# Process Confluence space
processor.process_confluence(
    url="https://company.atlassian.net",
    space_key="DEV"
)

# Process custom wiki
processor.process_custom_wiki("https://docs.example.com")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "wiki_content",
        "host": "localhost",
        "port": 9200
    },
    "platforms": {
        "mediawiki": {
            "api_endpoint": "/api.php",
            "include_categories": true
        },
        "confluence": {
            "username": "your_username",
            "api_token": "your_token"
        }
    },
    "processing": {
        "min_content_length": 50,
        "extract_links": true,
        "preserve_structure": true
    }
}
```

## 📦 Installation

```bash
uv add requests minsearch wikitextparser atlassian-python-api beautifulsoup4
```

## 🔍 Use Cases

- Documentation aggregation
- Knowledge base migration
- Content discovery systems
- Cross-platform wiki search
- Documentation backup and indexing