# Reddit Scraper

Extract and index Reddit discussions, posts, and comments from subreddits into MinSearch for community insights and content analysis.

## 📋 Overview

This pipeline extracts Reddit content including posts, comments, user interactions, and metadata for comprehensive discussion analysis and indexing.

## 🎯 Data Sources

- Subreddit posts and discussions
- Comment threads and replies
- User profiles and karma
- Post metadata (votes, awards, timestamps)
- Reddit search results
- Trending content

## 🛠️ Tools & Libraries

- **PRAW**: Python Reddit API Wrapper
- **Reddit API**: Official Reddit data access
- **MinSearch**: Target indexing system
- **Content Processing**: Text cleaning and thread structuring

## 🚀 Usage

```python
from reddit_scraper import RedditScraper

scraper = RedditScraper(
    reddit_client_id="your_client_id",
    reddit_client_secret="your_secret",
    minsearch_config="config.json"
)

# Scrape subreddit
scraper.scrape_subreddit("MachineLearning", limit=1000)

# Scrape specific post with comments
scraper.scrape_post("post_id", include_comments=True)

# Scrape multiple subreddits
subreddits = ["datascience", "artificial", "MachineLearning"]
scraper.batch_scrape_subreddits(subreddits)
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "reddit": {
        "client_id": "your_reddit_client_id",
        "client_secret": "your_reddit_client_secret",
        "user_agent": "YourBot/1.0"
    },
    "minsearch": {
        "index_name": "reddit_discussions",
        "host": "localhost",
        "port": 9200
    },
    "scraping": {
        "include_comments": true,
        "max_comment_depth": 5,
        "min_score_threshold": 1,
        "time_filter": "month",
        "sort_by": "hot"
    }
}
```

## 📦 Installation

```bash
uv add praw minsearch requests python-dotenv
```

## 🔍 Use Cases

- Community sentiment analysis
- Discussion topic discovery
- Content trend monitoring
- User behavior analysis
- Q&A data extraction
- Market research and insights