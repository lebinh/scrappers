from scrappers.spiders.generic_news_site import GenericNewsSiteSpider


class Kenh14Spider(GenericNewsSiteSpider):
    name = "kenh14"
    allowed_domains = ["kenh14.vn"]
    start_urls = (
        'http://www.kenh14.vn/',
    )
    ignored_urls = (
        'http://kenh14.vn/video.chn',
    )

    def select_category_urls(self, selector):
        return selector.xpath('//li[@class="kmm-category "]/a/@href').extract()

    def select_article_urls(self, selector):
        return selector.xpath('//a[@rel="newstype-title"]/@href').extract()

    def select_next_page_urls(self, selector):
        return selector.css('li.next-page').xpath('a/@href').extract()
