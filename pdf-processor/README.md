# PDF Processor

Extract text and structured content from PDF documents using MarkItDown and other PDF processing tools, indexing into MinSearch.

## 📋 Overview

This pipeline processes PDF documents to extract text, metadata, and structure for searchable content indexing.

## 🎯 Data Sources

- Research papers and academic documents
- Technical documentation
- Reports and whitepapers  
- Books and e-books
- Forms and structured documents

## 🛠️ Tools & Libraries

- **MarkItDown**: Advanced PDF text extraction
- **PyPDF2/PyMuPDF**: PDF parsing libraries
- **OCR Engines**: Image-based text extraction
- **MinSearch**: Target indexing system
- **Text Processing**: Content cleaning and structuring

## 🚀 Usage

```python
from pdf_processor import PDFProcessor

processor = PDFProcessor(
    minsearch_config="config.json"
)

# Process single PDF
processor.process_pdf("document.pdf")

# Batch process directory
processor.process_directory("./pdfs/")

# Extract with OCR for scanned documents
processor.process_with_ocr("scanned_document.pdf")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "pdf_documents",
        "host": "localhost",
        "port": 9200
    },
    "processing": {
        "extract_metadata": true,
        "use_ocr": true,
        "ocr_language": "eng",
        "chunk_size": 1000,
        "overlap_size": 200,
        "min_text_length": 50
    }
}
```

## 📦 Installation

```bash
uv add PyPDF2 pymupdf markitdown minsearch pytesseract pillow
```

## 🔗 References

- [RAG Pipeline Example](https://codecut.ai/open-source-rag-pipeline-intelligent-qa-system/)

## 🔍 Use Cases

- Document search systems
- Research paper analysis
- Technical documentation indexing
- Legal document processing
- Academic content aggregation