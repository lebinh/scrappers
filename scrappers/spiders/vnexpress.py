# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from newspaper import Article
from scrapy import Request, Spider
from scrapy.selector import Selector

from scrappers.items import NewsArticle

MAX_PAGES = 10


class VnexpressSpider(Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = (
        'http://www.vnexpress.net/',
    )
    ignored_urls = (
        'http://raovat.vnexpress.net',
        'http://video.vnexpress.net'
    )

    def parse(self, response):
        selector = Selector(response)
        category_urls = selector.xpath('//ul[@id="menu_web"]//a/@href').extract()
        for url in category_urls:
            url = self.get_full_url(url)
            if url not in self.start_urls and url not in self.ignored_urls:
                yield Request(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        page = response.meta.get('page', 1) if response.meta else 1
        if page <= MAX_PAGES:
            selector = Selector(response)
            article_urls = selector.css('a.txt_link').xpath('@href').extract()
            for url in set(article_urls):
                url = self.get_full_url(url)
                yield Request(url=url, callback=self.parse_article_page)

            next_page_urls = selector.css('a.pagination_btn').xpath('@href').extract()
            if next_page_urls:
                url = self.get_full_url(next_page_urls[0])
                yield Request(url=url, callback=self.parse_category_page,
                              meta={'page': page + 1})

    @staticmethod
    def parse_article_page(response):
        article = Article(url=response.request.url)
        article.set_html(response.text)
        article.parse()
        if article.title and article.text:
            item = NewsArticle()
            item['title'] = article.title
            item['text'] = article.text
            yield item

    def get_full_url(self, url):
        if url.startswith('http'):
            return url
        return urljoin(self.start_urls[0], url)
