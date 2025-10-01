# AI Data Pipelines

A comprehensive collection of AI data extraction and indexing pipelines. Each pipeline extracts data from a specific source and indexes it into **MinSearch** (or any other target search engine/vector database). Use these pipelines to power up your AI products with structured, searchable data.

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

### [`github-docs/`](./github-docs/)
**Extract GitHub documentation and README content for searchable knowledge bases**  
*Tech: GitHub API, BeautifulSoup, Markdown parsers → Clean documentation content*

### [`github-code/`](./github-code/)
**Analyze and index source code and Jupyter notebooks from repositories**  
*Tech: GitHub API, AST parsers, nbformat, Tree-sitter → Searchable code snippets and functions*

### [`github-api/`](./github-api/)
**Extract GitHub project metadata via REST and GraphQL APIs**  
*Tech: GitHub API, GraphQL, dlt, PyGithub → Structured project management data*

### [`website-scraper-basic/`](./website-scraper-basic/)
**Traditional web scraping for complex sites requiring custom extraction logic**  
*Tech: Beautiful Soup, Scrapy, Selenium → Clean web content with custom selectors*

### [`website-scraper-jina/`](./website-scraper-jina/)
**AI-powered content extraction using Jina's intelligent reader technology**  
*Tech: Jina Reader API → Clean content without HTML parsing complexity*

### [`wikipedia-processor/`](./wikipedia-processor/)
**Process Wikipedia XML dumps and MediaWiki exports into searchable format**  
*Tech: XML parsers, WikiTextParser, MediaWiki API → Clean article content with metadata*

### [`pdf-processor/`](./pdf-processor/)
**Extract and OCR text content from PDF documents**  
*Tech: MarkItDown, PyPDF2, Tesseract OCR → Searchable document content*

### [`audio-transcriber/`](./audio-transcriber/)
**Transcribe podcasts and audio content into searchable text**  
*Tech: OpenAI Whisper, AssemblyAI, FFmpeg → Time-stamped transcripts*

### [`slack-exporter/`](./slack-exporter/)
**Export Slack workspace conversations for team knowledge indexing**  
*Tech: Slack Web API, Slack SDK → Structured conversation data*

### [`wiki-processor/`](./wiki-processor/)
**Extract content from various wiki platforms and documentation systems**  
*Tech: Platform APIs, markup parsers, Confluence API → Unified wiki content*

### [`notion-sync/`](./notion-sync/)
**Synchronize Notion workspace pages and databases**  
*Tech: Notion API, dlt framework → Structured knowledge base content*

### [`article-indexer/`](./article-indexer/)
**Aggregate and index articles from multiple publishing platforms**  
*Tech: RSS parsers, Medium API, Newspaper3k → Normalized article content*

### [`slide-ocr/`](./slide-ocr/)
**Extract text from presentations using OCR and AI image analysis**  
*Tech: Tesseract OCR, GPT-4o-mini, python-pptx → Slide text with visual descriptions*

### [`reddit-scraper/`](./reddit-scraper/)
**Extract Reddit discussions and community conversations**  
*Tech: PRAW, Reddit API → Hierarchical discussion threads with metadata*

### [`video-processor/`](./video-processor/)
**Extract audio from videos and transcribe for content indexing**  
*Tech: FFmpeg, OpenAI Whisper, yt-dlp → Video transcripts with timestamps*

---

## 🛠️ Getting Started

1. **Choose a project** from the folders above
2. **Navigate** to the project directory
3. **Follow** the project-specific README for setup instructions
4. **Customize** the pipeline for your specific needs

## 📋 Requirements

- Python 3.8+
- Project-specific dependencies (see individual project READMEs)
- API keys for external services (when applicable)

## 🤝 Contributing

Each project is designed to be modular and extensible. Feel free to:
- Add new data sources
- Improve existing pipelines
- Submit bug fixes and enhancements

## 📄 License

See individual project folders for licensing information.
