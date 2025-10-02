# Video Processor

Extract audio from videos, transcribe speech content, and index video metadata and transcripts into MinSearch.

## 📋 Overview

This pipeline processes video files by extracting audio tracks, transcribing speech content, and creating searchable indexes of video content.

## 🎯 Data Sources

- Local video files (MP4, AVI, MOV, MKV)
- YouTube videos and playlists
- Vimeo content
- Educational video platforms
- Webinar recordings
- Conference presentations

## 🛠️ Tools & Libraries

- **FFmpeg**: Video/audio processing and extraction
- **Whisper**: Speech-to-text transcription
- **yt-dlp**: YouTube and video platform downloads
- **MinSearch**: Target indexing system
- **Video Processing**: Metadata extraction and frame analysis

## 🚀 Usage

```python
from video_processor import VideoProcessor

processor = VideoProcessor(
    minsearch_config="config.json"
)

# Process local video file
processor.process_video("lecture.mp4")

# Process YouTube video
processor.process_youtube_video("https://youtube.com/watch?v=abc123")

# Process entire playlist
processor.process_youtube_playlist("playlist_id")

# Batch process directory
processor.process_directory("./videos/")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "minsearch": {
        "index_name": "video_content",
        "host": "localhost",
        "port": 9200
    },
    "video_processing": {
        "extract_audio_format": "wav",
        "audio_sample_rate": 16000,
        "video_quality": "720p",
        "extract_thumbnails": true
    },
    "transcription": {
        "model": "base",
        "language": "en",
        "chunk_duration": 300
    }
}
```

## 📦 Installation

```bash
uv add ffmpeg-python openai-whisper yt-dlp minsearch pillow
```

## 📋 Pipeline Flow

```
Video File → FFmpeg (Audio Extraction) → Whisper (Transcription) → MinSearch (Indexing)
```

## 🔍 Use Cases

- Educational content indexing
- Conference video search
- Podcast video processing
- Training material organization
- Video content discovery
- Accessibility transcript generation