# Wikipedia Processor

Extract and process Wikipedia dumps and MediaWiki exports, converting them into searchable format for MinSearch indexing.

## 📋 Overview

This pipeline processes Wikipedia dump files and other MediaWiki exports, extracting clean article content and metadata for indexing.

## 🎯 Data Sources

- Wikipedia XML dumps
- MediaWiki exports
- Wikidata entities
- Custom wiki installations
- Wiki subsets and categories

## 🛠️ Tools & Libraries

- **XML Parsers**: Process Wikipedia dump format
- **MediaWiki API**: Live wiki content access
- **MinSearch**: Target indexing system
- **Custom Converters**: Wiki markup to text conversion

## 🚀 Usage

```python
from wikipedia_processor import WikipediaProcessor

processor = WikipediaProcessor(
    minsearch_config="config.json"
)

# Process Wikipedia dump
processor.process_dump("enwiki-latest-pages-articles.xml.bz2")

# Process specific categories
processor.process_category("Machine Learning")

# Convert MediaWiki export
processor.convert_mediawiki_export("export.xml")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "wikipedia_content",
        "host": "localhost",
        "port": 9200
    },
    "processing": {
        "languages": ["en", "es", "fr"],
        "min_article_length": 100,
        "exclude_redirects": true,
        "include_categories": true,
        "max_articles": 1000000
    }
}
```

## 📦 Installation

```bash
uv add requests minsearch lxml wikitextparser
```

## 🔗 References

- [MediaWiki Transfer Script](https://github.com/alexeygrigorev/mlwiki.org/blob/main/transfer.py)
- Wikipedia dump downloads: [dumps.wikimedia.org](https://dumps.wikimedia.org/)

## 🔍 Use Cases

- Knowledge base creation
- Educational content indexing
- Research article collection
- Multi-language content processing
- Historical data analysis