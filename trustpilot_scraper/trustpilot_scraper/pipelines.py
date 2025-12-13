# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import logging


class TrustpilotScraperPipeline:
    def process_item(self, item, spider):
        return item


class DuplicateFilterPipeline:
    def __init__(self):
        self.urls_seen = set()

        def process_item(self, item, spider):
            unique_url = item['trustpilot_url'].strip().rstrip("/")

            if unique_url in self.urls_seen:
                raise DropItem(f"Duplicate data removed: {item['company_name']}")
            else:
                self.urls_seen.add(unique_url)
                return item
                

class DescribeItemPipeline:
    """A pipeline that describes unique items."""
    def __init__(self) -> None:
        self.categories = set()
        self.subcategories = set()

    def process_item(self, item, spider):
        category = item.get('category')
        subcategory = item.get('subcategory')
        if category:
            self.categories.add(category)
        if subcategory:
            self.subcategories.add(subcategory)
        return item
    
    def close_spider(self, spider):
        logging.info("------- SCRAPING SUMMARY -------")
        logging.info(f"Total unique categories scraped: {len(self.categories)}")
        logging.info(f"Categories: {self.categories}")
        logging.info(f"Total unique subcategories scraped: {len(self.subcategories)}")
        logging.info(f"Subcategories: {self.subcategories}")