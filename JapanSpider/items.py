# -*- coding: utf-8 -*-
from scrapy import Item, Field


class TaxFreeShopItem(Item):
    name_en = Field() # 英文名
    name_jp = Field() # 日文名
    address_en = Field() # 英文地址
    address_jp = Field() # 日文地址
    prefecture = Field() # 日本省份
    telephone = Field() # 电话
    credit_card = Field() # 信用卡
    lat = Field() # 经纬度
    lng = Field()
    url = Field() # 免税店网址


class ShopItem(Item):
    name = Field()
    name_en = Field()
    description = Field()
    highlights = Field()
    address = Field()
    telephone = Field()
    open_time = Field()
    off_day = Field()
    free_wifi = Field()
    service = Field()
    website = Field()
    credit_card = Field()
    other = Field()
    traffic = Field()
