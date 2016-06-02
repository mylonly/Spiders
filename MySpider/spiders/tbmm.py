import urllib2
import os
import re
import codecs


from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import tbmmItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class zhihuSpider(CrawlSpider):
    name = "tbmm"
    allow_domians = ["mm.taobao.com"]
    start_urls = ["https://mm.taobao.com/search_tstar_model.htm"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('//mm.taobao.com/self/aiShow.htm?spm=.*&userId=\d*')),callback='parse_mm'),
    )
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS':{
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
           "Connection": "keep-alive",
           "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36",
           "Referer": "https://mm.taobao.com"
        },
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
    }
    
    def parse_start_url(self,response):
        open_in_browser(response)
    
    def parse_mm(self,response):
        sel = Selector(response)
        item = tbmmItem()
        item['mm_userId']=sel.xpath("//input[@name='userId']/@value").extract()[0]
        item['mm_avatar']=self.xpath("//div[@class='mm-p-model-info-left-top']//img[@id='J_MmPheader']/@src").extract()[0]
        item['mm_name']=self.xpath("//div[@class='mm-p-model-info-left-top']//dd/a/text()").extract()[0]
        item['mm_usercenter']=self.xpath("//div[@class='mm-p-model-info-left-top']//dd/a/@href").extract()[0]
        self.log(item['mm_name'])
        return item        