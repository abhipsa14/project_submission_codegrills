# Project_submission_codegrills

This repository contains two Python tools designed for monitoring and extracting content related to cryptocurrencies and dark web (.onion) links:

1. **Pastebin Keyword Crawler**: Scrapes Pastebin's public archive for pastes containing crypto-related keywords or Telegram links.

   ![Screenshot From 2025-05-21 21-30-45](https://github.com/user-attachments/assets/67f0efcd-6dcb-496f-874d-7efc8857d9e9)
   ![Screenshot From 2025-05-21 21-30-55](https://github.com/user-attachments/assets/f9520c00-010d-4af9-ac06-ec39e346a0c0)


## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Pastebin Keyword Crawler](#pastebin-keyword-crawler)
  - [Features](#features)
  - [Usage](#usage)
  - [Output Format](#output-format)
- [Best Practices](#best-practices)
- [Legal Considerations](#legal-considerations)

## Requirements

- Python 3.7+
- Internet connection
- For the Telegram extractor: Telegram account and API credentials

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/project_submission_codegrills.git
   cd project_submission_codegrills
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install dependencies individually:
   ```bash
   pip install requests beautifulsoup4 telethon
   ```

## Pastebin Keyword Crawler

The Pastebin Keyword Crawler (`pastebin_keyword_crawler.py`) scrapes Pastebin's public archive for pastes containing crypto-related keywords or Telegram links and stores the results in a JSONL file.

### Features

- Scrapes Pastebin's archive to extract the latest 30 paste IDs
- Fetches content for each paste using the raw URL format
- Checks for crypto and Telegram-related keywords in paste content
- Multi-threaded processing for improved performance
- Rate limiting and request delays to avoid being blocked
- Comprehensive logging of the crawling process

### Usage

Run the script with the following command:

```bash
python pastebin_keyword_crawler.py
```

To customize the crawler, you can modify the following parameters in the script:

- `keywords`: List of keywords to search for in pastes
- `output_file`: Path to save the matching results (default: `keyword_matches.jsonl`)
- `max_workers`: Number of concurrent threads for processing (default: 5)

### Output Format

The crawler outputs results in JSONL format (one JSON object per line):

```json
{
  "source": "pastebin",
  "context": "Found crypto-related content in Pastebin paste ID abc123",
  "paste_id": "abc123",
  "url": "https://pastebin.com/raw/abc123",
  "discovered_at": "2025-05-21T10:00:00Z",
  "keywords_found": ["crypto", "bitcoin"],
  "status": "pending"
}
```

## Best Practices

- **Rate Limiting**: Both tools implement delays between requests to avoid being rate-limited or blocked
- **Error Handling**: The scripts include robust error handling for network issues and API failures
- **Logging**: Comprehensive logging helps track execution and troubleshoot issues
- **Scalability**: The Pastebin crawler uses multi-threading while the Telegram extractor uses async/await for efficient execution

## Legal Considerations

These tools are designed for educational and research purposes only. When using these tools:

- Respect Pastebin's and Telegram's Terms of Service
- Do not use these tools for any illegal activities
- Be mindful of rate limits to avoid disrupting services
- Do not access private or protected content without authorization

**Note**: While these tools extract information about .onion links, they do not directly access Tor hidden services or the dark web. Additional tools like the Tor Browser would be required to visit the extracted links.
