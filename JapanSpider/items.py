# -*- coding: utf-8 -*-
from scrapy import Item, Field


class TaxFreeShopItem(Item):
    name_en = Field()  # 英文名
    name_jp = Field()  # 日文名
    address_en = Field()  # 英文地址
    address_jp = Field()  # 日文地址
    prefecture = Field()  # 日本省份
    telephone = Field()  # 电话
    credit_card = Field()  # 信用卡
    lat = Field()  # 经纬度
    lng = Field()
    url = Field()  # 免税店网址


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


class HotelItem(Item):
    name = Field()  # 名称
    name_en = Field()  # 英文名称
    url = Field()  # 链接地址
    classes = Field()  # 酒店类型
    address = Field()  # 地址
    locality = Field()  # 地区
    review_stars = Field()  # 点评星级
    review_qty = Field()  # 点评数
    rank = Field()  # 酒店排名
    restaurant = Field()  # 酒店餐饮
    price = Field()  # 价格区间
    network = Field()  # 网络情况
    service = Field()  # 提供的服务
    room_type = Field()  # 客房类型
    activity = Field()  # 活动设施
    special = Field()  # 酒店特色
    lat = Field()  # 经纬度
    lng = Field() 
    level_tags = Field()  # 标签
    stars = Field()  # 星级
    update_date = Field()  # 数据库更新时间


class RestaurantItem(Item):
    name = Field()
    url = Field()
    classes = Field()  # 菜系
    rank = Field()  # 排名
    review_stars = Field()  # 评价星级
    review_qty = Field()  # 评价数
    address = Field()
    open_time = Field()
    price = Field()
    level = Field()  # 评级
    offer_kind = Field()  # 餐时
    special = Field()  # 餐厅特色
    env = Field()  # 氛围类别
    telephone = Field()  # 电话
    update_date = Field()
    award = Field()


class AttractionItem(Item):
    name = Field()  # 名称
    name_en = Field()
    description = Field()
    review_stars = Field()
    review_qty = Field()
    rank = Field()
    award = Field()
    open_time = Field()
    price = Field()
    address = Field()
    lat = Field()
    lng = Field()
    telephone = Field()
    suggested_duration = Field()  # 建议浏览时间
    classes = Field()  # 景点类型
    url = Field()
    update_date = Field()
