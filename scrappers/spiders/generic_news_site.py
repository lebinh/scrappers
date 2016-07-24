from urllib.parse import urljoin

from newspaper import Article
from scrapy import Request, Spider
from scrapy.selector import Selector

from scrappers.items import NewsArticle


class GenericNewsSiteSpider(Spider):
    max_page = 100
    ignored_urls = []

    def parse(self, response):
        selector = Selector(response)
        category_urls = self.select_category_urls(selector)
        for url in category_urls:
            url = self.get_full_url(url)
            if url not in self.start_urls and url not in self.ignored_urls:
                yield Request(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        page = response.meta.get('page', 1) if response.meta else 1
        if page <= self.max_page:
            selector = Selector(response)
            article_urls = self.select_article_urls(selector)
            for url in set(article_urls):
                url = self.get_full_url(url)
                yield Request(url=url, callback=self.parse_article_page)

            next_page_urls = self.select_next_page_urls(selector)
            if next_page_urls:
                url = self.get_full_url(next_page_urls[-1])
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

    def select_category_urls(self, selector):
        raise NotImplementedError()

    def select_article_urls(self, selector):
        raise NotImplementedError()

    def select_next_page_urls(self, selector):
        raise NotImplementedError()

    def get_full_url(self, url):
        if url.startswith('http'):
            return url
        return urljoin(self.start_urls[0], url)
