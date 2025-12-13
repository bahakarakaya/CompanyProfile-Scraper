import scrapy
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from trustpilot_scraper.items import TrustpilotScraperItem
import re
import logging


class TrustpilotSpider(scrapy.Spider):
    name = "trustpilot"
    allowed_domains = ["www.trustpilot.com"]

    def __init__(self, country: str = "GB", *args, **kwargs):
        """
        example: scrapy crawl trustpilot -a country=DE -o output_de.json
        """

        super(TrustpilotSpider, self).__init__(*args, **kwargs)
        self.country_code = country.upper()
        self.base_url = "https://www.trustpilot.com"

        self.start_urls = [f"{self.base_url}/categories?country={self.country_code}"]

    
    def add_country_param(self, url):
        """Adds country parameter to the URL."""
        if not url: return None

        #for relative URLs
        if not url.startswith('http'):
            url = self.base_url + url if url.startswith('/') else f"{self.base_url}/{url}"

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['country'] = [self.country_code]

        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed_url._replace(query=new_query)
        return urlunparse(new_parsed)


    def parse(self, response):
        """Main and subcategory extraction from the categories page."""

        categories = response.xpath('//div[contains(@class, "CDS_Card")]')
        
        category_names = [
            cat.xpath('.//h2/text()').get() 
            for cat in categories
        ]
        category_names = [
            name.replace("&", "_").replace(",", "_").replace(" ", "").lower() 
            for name in category_names
        ]

        for cat_idx, cat_selector in enumerate(categories[:2]):
            subcategory_links = cat_selector.xpath('./ul//a[contains(@href, "/categories/")]/@href')
            cat_name = category_names[cat_idx]

            for subcat_link in subcategory_links:
                subcat_link = subcat_link.get()
                
                full_url = self.add_country_param(subcat_link)
                yield response.follow(full_url, callback=self.parse_category_pagination, meta={"category_name": cat_name})


    def parse_category_pagination(self, response):
        """Pagination for category and company pages."""

        company_links = response.xpath('//a[contains(@href, "/review")]/@href').getall()

        try:
            path = urlparse(response.url).path  # example: /categories/furniture
            if '/categories/' in path:
                current_subcategory = path.split('/categories/')[1].split('/')[0]
            else:
                current_subcategory = "unknown_subcategory"
        except Exception as e:
            raise Exception(f"CATEGORY_ERROR: {e}")

        for link in company_links:
            yield response.follow(link, callback=self.parse_company_profile, meta={'category_name': response.meta.get('category_name'), 'subcategory': current_subcategory})
        
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            next_page = self.add_country_param(next_page)
            yield response.follow(next_page, callback=self.parse_category_pagination, meta={'category_name': response.meta.get('category_name'), 'subcategory': current_subcategory})

    

    def parse_company_profile(self, response):
        """Company profile and reviews extraction."""

        item = TrustpilotScraperItem()
        try:
            item['company_name'] = response.xpath('//h1//span[contains(@class, "title_displayName")]/text()').get().strip()
            item['category'] = response.meta.get('category_name')
            item['subcategory'] = response.meta.get('subcategory')

            avg = response.xpath('//p[contains(@class, "trustScore")]/text()').get()
            item['avg_review_score'] = avg.strip() if avg else None
            item['review_count'] = response.xpath('//span[contains(@class, "reviewsAndRating")]/text()').getall()[-1].replace(',', '').strip()
            
            # CONTACT INFO
            item['website'] = None
            item['phone'] = None
            item['email'] = None
            item['address'] = None

            contacts_info_sel = response.xpath('//ul[contains(@class, "itemsColumn")]/li')
            website = None
            phone = None
            email = None
            address = None
            for li in contacts_info_sel:
                hrefs = li.xpath('.//a/@href').getall()
                if hrefs:
                    for href in hrefs:
                        if not href:
                            continue
                        href = href.strip()
                        if href.startswith('mailto:') and not email:
                            email = href.split(':', 1)[1].split('?')[0].strip()
                        elif href.startswith('tel:') and not phone:
                            phone = href.split(':', 1)[1].strip()
                        else:
                            # normalize relative urls and skip trustpilot links
                            link = response.urljoin(href)
                            if 'trustpilot.com' in link:
                                continue
                            if not website:
                                website = link.split('?')[0].strip()
                else:
                    # possible address block
                    paragraph = li.xpath('.//p/text()').get()
                    if paragraph:
                        address = paragraph.strip()
            
            item['website'] = website
            item['phone'] = phone
            item['email'] = email
            item['address'] = address
                        
            item['trustpilot_url'] = response.url
            item['country'] = self.country_code
        except Exception as e:
            print(f"Error parsing company profile: {e}")
            raise

        yield item
        
        