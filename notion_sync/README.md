# Notion Sync

Extract and index Notion workspace content including pages, databases, and blocks into MinSearch.

## 📋 Overview

This pipeline syncs Notion workspace content, extracting pages, database records, and structured blocks for searchable indexing.

## 🎯 Data Sources

- Notion pages and subpages
- Notion databases and records
- Block content (text, code, embeds)
- Page properties and metadata
- Comments and discussions

## 🛠️ Tools & Libraries

- **Notion API**: Official workspace access
- **dlt (Data Load Tool)**: Data pipeline framework
- **MinSearch**: Target indexing system
- **Content Processing**: Block and page structure handling

## 🚀 Usage

```python
from notion_sync import NotionSync

sync = NotionSync(
    notion_token="secret_your_token",
    minsearch_config="config.json"
)

# Sync entire workspace
sync.sync_workspace()

# Sync specific database
sync.sync_database("database_id")

# Sync page hierarchy
sync.sync_page_tree("page_id")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "notion_token": "secret_your_notion_integration_token",
    "minsearch": {
        "index_name": "notion_content",
        "host": "localhost",
        "port": 9200
    },
    "sync": {
        "include_archived": false,
        "sync_comments": true,
        "max_depth": 10,
        "exclude_databases": [],
        "batch_size": 100
    }
}
```

## 📦 Installation

```bash
uv add notion-client dlt minsearch requests python-dotenv
```

## 🔍 Use Cases

- Personal knowledge management
- Team documentation indexing
- Project management data extraction
- Note and research aggregation
- Content migration and backup
- Cross-workspace search