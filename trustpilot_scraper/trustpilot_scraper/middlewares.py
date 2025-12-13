# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import random
import logging


class TrustpilotScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TrustpilotScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Try to get proxy from environment variables
        self.http_proxy = os.getenv("HTTP_PROXY")
        self.https_proxy = os.getenv("HTTPS_PROXY") or self.http_proxy
        
        # Support for proxy list file
        proxy_file = os.getenv("PROXY_FILE")
        self.proxy_list = []
        
        if proxy_file and os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r') as f:
                    self.proxy_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                self.logger.info(f"Loaded {len(self.proxy_list)} proxies from {proxy_file}")
            except Exception as e:
                self.logger.error(f"Failed to load proxy file: {e}")
        
        # Support for comma-separated proxy list
        proxy_list_env = os.getenv("PROXY_LIST")
        if proxy_list_env:
            env_proxies = [p.strip() for p in proxy_list_env.split(',') if p.strip()]
            self.proxy_list.extend(env_proxies)
            self.logger.info(f"Loaded {len(env_proxies)} proxies from PROXY_LIST environment variable")
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        # Skip if proxy already set
        if "proxy" in request.meta:
            return
        
        # Check if spider has proxy parameter
        proxy = None
        if hasattr(spider, 'proxy') and spider.proxy:
            proxy = spider.proxy
            self.logger.debug(f"Using spider proxy parameter: {proxy}")
        
        # Use rotating proxy list if available
        elif self.proxy_list:
            proxy = random.choice(self.proxy_list)
            self.logger.debug(f"Using rotating proxy: {proxy}")
        
        # Fall back to environment variables
        elif request.url.startswith('https') and self.https_proxy:
            proxy = self.https_proxy
            self.logger.debug(f"Using HTTPS_PROXY: {proxy}")
        elif self.http_proxy:
            proxy = self.http_proxy
            self.logger.debug(f"Using HTTP_PROXY: {proxy}")
        
        if proxy:
            request.meta["proxy"] = proxy
            self.logger.info(f"Request to {request.url} using proxy: {proxy}")
    
    def process_exception(self, request, exception, spider):
        # Retry with different proxy if available
        if self.proxy_list and len(self.proxy_list) > 1:
            old_proxy = request.meta.get('proxy')
            # Try to use a different proxy
            available_proxies = [p for p in self.proxy_list if p != old_proxy]
            if available_proxies:
                new_proxy = random.choice(available_proxies)
                self.logger.warning(f"Proxy {old_proxy} failed, retrying with {new_proxy}")
                request.meta["proxy"] = new_proxy
                return request
        return None