# CompanyProfile-Scraper

***"This repository is created for educational purposes to demonstrate web scraping techniques using Scrapy. It is not intended for commercial use or to violate any Terms of Service. The author is not responsible for any misuse of this software."***

A Scrapy-based web scraper for extracting company information and reviews from Trustpilot, organized by categories and countries.

## Features

- **Multi-country support**: Scrape data for specific countries using country codes
- **Category-based scraping**: Automatically discovers and scrapes companies across different categories and subcategories
- **Comprehensive data extraction**: Collects company details including:
  - Company name
  - Category and subcategory
  - Average review score
  - Total review count
  - Contact information (website, email, phone, address)
  - Trustpilot URL
  - Country
- **Polite scraping**: Includes rate limiting and randomized delays to respect server resources
- **Browser impersonation**: Uses scrapy-impersonate for better scraping reliability

## Installation

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/bahakarakaya/CompanyProfile-Scraper.git
cd trustpilotScraper
```

2. Install dependencies:
```bash
pip install -e .
```

Or if using uv:
```bash
uv pip install -e .
```

## Usage

### Basic Command

Navigate to the Scrapy project directory and run:

```bash
cd trustpilot_scraper
scrapy crawl trustpilot -a country=GB -o output.csv
```

### Command Parameters

- `-a country=<CODE>`: Specify the country code (e.g., GB, DE, US, FR). Defaults to GB if not specified.
- `-o <filename>`: Specify output file. Supports formats: `.json`, `.csv`, `.xml`, `.jsonl`

### Examples

Scrape UK companies and output to JSON:
```bash
scrapy crawl trustpilot -a country=GB -o output_uk.json
```

Scrape German companies and output to CSV:
```bash
scrapy crawl trustpilot -a country=DE -o output_de.csv
```

Scrape US companies with detailed logging:
```bash
scrapy crawl trustpilot -a country=US -o output_us.json --loglevel=DEBUG
```

### Proxy Usage

The scraper supports multiple proxy configuration methods:

**1. Single Proxy via Spider Parameter:**
```bash
scrapy crawl trustpilot -a country=GB -a proxy=http://proxy-server:port -o output.json
```

With authentication:
```bash
scrapy crawl trustpilot -a country=GB -a proxy=http://username:password@proxy-server:port -o output.json
```

**2. Environment Variables:**
```bash
# HTTP proxy
export HTTP_PROXY="http://username:password@proxy-server:port"
scrapy crawl trustpilot -a country=GB -o output.json

# HTTPS proxy (for HTTPS requests)
export HTTPS_PROXY="https://username:password@proxy-server:port"
scrapy crawl trustpilot -a country=GB -o output.json

# Or inline
HTTP_PROXY="http://10.10.1.10:3128" scrapy crawl trustpilot -a country=GB -o output.json
```

**3. Rotating Proxy List (via comma-separated list):**
```bash
export PROXY_LIST="http://proxy1:port,http://proxy2:port,http://proxy3:port"
scrapy crawl trustpilot -a country=GB -o output.json
```

**4. Rotating Proxy List (via file):**

Create a file `proxies.txt`:
```
http://proxy1.example.com:8080
http://username:password@proxy2.example.com:8080
http://proxy3.example.com:3128
# Comments are ignored
```

Then run:
```bash
export PROXY_FILE="proxies.txt"
scrapy crawl trustpilot -a country=GB -o output.json
```

**Proxy Features:**
- Automatic HTTPS proxy support
- Rotating proxies (randomly selected from list)
- Authentication support (username:password)
- Automatic retry with different proxy on failure
- Priority: Spider parameter > Proxy list > Environment variables

## Project Structure

```
trustpilotScraper/
├── trustpilot_scraper/          # Scrapy project root
│   ├── scrapy.cfg               # Scrapy configuration
│   ├── trustpilot_scraper/      # Python module
│   │   ├── __init__.py
│   │   ├── items.py             # Data models
│   │   ├── middlewares.py       # Custom middlewares
│   │   ├── pipelines.py         # Data processing pipelines
│   │   ├── settings.py          # Scrapy settings
│   │   └── spiders/
│   │       ├── __init__.py
│   │       └── trustpilot.py    # Main spider
│   └── output.csv               # Example output
├── check_data.py                # Data validation script
├── check_data.ipynb             # Data analysis notebook
├── main.py                      # Entry point
├── pyproject.toml               # Project metadata
└── README.md                    # This file
```

## Output Data Structure

Each scraped item contains the following fields:

| Field              | Type   | Description                          |
|--------------------|--------|--------------------------------------|
| `company_name`     | string | Name of the company                  |
| `category`         | string | Main category                        |
| `subcategory`      | string | Subcategory                          |
| `avg_review_score` | string | Average review score (e.g., "4.5")   |
| `review_count`     | string | Total number of reviews              |
| `website`          | string | Company website URL                  |
| `email`            | string | Contact email address                |
| `phone`            | string | Contact phone number                 |
| `address`          | string | Physical address                     |
| `trustpilot_url`   | string | Trustpilot profile URL               |
| `country`          | string | Country code (e.g., "GB", "DE")      |

## Configuration

### Spider Settings

Key settings in `trustpilot_scraper/settings.py`:

- `CONCURRENT_REQUESTS = 4`: Number of concurrent requests
- `DOWNLOAD_DELAY = 1`: Delay between requests (seconds)
- `RANDOMIZE_DOWNLOAD_DELAY = True`: Randomize delays for more natural behavior
- `ROBOTSTXT_OBEY = False`: Robots.txt compliance (currently disabled)
- `COOKIES_ENABLED = True`: Enable cookie handling

### Customization

You can modify the spider behavior by editing `trustpilot_scraper/spiders/trustpilot.py`:

- Limit categories to scrape: Modify line 59 (`categories[:2]`) to change the number
- Adjust pagination logic in `parse_category_pagination()`
- Customize data extraction in `parse_company_profile()`

## Dependencies

- **scrapy** (>=2.13.4): Web scraping framework
- **pandas** (>=2.3.3): Data analysis and manipulation
- **scrapy-fake-useragent** (>=1.4.4): Random user agent rotation
- **scrapy-impersonate** (>=1.6.1): Browser impersonation for better reliability

## Notes

- The scraper currently processes only the first 2 categories by default (see line 59 in `trustpilot.py`)
- Rate limiting is implemented to avoid overwhelming the server
- Some contact information fields may be empty if not available on the company's Trustpilot page
- The scraper respects pagination and will automatically follow "next page" links

## Legal & Ethical Considerations

⚠️ **Important**: 
- Always respect the website's Terms of Service
- Use reasonable rate limits to avoid server overload
- Consider the legal implications of web scraping in your jurisdiction
- This tool is for educational and research purposes only

## Troubleshooting

**Issue**: No data being scraped
- Check your internet connection
- Verify the country code is valid
- Increase logging level: `--loglevel=DEBUG`

**Issue**: Rate limiting or blocking
- Increase `DOWNLOAD_DELAY` in settings.py
- Reduce `CONCURRENT_REQUESTS`
- Check if your IP has been temporarily blocked

**Issue**: XPath errors
- The website structure may have changed
- Update XPath selectors in `trustpilot.py`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

--
