from scrappers.spiders.generic_news_site import GenericNewsSiteSpider


class AFamilySpider(GenericNewsSiteSpider):
    name = "afamily"
    allowed_domains = ["afamily.vn"]
    start_urls = (
        'http://afamily.vn/',
    )
    ignored_urls = (
        'http://afamily.vn/video.chn',
    )

    def select_category_urls(self, selector):
        return selector.xpath('//ul[@class="menu-wrap"]/li[not(@class="first")]/a/@href').extract()

    def select_article_urls(self, selector):
        return selector.xpath('//div[@class="list-news1"]/div/a/@href').extract()

    def select_next_page_urls(self, selector):
        return selector.css('div.paging').xpath('a/@href').extract()
