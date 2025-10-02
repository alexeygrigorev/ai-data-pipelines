# AI Data Pipelines

A comprehensive collection of AI data extraction and indexing pipelines. Each pipeline extracts data from a specific source and indexes it into `minsearch` (you can replace it with any other target).

Use the code from these pipelines to power up your AI products with structured, searchable data.

## 📁 Project Structure

Each project folder contains a complete data pipeline:
- **Data extraction** scripts from specific sources
- **Processing and transformation** utilities
- **MinSearch indexing** (configurable for other targets)
- **Documentation** and usage examples
- **Configuration** files and requirements


## 🔄 Pipeline Flow

Data Source → Extract → Transform → Index with minsearch (or other target)


## 🚀 Available Projects

### [`github_docs/`](./github_docs/)
**Extract GitHub documentation and README content for searchable knowledge bases**  
*Tech: GitHub API, BeautifulSoup, Markdown parsers → Clean documentation content*

### [`github_code/`](./github_code/)
**Analyze and index source code and Jupyter notebooks from repositories**  
*Tech: GitHub API, AST parsers, nbformat, Tree-sitter → Searchable code snippets and functions*

### [`github_api/`](./github_api/)
**Extract GitHub project metadata via REST and GraphQL APIs**  
*Tech: GitHub API, GraphQL, dlt, PyGithub → Structured project management data*

### [`website_scraper_basic/`](./website_scraper_basic/)
**Traditional web scraping for complex sites requiring custom extraction logic**  
*Tech: Beautiful Soup, Scrapy, Selenium → Clean web content with custom selectors*

### [`website_scraper_jina/`](./website_scraper_jina/)
**AI-powered content extraction using Jina's intelligent reader technology**  
*Tech: Jina Reader API → Clean content without HTML parsing complexity*

### [`wikipedia_processor/`](./wikipedia_processor/)
**Process Wikipedia XML dumps and MediaWiki exports into searchable format**  
*Tech: XML parsers, WikiTextParser, MediaWiki API → Clean article content with metadata*

### [`pdf_processor/`](./pdf_processor/)
**Extract and OCR text content from PDF documents**  
*Tech: MarkItDown, PyPDF2, Tesseract OCR → Searchable document content*

### [`audio_transcriber/`](./audio_transcriber/)
**Transcribe podcasts and audio content into searchable text**  
*Tech: OpenAI Whisper, AssemblyAI, FFmpeg → Time-stamped transcripts*

### [`slack_exporter/`](./slack_exporter/)
**Export Slack workspace conversations for team knowledge indexing**  
*Tech: Slack Web API, Slack SDK → Structured conversation data*

### [`wiki_processor/`](./wiki_processor/)
**Extract content from various wiki platforms and documentation systems**  
*Tech: Platform APIs, markup parsers, Confluence API → Unified wiki content*

### [`notion_sync/`](./notion_sync/)
**Synchronize Notion workspace pages and databases**  
*Tech: Notion API, dlt framework → Structured knowledge base content*

### [`article_indexer/`](./article_indexer/)
**Aggregate and index articles from multiple publishing platforms**  
*Tech: RSS parsers, Medium API, Newspaper3k → Normalized article content*

### [`slide_ocr/`](./slide_ocr/)
**Extract text from presentations using OCR and AI image analysis**  
*Tech: Tesseract OCR, GPT-4o-mini, python-pptx → Slide text with visual descriptions*

### [`reddit_scraper/`](./reddit_scraper/)
**Extract Reddit discussions and community conversations**  
*Tech: PRAW, Reddit API → Hierarchical discussion threads with metadata*

### [`video_processor/`](./video_processor/)
**Extract audio from videos and transcribe for content indexing**  
*Tech: FFmpeg, OpenAI Whisper, yt-dlp → Video transcripts with timestamps*

---

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
