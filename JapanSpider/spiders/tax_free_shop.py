# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from JapanSpider.items import TaxFreeShopItem
import re


class TaxFreeShopSpider(Spider):
    name = "tax_free_shop"
    collection_name = "tax_free_shop"
    start_urls = [
        "http://tax-freeshop.jnto.go.jp/eng/locator.php?sort=shop_name_asc&view=list",
    ]

    def parse(self, response):
        self.logger.info('Tax free shop list url: %s' % response.url)

        for shop in response.xpath('//table[@class="tbl_result"]//tr[position()>1]'):
            pass
        
        next_page = response.xpath('//a[@title="next page"]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield Request(url, self.parse)
