# Scrapy settings for trustpilot_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "trustpilot_scraper"

SPIDER_MODULES = ["trustpilot_scraper.spiders"]
NEWSPIDER_MODULE = "trustpilot_scraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en-GB,en;q=0.9',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "trustpilot_scraper.middlewares.TrustpilotScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    'trustpilot_scraper.middlewares.ProxyMiddleware': 300,
}

FAKEUSERAGENT_providers = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',
    'scrapy_fake_useragent.providers.FakerProvider',
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',
]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    "trustpilot_scraper.pipelines.TrustpilotScraperPipeline": 300,
    'trustpilot_scraper.pipelines.DuplicateFilterPipeline': 300,
    'trustpilot_scraper.pipelines.DescribeItemPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_impersonate.ImpersonateDownloadHandler",
    "https": "scrapy_impersonate.ImpersonateDownloadHandler",
}