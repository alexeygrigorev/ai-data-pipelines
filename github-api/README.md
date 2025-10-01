# GitHub API Data Extractor

Extract and index GitHub issues, pull requests, and project metadata into MinSearch using GitHub's REST and GraphQL APIs.

## 📋 Overview

This pipeline extracts structured data from GitHub's API endpoints and indexes it for searchable project management and analysis.

## 🎯 Data Sources

- GitHub Issues and comments
- Pull Requests and reviews
- Commits and commit messages
- GitHub Discussions
- Repository metadata and statistics
- User and organization data

## 🛠️ Tools & Libraries

- **GitHub API (REST)**: Standard API access
- **GitHub GraphQL API**: Advanced queries
- **dlt (Data Load Tool)**: Data pipeline framework
- **MinSearch**: Target indexing system
- **PyGithub**: Python GitHub API wrapper

## 🚀 Usage

```python
from github_api_extractor import GitHubAPIExtractor

extractor = GitHubAPIExtractor(
    github_token="your_token",
    minsearch_config="config.json"
)

# Extract issues and PRs
extractor.extract_issues("owner/repo")
extractor.extract_pull_requests("owner/repo")

# Extract all project data
extractor.extract_full_project("owner/repo")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "github_token": "your_github_token",
    "minsearch": {
        "index_name": "github_api_data",
        "host": "localhost",
        "port": 9200
    },
    "extraction": {
        "include_closed_issues": true,
        "include_merged_prs": true,
        "max_comments_per_issue": 100,
        "date_range": {
            "start": "2023-01-01",
            "end": "2024-12-31"
        }
    }
}
```

## 📦 Installation

```bash
uv add PyGithub dlt requests minsearch python-dotenv
```

## 🔍 Use Cases

- Issue tracking and analysis
- Pull request management
- Project health monitoring
- Developer activity analysis
- Community engagement metrics