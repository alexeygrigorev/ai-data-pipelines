# AI Data Pipelines

A comprehensive collection of AI data extraction and indexing pipelines. Each pipeline extracts data from a specific source and indexes it into `minsearch` (you can replace it with any other target).

Use the code from these pipelines to power up your AI products with structured, searchable data.


## 📁 Project Structure

Each project folder contains a complete data pipeline:

- **Data extraction** scripts from specific sources
- **Processing and transformation** utilities
- **`minsearch` indexing** (easy to replace with a different target)
- **Documentation** and usage examples
- **Configuration** files and requirements


## 🔄 Pipeline Flow

Data Source → Extract → Transform → Cache → Index with minsearch (or other target)


## 🚀 Available Projects

### [`common`](./common/)

Common utilities used in many projects

- [`chunking.py`](common/chunking.py) - Chunking
- [`indexing.py`](common/indexing.py) - Indexing with minsearch
- [`interactive.py`](common/interactive.py) - Displaying results in termimal
- TODO

Dependencies (installable with `pip install` or `uv add`):

- `minsearch` for seach
- `rich` for TODO 


### [`github_docs/`](./github_docs/)

Extract GitHub documentation

* Example for https://github.com/DataTalksClub/faq
* Download a repository as an Zip archive
* Parse with frontmatter
* Optional: simple chunking

Running:

```bash
python run.py github_docs
```

Files:

* [`github.py`](github_docs/github.py) - Downloads file content from github
* [`main.py`](github_docs/main.py) - Orchestrates everything


Dependencies:

- `requests` for downloading the zip archive from GitHub
- `frontmatter` for parsing frontmatter (markdown) files
- the common module


### [`github_code/`](./github_code/)

Extracts code and jupyter notebooks

* Uses [`github.py`](github_docs/github.py) from `github_docs` to donwload the content
* Parses Jupyter notebooks (ipynb files) into md files 
* Converts code and ipynb files into md documentation with LLM
* Caches the results with [`petcache`](https://github.com/alexeygrigorev/petcache)

Running:

```bash
python run.py github_code
```

Dependencies:

- the github_docs module (for dowloading the zip with files)
- `requests` via the github_docs module
- `nbcovert` for processing notebooks
- `openai`
- the common module


### [`github_api/`](./github_api/)

Extract issues from GitHub

* Uses dlt to fetch data from GitHub API (`issues` endpoint)
* Puts data into duckdb (also serves as a cache)


```bash
python run.py github_api
```

Dependencies


- `GITHUB_API_KEY`
- `dlt[duckdb]`
- the common module


### [`website_scraper_basic/`](./website_scraper_basic/)

TODO

### [`website_scraper_jina/`](./website_scraper_jina/)

TODO


### [`wikipedia_processor/`](./wikipedia_processor/)

TODO

### [`pdf_processor/`](./pdf_processor/)

TODO

### [`audio_transcriber/`](./audio_transcriber/)

TODO


### [`slack_exporter/`](./slack_exporter/)

TODO


### [`wiki_processor/`](./wiki_processor/)

TODO


### [`notion_sync/`](./notion_sync/)

TODO (use dlt)


### [`article_indexer/`](./article_indexer/)

TODO


### [`slide_ocr/`](./slide_ocr/)

TODO


### [`reddit_scraper/`](./reddit_scraper/)

TODO

### [`video_processor/`](./video_processor/)

TODO


## 🛠️ Getting Started

1. **Choose a project** from the folders above
2. **Navigate** to the project directory
3. **Follow** the project-specific README for setup instructions
4. **Customize** the pipeline for your specific needs

## 📋 Requirements

- Python 3.10+
- Project-specific dependencies (see individual project READMEs)
- API keys for external services (when applicable)

## 🤝 Contributing

Each project is designed to be modular and extensible. Feel free to:
- Add new data sources
- Improve existing pipelines
- Submit bug fixes and enhancements
