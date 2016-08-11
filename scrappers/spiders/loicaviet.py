import string

from scrapy import Selector

from scrappers.spiders.generic_news_site import GenericNewsSiteSpider
from scrappers.items import Lyrics


class LoicavietSpider(GenericNewsSiteSpider):
    name = "loicaviet"
    allowed_domains = ["loicaviet.com"]
    start_urls = ['https://loicaviet.com/ca-si?alphabet=' + c for c in string.ascii_lowercase]
    ignored_urls = []

    def select_category_urls(self, selector):
        return selector.xpath('//div[@id="w0"]/a/@href').extract()

    def select_article_urls(self, selector):
        return selector.xpath('//div[@id="w0"]/a/@href').extract()

    def select_next_page_urls(self, selector):
        return []

    @staticmethod
    def parse_article_page(response):
        selector = Selector(response)
        title = selector.xpath('//div[@class="row"]//h1/text()').extract()
        text = selector.xpath('//div[@class="row"]/div/div/text()').extract()
        if title and text:
            item = Lyrics()
            item['title'] = title[0].strip()
            item['text'] = '. '.join(line.strip() for line in text if line.strip())
            yield item
