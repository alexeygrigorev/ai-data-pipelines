# GitHub Documentation Extractor

Extract and index GitHub documentation, README files, and wiki pages into MinSearch.

## 📋 Overview

This pipeline extracts documentation content from GitHub repositories and indexes it for searchable AI applications.

## 🎯 Data Sources

- Repository README files
- GitHub wiki pages  
- Documentation folders (`/docs`, `/documentation`)
- Markdown files in repositories
- GitHub Pages content

## 🛠️ Tools & Libraries

- **GitHub API**: Repository and content access
- **Requests**: HTTP client for API calls
- **MinSearch**: Target indexing system
- **Markdown Parser**: Content processing
- **BeautifulSoup**: HTML content extraction

## 🚀 Usage

```python
from github_docs_extractor import GitHubDocsExtractor

extractor = GitHubDocsExtractor(
    github_token="your_token",
    minsearch_config="config.json"
)

# Extract from specific repository
extractor.extract_repo_docs("owner/repo")

# Extract from multiple repositories
repos = ["owner/repo1", "owner/repo2"]
extractor.batch_extract(repos)
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "github_token": "your_github_token",
    "minsearch": {
        "index_name": "github_docs",
        "host": "localhost",
        "port": 9200
    },
    "extraction": {
        "include_wikis": true,
        "include_readme": true,
        "file_extensions": [".md", ".rst", ".txt"]
    }
}
```

## 📦 Installation

```bash
uv add requests beautifulsoup4 minsearch
```

## 🔍 Use Cases

- Documentation search engines
- Developer knowledge bases
- Code documentation analysis
- Project documentation aggregation