# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from JapanSpider.items import AttractionItem
from datetime import datetime
import re


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class AttractionTripAdvisorSpider(Spider):
    name = "attraction_trip_advisor"
    collection_name = "attractions"
    allowed_domains = ["tripadvisor.cn"]
    start_urls = (
        'http://www.tripadvisor.cn/Attractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html',
    )

    def parse(self, response):
        for title in response.xpath('//div[@class="property_title"]/a/@href').extract():
            url = response.urljoin(title)
            yield Request(url, self.parse_detail)

        next_page = response.xpath('//div[contains(@class, "unified pagination")]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield Request(url, self.parse)

    def parse_detail(self, response):
        self.logger.info('Attraction Detail URL: %s' % response.url)
        item = AttractionItem()

        update_date = datetime.now()
        item['update_date'] = update_date.strftime(DATE_FORMAT)

        item['url'] = response.url

        title = ''.join(response.xpath('//h1[@id="HEADING"]/text()').extract()).strip()
        item['name'] = title

        title_en = response.xpath('//span[@class="altHead"]/text()')
        if title_en:
            item['name_en'] = title_en[0].extract().strip()

        description = response.xpath('//div[@class="listing_details"]/p/text()')
        if description:
            item['description'] = description[0].extract().strip()
        else:
            description = response.xpath('//div[@class="details_wrapper"]/p/text()')
            if description:
                item['description'] = description[0].extract().strip()

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

        if response.xpath('//div[@id="HOUR_OVERLAY_CONTENTS"]'):
            days = response.xpath('//span[@class="days"]/text()')[0].extract().strip()
            hours = response.xpath('//span[@class="hours"]/text()')[0].extract().strip()
            item['open_time'] = [{days: hours}]

        address = []
        region = response.xpath('//span[@property="addressRegion"]/text()')
        if region:
            address.append(region[0].extract().strip())
        locality = response.xpath('//span[@property="addressLocality"]/text()')
        if locality:
            address.append(locality[0].extract().strip())
        street = response.xpath('//span[@property="streetAddress"]/text()')
        if street:
            address.append(street[0].extract().strip())
        postal_code = response.xpath('//span[@property="postalCode"]/text()')
        if postal_code:
            address.append(postal_code[0].extract().strip())
        item['address'] = ''.join(address)

        telephone = response.xpath('//div[@class="phoneNumber"]/text()')
        if telephone:
            item['telephone'] = telephone[0].extract().strip()

        classes = response.xpath('//div[@class="heading_details"]//div[@class="detail"]/a/text()')
        if classes:
            item['classes'] = map(lambda x:x.strip(), classes.extract())

        for detail in response.xpath('//div[@class="details_wrapper"]/div[@class="detail"]'):
            key = ''.join(detail.xpath('.//b/text()').extract()).strip()
            value = detail.xpath('./text()').extract()
            if key == u'建议游览时间：':
                item['suggested_duration'] = ''.join(value).strip()
            elif key == u'收费：':
                item['price'] = ''.join(value).strip()
        
        yield item

