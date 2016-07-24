from scrappers.spiders.generic_news_site import GenericNewsSiteSpider


class VnexpressSpider(GenericNewsSiteSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = (
        'http://www.vnexpress.net/',
    )
    ignored_urls = (
        'http://raovat.vnexpress.net',
        'http://video.vnexpress.net'
    )

    def select_category_urls(self, selector):
        return selector.xpath('//ul[@id="menu_web"]//a/@href').extract()

    def select_article_urls(self, selector):
        return selector.css('a.txt_link').xpath('@href').extract()

    def select_next_page_urls(self, selector):
        return selector.css('a.pagination_btn').xpath('@href').extract()
