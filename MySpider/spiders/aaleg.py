#coding: utf-8
import urllib2
import os
import re
import codecs


from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import legItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class aalegSpider(CrawlSpider):
    name="aaleg"
    allowed_domains=["aaleg.com"]
    start_urls=["http://www.aaleg.com/"]
    custom_settings = {
    "ITEM_PIPELINES":{'scrapy.pipelines.images.ImagesPipeline': 1},
    "IMAGES_STORE":"/Users/Apple/Pictures/legs"
    }
 
    rules = (
        Rule(SgmlLinkExtractor(allow=('/\d*.html')),callback='parse_page',follow=True),
        Rule(SgmlLinkExtractor(allow=('/\d*.html/\d*')),callback='parse_page'),
    )
    
    
    def parse_page(self,response):
        self.log("find a page")
        sel = Selector(response)
        item = legItem()
        urls = sel.xpath("//div[@class='picsbox picsboxcenter']//img/@src").extract()
        imageUrls = []
        for url in urls:
            imageUrls.append(url)
        item['image_urls'] = imageUrls
        return item
        
        