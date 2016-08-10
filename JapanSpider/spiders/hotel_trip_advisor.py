# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from JapanSpider.items import HotelItem
from datetime import datetime
import re


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class HotelTripAdvisorSpider(Spider):
    name = "hotel_trip_advisor"
    collection_name = 'hotel'
    level = [u'豪华', u'中等', u'经济实惠']
    start_urls = [
        "http://www.tripadvisor.cn/Hotels-g298184-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html",
    ]

    def parse(self, response):
        self.logger.info('Hotel list page url: %s' % response.url)
        for href in response.xpath('//div[@class="listing_title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_hotel)

        next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[-1].extract())
            yield Request(url, self.parse)

    def parse_hotel(self, response):
        self.logger.info('Hotel detail page url: %s' % response.url)
        item = HotelItem()

        update_date = datetime.now()
        item['update_date'] = update_date.strftime(DATE_FORMAT)

        item['name'] = ''.join(response.xpath('//h1[@id="HEADING"]/text()').extract()).strip()
        try:
            item['name_en'] = ''.join(response.xpath('//h1[@id="HEADING"]/span[@class="altHead"]/text()').extract()).strip()
        except Exception as e:
            self.logger.error(e)
            item['name_en'] = ''

        try:
            item['review_stars'] = response.xpath('//img[@property="ratingValue"]/@content').extract()[0]
            item['review_qty'] = response.xpath('//a[@property="reviewCount"]/@content').extract()[0]
        except Exception as e:
            self.logger.error(e)
            item['review_stars'] = ""
            item['review_qty'] = ""

        try:
            item['classes'] = response.xpath('//div[starts-with(@class, "popRanking")]/a/text()').extract()[0].split('/')[1].split(' ')[0]
        except Exception, e:
            self.logger.error(e)
            item['classes'] = ""
        
        try:
            rank_str = response.xpath('//div[starts-with(@class, "popRanking")]/b[@class="rank"]/text()').extract()[0]
            regx = r'(\d+)'
            pm = re.search(regx, rank_str)
            rank = pm.group(1)
            total = response.xpath('//div[starts-with(@class, "popRanking")]/a/text()').extract()[0].split('/')[1].split(' ')[2]
            item['rank'] = '/'.join([rank, total])
        except Exception, e:
            self.logger.error(e)
            item['rank'] = ""

        item['url'] = response.url

        # 酒店星级
        stars = response.xpath(u'//img[@title="酒店星级"]/@alt').extract()
        if stars:
            regx = r'(\d\.\d)'
            pm = re.search(regx, stars[0])
            if pm:
                item['stars'] = pm.group(0)

        # 地址
        address_list = []
        region = response.xpath('//span[@property="addressRegion"]/text()').extract()
        if len(region) > 0:
            address_list.append(region[0])
        locality = response.xpath('//span[@property="addressLocality"]/text()').extract()
        if len(locality) > 0:
            address_list.append(locality[0])
        street = response.xpath('//span[@property="streetAddress"]/text()').extract()
        if len(street) > 0:            
            address_list.append(street[0])
        postal = response.xpath('//span[@property="postalCode"]/text()').extract()
        if len(postal) > 0:
            address_list.append(postal[0])
        item['address'] = ''.join(address_list)
        item['locality'] = address_list[:2]

        # 特色
        property_tags = []
        for tag in response.xpath('//ul[@class="property_tags"]/li/text()').extract():
            if len(tag.strip()) != 0:
                property_tags.append(tag.strip())
        item['special'] = property_tags

        # 等级
        level_tags = []
        for tag in response.xpath('//span[@class="tag"]/text()').extract():
            if tag.strip() != "":
                level_tags.append(tag.strip())
        item['level_tags'] = level_tags

        # 活动设施, 客房类型, 网络, 服务
        for amenity in response.xpath('//div[starts-with(@class, "amenity_row")]'):
            t = amenity.xpath('./div[@class="amenity_hdr"]/text()')[0].extract().strip()
            v = amenity.xpath('./div[@class="amenity_lst"]/ul/li/text()').extract()
            if t == u'活动设施':
                activity_list = []
                for activity in v:
                    if activity.strip() != "":
                        activity_list.append(activity.strip())
                item['activity'] = activity_list

            elif t == u'客房类型':
                room_type = []
                for room in v:
                    if room.strip() != "":
                        room_type.append(room.strip())
                item['room_type'] = room_type
            elif t == u'网络':
                network_list = []
                for network in v:
                    if network.strip() != "":
                        network_list.append(network.strip())
                item['network'] = network_list
            elif t == u'服务':
                service_list = []
                for service in v:
                    if service.strip() != "":
                        service_list.append(service.strip())
                item['service'] = service_list
            elif t == u'酒店餐饮':
                restaurant_list = []
                v = amenity.xpath('.//div[@class="poi_card easyClear"]/div[@class="description_block"]')
                for restaurant in v:
                    info = {}
                    try:
                        info['name'] = restaurant.xpath('./a[@class="poi_title"]/text()')[0].extract()
                        info['url'] = response.urljoin(restaurant.xpath('./a[@class="poi_title"]/@href')[0].extract())
                        stars = restaurant.xpath('.//span[starts-with(@class,"rate sprite-rating_s rating_s")]/img/@alt')[0].extract()
                        regx = r'(\d)'
                        pm = re.search(regx, stars)
                        info['review_stars'] = pm.group(0)
                        qty =  restaurant.xpath('.//div[@class="rating"]/a/text()')[0].extract()
                        regx = r'(\d+)'
                        info['review_qty'] = re.search(regx, qty).group(0)
                        classes_xpath = restaurant.xpath('.//div[@class="details_block"]/text()').extract()
                        if len(classes_xpath) > 0:
                            classes = classes_xpath[-1].strip().split(',')
                            info['classes'] = map(lambda x:x.strip(), classes)
                        else:
                            info['classes'] = []
                        restaurant_list.append(info)
                    except Exception as e:
                        info = {}
                item['restaurant'] = restaurant_list
            else:
                continue
        
        try:
            item['price'] = response.xpath('//span[@property="priceRange"]/text()')[0].extract()
        except Exception as e:
            self.logger.error(e)
            item['price'] = ''

        try:
            item['lat'] = response.xpath('//div[@class="mapContainer"]/@data-lat')[0].extract()
            item['lng'] = response.xpath('//div[@class="mapContainer"]/@data-lng')[0].extract()
        except Exception as e:
            self.logger.error(e)
            item['lat'] = ''
            item['lng'] = ''
        self.logger.debug(item)
        yield item
