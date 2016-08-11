# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from JapanSpider.items import RestaurantItem
from datetime import datetime
import re


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class RestaurantTripAdvisorSpider(Spider):
    name = "restaurant_trip_advisor"
    collection_name = "restaurant"
    allowed_domains = ["tripadvisor.cn"]
    start_urls = (
        'http://www.tripadvisor.cn/Restaurants-g298184-Tokyo_Tokyo_Prefecture_Kanto.html#EATERY_OVERVIEW_BOX',
    )

    def parse(self, response):
        self.logger.info("Restaurant list url: %s" % response.url)
        for title in response.xpath('//h3[@class="title"]/a/@href').extract():
            url = response.urljoin(title)
            yield Request(url, self.parse_restaurant)

        next_page = response.xpath('//div[@class="unified pagination js_pageLinks"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[-1].extract())
            yield Request(url, self.parse)

    def parse_restaurant(self, response):
        self.logger.info("Restaurant detail url: %s" % response.url)
        item = RestaurantItem()
        item['url'] = response.url

        update_date = datetime.now()
        item['update_date'] = update_date.strftime(DATE_FORMAT)
        
        for a in response.xpath('//h1[@id="HEADING"]/text()').extract():
            if a.strip() != "":
                item['name'] = a.strip()

        review_stars = response.xpath('//img[@property="ratingValue"]/@content').extract()
        if review_stars:
            item['review_stars'] = review_stars[0].strip()

        review_qty = response.xpath('//a[@class="more"]/text()').extract()
        if review_qty:
            regx = r'(\d+)'
            pm = re.search(regx, review_qty[0])
            if pm:
                item['review_qty'] = pm.group(0).strip()

        award = response.xpath('//span[@class="taLnk text"]/text()').extract()
        if award:
            item['award'] = award[0].strip()

        rank_xpath = response.xpath('//div[@class="slim_ranking"]')
        if rank_xpath:
            total = ""
            rank = ""
            
            total_xpath = rank_xpath.xpath("./text()")[0]
            regx = r'(\d+)'
            pm = re.search(regx, total_xpath.extract().strip())
            if pm:
                total = pm.group(0)

            result_xpath = rank_xpath.xpath('./b[@class="rank_text wrap"]/span/text()').extract()
            regx = r'(\d+)'            
            pm = re.search(regx, result_xpath[0])
            if pm:
                rank = pm.group(0)

            item['rank'] = '/'.join([rank, total])

        level = []
        for bar in response.xpath('//ul[@class="barChart"]//div[@class="ratingRow wrap"]'):
            info = {}
            key_xpath = bar.xpath('.//span[@class="text"]/text()').extract()
            if key_xpath:
                key = key_xpath[0].strip()
            value_xpath = bar.xpath('.//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()
            if value_xpath:
                regx = r'(\d)'
                pm = re.search(regx, value_xpath[0].strip())
                if pm:
                    value = pm.group(0)
                    info[key] = value
            level.append(info)
        item['level'] = level

        for row in response.xpath('//div[@class="row"]')[1:]:
            key = row.xpath('.//div[contains(@class, "title")]/text()').extract()[0].strip()
            value = row.xpath('.//div[contains(@class, "content")]/text()').extract()
            if key == u'参考价格':
                value = row.xpath('.//div[contains(@class, "content")]/span/text()').extract()
                item['price'] = value[0].strip()
            elif key == u'菜系':
                item['classes'] = map(lambda x:x.strip(), value[0].strip().split(','))
            elif key == u'餐时':
                item['offer_kind'] = map(lambda x:x.strip(), value[0].strip().split(','))
            elif key == u'餐厅特色':
                item['special'] = map(lambda x:x.strip(), value[0].strip().split(','))
            elif key == u'氛围类别':
                item['env'] = map(lambda x:x.strip(), value[0].strip().split(','))
            elif key == u'营业时间':
                open_time = []
                content_lst = row.xpath('.//div[contains(@class, "content")]/div[@class="detail"]')
                for content in content_lst:
                    info = {}
                    day = content.xpath('./span[@class="day"]/text()').extract()[0].strip()
                    hours = content.xpath('./span[@class="hours"]/div[@class="hoursRange"]/text()').extract()
                    info[day] = map(lambda x:x.strip(), hours)
                    open_time.append(info)
                item['open_time'] = open_time

        address_lst = []
        locality = map(lambda x:x.strip(), response.xpath('//span[@class="locality"]/text()').extract())
        if locality:
            address_lst.append(locality[0])
        
        street_address = map(lambda x:x.strip(), response.xpath('//span[@class="street-address"]/text()').extract())
        if street_address:
            address_lst.append(street_address[0])

        extended_address = map(lambda x:x.strip(), response.xpath('//span[@class="extended-address"]/text()').extract())
        if extended_address:
            address_lst.append(extended_address[0])

        postal_code = map(lambda x:x.strip(), response.xpath('//span[@class="postal-code"]/text()').extract())
        if postal_code:
            address_lst.append(postal_code[0])
        item['address'] = ','.join(address_lst)

        phone = response.xpath('//div[@class="fl phoneNumber"]/text()').extract()
        if phone:
            item['telephone'] = phone[0].strip()

        yield item
