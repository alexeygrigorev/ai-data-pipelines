# Audio Transcriber

Download, transcribe, and index audio content from podcasts, RSS feeds, and audio files into MinSearch.

## 📋 Overview

This pipeline handles the complete audio processing workflow: download → transcribe → process → index for searchable audio content.

## 🎯 Data Sources

- Podcast RSS feeds
- Audio files (MP3, WAV, M4A)
- YouTube audio tracks
- Webinar recordings
- Voice memos and interviews

## 🛠️ Tools & Libraries

- **Whisper**: OpenAI's speech-to-text model
- **AssemblyAI**: Cloud transcription service
- **FFmpeg**: Audio processing and conversion
- **MinSearch**: Target indexing system
- **RSS Parsers**: Podcast feed processing

## 🚀 Usage

```python
from audio_transcriber import AudioTranscriber

transcriber = AudioTranscriber(
    minsearch_config="config.json"
)

# Process single audio file
transcriber.transcribe_file("podcast_episode.mp3")

# Process RSS feed
transcriber.process_rss_feed("https://podcast.com/rss")

# Batch process directory
transcriber.process_directory("./audio_files/")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "audio_transcripts",
        "host": "localhost",
        "port": 9200
    },
    "transcription": {
        "service": "whisper",
        "model": "base",
        "language": "en",
        "chunk_duration": 300,
        "assemblyai_api_key": "your_key_if_using_assemblyai"
    },
    "audio": {
        "sample_rate": 16000,
        "format": "wav",
        "normalize_audio": true
    }
}
```

## 📦 Installation

```bash
uv add openai-whisper assemblyai minsearch ffmpeg-python feedparser requests
```

## 🔍 Use Cases

- Podcast content search
- Meeting transcription indexing
- Educational content processing
- Interview analysis
- Audio content discovery
- Voice note organization