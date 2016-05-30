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