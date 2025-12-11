# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrustpilotScraperItem(scrapy.Item):
    company_name = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    avg_review_score = scrapy.Field()
    review_count = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    trustpilot_url = scrapy.Field()
    country = scrapy.Field()
