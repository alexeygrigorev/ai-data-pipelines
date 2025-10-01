# GitHub Code & Notebook Extractor

Extract and index source code and Jupyter notebooks from GitHub repositories into MinSearch.

## 📋 Overview

This pipeline extracts code files and Jupyter notebooks from GitHub repositories, processes them for searchability, and indexes the content.

## 🎯 Data Sources

- Python, JavaScript, Java, and other source code files
- Jupyter notebooks (.ipynb files)
- Code documentation and comments
- Function and class definitions
- Repository structure and metadata

## 🛠️ Tools & Libraries

- **GitHub API**: Repository access
- **AST Parsers**: Code structure analysis
- **nbformat**: Jupyter notebook processing
- **MinSearch**: Target indexing system
- **Tree-sitter**: Multi-language code parsing

## 🚀 Usage

```python
from github_code_extractor import GitHubCodeExtractor

extractor = GitHubCodeExtractor(
    github_token="your_token",
    minsearch_config="config.json"
)

# Extract code from repository
extractor.extract_repo_code("owner/repo")

# Extract specific file types
extractor.extract_notebooks("owner/repo")
extractor.extract_python_files("owner/repo")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "github_token": "your_github_token",
    "minsearch": {
        "index_name": "github_code",
        "host": "localhost",
        "port": 9200
    },
    "extraction": {
        "languages": ["python", "javascript", "java", "go"],
        "include_notebooks": true,
        "max_file_size": "1MB",
        "exclude_patterns": ["node_modules/", "__pycache__/"]
    }
}
```

## 📦 Installation

```bash
uv add requests nbformat tree-sitter minsearch ast
```

## 🔍 Use Cases

- Code search engines
- Function and class discovery
- Notebook content analysis
- Code documentation systems
- Programming pattern analysis