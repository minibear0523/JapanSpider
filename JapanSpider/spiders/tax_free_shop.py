# -*- coding: utf-8 -*-
import scrapy


class TaxFreeShopSpider(scrapy.Spider):
    name = "tax_free_shop"
    allowed_domains = ["jnto.go.jp"]
    start_urls = (
        'http://www.jnto.go.jp/',
    )

    def parse(self, response):
        pass
