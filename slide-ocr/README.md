# Slide OCR Processor

Extract and index text content from slide decks and presentations using OCR and AI-powered image description into MinSearch.

## 📋 Overview

This pipeline processes slide presentations and images, extracting text through OCR and generating descriptions using AI models for comprehensive indexing.

## 🎯 Data Sources

- PowerPoint presentations (PPTX)
- PDF slide decks
- Google Slides exports
- Image files (PNG, JPG, SVG)
- Keynote presentations
- SlideShare content

## 🛠️ Tools & Libraries

- **OCR Engines**: Tesseract, EasyOCR
- **GPT-4o-mini**: AI-powered image description
- **python-pptx**: PowerPoint file processing
- **MinSearch**: Target indexing system
- **PIL/Pillow**: Image processing

## 🚀 Usage

```python
from slide_ocr_processor import SlideOCRProcessor

processor = SlideOCRProcessor(
    openai_api_key="your_openai_key",
    minsearch_config="config.json"
)

# Process PowerPoint file
processor.process_pptx("presentation.pptx")

# Process PDF slides
processor.process_pdf_slides("slides.pdf")

# Process individual images
processor.process_image("slide_image.png")

# Batch process directory
processor.process_directory("./presentations/")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "openai_api_key": "your_openai_api_key",
    "minsearch": {
        "index_name": "slide_content",
        "host": "localhost",
        "port": 9200
    },
    "ocr": {
        "engine": "tesseract",
        "languages": ["eng"],
        "confidence_threshold": 60
    },
    "ai_description": {
        "model": "gpt-4o-mini",
        "max_tokens": 500,
        "include_visual_elements": true
    }
}
```

## 📦 Installation

```bash
uv add pytesseract pillow python-pptx openai minsearch easyocr pdf2image
```

## 🔍 Use Cases

- Presentation content search
- Educational material indexing
- Conference slide analysis
- Visual content discovery
- Training material aggregation
- Image-based documentation processing