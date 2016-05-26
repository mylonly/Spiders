#coding: utf-8
#!/usr/bin/python

import urllib2
import os
import re

from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import girlItem
from scrapy.http import Request

class girlSpider(CrawlSpider):
        name = "girlSpider"
        allowed_domains = ['baike66.com']
        start_urls = ['http://www.baike66.com/']
        number = 0
        rules = (
                        Rule(SgmlLinkExtractor(allow = ('index_\d*.html')),callback = 'parse_image',follow=True),
                        )
        def parse_image(self,response):
                self.log('hi,this is an item page! %s' % response.url)
                sel = Selector(response)
                sites = sel.xpath('//div[@class="thumb"]//img/@src').extract()
                items = []
                for site in sites:
                        url = site
                        if(site.find('http') == -1):
                            url = 'http://www.baike66.com%s' % (site)
                        print 'one image:',url
                        item = girlItem()
                        item['imgSrc'] = url
                        items.append(item)
                return items