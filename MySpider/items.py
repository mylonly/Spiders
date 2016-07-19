# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class girlItem(scrapy.Item):
    altInfo = scrapy.Field()
    imgSrc = scrapy.Field()

class zhihuItem(scrapy.Item):
    qestionTitle = scrapy.Field()
    image_urls = scrapy.Field()

class sisItem(scrapy.Item):
    link = scrapy.Field()
    albumTitle = scrapy.Field()
    image_urls = scrapy.Field()
    
class legItem(scrapy.Item):
    image_urls = scrapy.Field()
    
class tbModelItem(scrapy.Item):
    avatarUrl = scrapy.Field()
    cardUrl = scrapy.Field()
    city = scrapy.Field()
    height = scrapy.Field()
    identityUrl = scrapy.Field()
    modelUrl = scrapy.Field()
    realName = scrapy.Field()
    totalFanNum = scrapy.Field()
    totalFavorNum = scrapy.Field()
    userId = scrapy.Field()
    viewFlag = scrapy.Field()
    weight = scrapy.Field()

class tbThumbItem(scrapy.Item):
    thumb_id = scrapy.Field()
    thumb_userId = scrapy.Field()
    thumb_url = scrapy.Field()
    thumb_name = scrapy.Field()
    
class tbPhotoItem(scrapy.Item):
    user_id = scrapy.Field()
    albumId = scrapy.Field()
    picId = scrapy.Field()
    picUrl = scrapy.Field()
    picWidth = scrapy.Field()
    picHeight = scrapy.Field()
    url = scrapy.Field()

class contactItem(scrapy.Item):
    username = scrapy.Field()
    password = scrapy.Field()