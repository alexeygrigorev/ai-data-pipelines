# Slack Exporter

Export and index Slack workspace conversations, channels, and messages into MinSearch for searchable team knowledge.

## 📋 Overview

This pipeline exports Slack workspace data including channels, direct messages, threads, and user interactions for knowledge base creation.

## 🎯 Data Sources

- Slack channels (public and private)
- Direct messages
- Thread conversations
- File attachments and links
- User profiles and metadata
- Slack Connect conversations

## 🛠️ Tools & Libraries

- **Slack API**: Workspace data access
- **Slack SDK**: Python client library
- **MinSearch**: Target indexing system
- **Data Processing**: Message cleaning and structuring

## 🚀 Usage

```python
from slack_exporter import SlackExporter

exporter = SlackExporter(
    slack_token="xoxb-your-token",
    minsearch_config="config.json"
)

# Export specific channels
exporter.export_channel("book-of-the-week")
exporter.export_channel("course-questions")

# Export all channels
exporter.export_all_channels()

# Export user conversations
exporter.export_user_messages("user_id")
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "slack_token": "xoxb-your-slack-bot-token",
    "minsearch": {
        "index_name": "slack_conversations",
        "host": "localhost",
        "port": 9200
    },
    "export": {
        "include_private_channels": false,
        "include_direct_messages": true,
        "include_threads": true,
        "date_range": {
            "start": "2023-01-01",
            "end": "2024-12-31"
        },
        "exclude_bots": true
    }
}
```

## 📦 Installation

```bash
uv add slack-sdk minsearch requests python-dotenv
```

## 🔍 Use Cases

- Team knowledge base creation
- Conversation search and discovery
- Project discussion analysis
- Training data for chatbots
- Historical decision tracking
- Course and community Q&A indexing

## 📝 Examples

- Book of the week channel discussions
- Course question channels
- Career advice conversations
- Technical support threads