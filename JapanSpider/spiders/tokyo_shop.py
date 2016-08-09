# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from JapanSpider.items import ShopItem


class TokyoShopSpider(Spider):
    name = "tokyo_shop"
    collection_name = "shop"
    allowed_domains = ["dongjinggonglue.com"]
    start_urls = (
        'http://www.dongjinggonglue.com/gouwu/dianpu/',
    )

    def parse(self, response):
        for shop in response.xpath('//p[@class="equalChildTxt"]/a/@href'):
            url = response.urljoin(shop.extract())
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        self.logger.info(response.url)
        item = ShopItem()
        item['name'] = response.xpath('//h1[@class="heading01"]/em/text()').extract()[0]
        try:
            item['name_en'] = response.xpath('//h1[@class="heading01"]/em/span/text()').extract()[0]
        except Exception as e:
            self.logger.error(e)
            item['name_en'] = ""

        item['description'] = response.xpath('//div[@class="txt"]/p/text()').extract()[0]

        try:
            highlights = []
            for h in response.xpath('//div[@class="txt"]/h4[@class="heading04"]/em/text()'):
                if h.extract().strip() != "":
                    highlights.append(h.extract().strip())
            item['highlights'] = highlights
        except Exception as e:
            item['highlights'] = []

        for info in response.xpath('//table[@class="table01"]/tr'):
            k = info.css('.type01::text').extract()
            v = info.xpath('./td/text()').extract()
            if k == u'地址':
                item['address'] = '\n'.join(v)
            elif k == u'电话':
                item['telephone'] = ''.join(v)
            elif k == u'营业时间':
                item['open_time'] = ''.join(v)
            elif k == u'休息日':
                item['off_day'] = ''.join(v)
            elif k == u'免费Wifi':
                item['free_wifi'] = (v[0] == u'有')
            elif k == u'中文服务':
                service_lst = []
                for s in v:
                    service_lst.append(s.strip())
                item['service'] = service_lst
            elif k == u'官方网站':
                item['website'] = ''.join(v)
            elif k == '刷卡':
                item['credit_card'] = ''.join(v)
            elif k == '其他':
                item['other'] = ''.join(v)

        try:
            item['traffic'] = response.xpath(u'//span[text()="乘车方式"]//../text()').extract()[1].strip()
        except Exception, e:
            self.logger.error('无法获取交通方式 %s' % e)
            item['traffic'] = ""

        yield item
        
