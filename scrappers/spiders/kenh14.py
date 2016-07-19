# -*- coding: utf-8 -*-
import scrapy


class K14Spider(scrapy.Spider):
    name = "kenh14"
    allowed_domains = ["kenh14.vn"]
    start_urls = (
        'http://www.kenh14.vn/',
    )

    def parse(self, response):
        pass
