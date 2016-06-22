#coding: utf-8
import urllib2
import os
import re
import codecs


from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import sisItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser




class sisSpider(CrawlSpider):
    name="sis"
    allowed_domains=["sexinsex.net"]
    start_urls=["http://sexinsex.net/bbs/forum-186-1.html"]
    cookie = ""
    rules = (
        Rule(SgmlLinkExtractor(allow=('/bbs/forum-186-\d*.html')),process_request='request_form',follow=True),
        Rule(SgmlLinkExtractor(allow=('/bbs/thread-\d*-1-\d*.html')),process_request='request_thread'),
    )
    custom_settings = {
       "IMAGES_STORE":"/Users/mylonly/Pictures/zhihu",
       "ITEM_PIPELINES":{
         'scrapy.pipelines.images.ImagesPipeline': 1,
       }
    }
    
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36",
    "Referer": "http://sexinsex.net/bbs/index.php"
    }
    
    def start_requests(self):
        return [Request("http://sexinsex.net/bbs/logging.php?action=login",meta={"cookiejar":1},callback=self.post_login)]
        
    def post_login(self,response):
        self.log("preparing login...")
        formhash = Selector(response).xpath('//form//input[@name="formhash"]/@value').extract()[0]
        self.log(formhash)
        self.cookie = response.meta['cookiejar']
        self.log(self.cookie)
        return [FormRequest.from_response(response,meta={'cookiejar':response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata = {
                                             'formhash':formhash,
                                             'referer':'http://sexinsex.net/bbs/index.php',
                                             'loginfield':'username',
                                             'username':'adimtxg0422',
                                             'password':'703003659txg',
                                             'questionid':'0',
                                             'cookietime':'2592000',
                                             'loginsubmit':'true'
                                          },
                                          callback = self.after_login,
                                          dont_filter = False)]
                                                      
    def after_login(self,response):
        for url in self.start_urls:
            yield Request(url,headers = self.headers,meta={'cookiejar':self.cookie})
            
    
    def request_form(self,request):
        return Request(request.url,headers = self.headers,meta={'cookiejar':self.cookie})
    
    def request_thread(self,request):
        return Request(request.url,headers = self.headers,meta={'cookiejar':self.cookie},callback=self.parse_thread)

    def parse_thread(self,response):
        self.log("find a thread")
        sel = Selector(response)
        title = ""
        titles = sel.xpath("//form[@name='modactions']//div[@class='mainbox viewthread']//h1/text()").extract()
        for txt in titles:
            title = txt.encode('utf-8')
            break
        self.log(title)
        item = sisItem()
        item['link'] = response.request.url
        item['albumTitle'] = title
        imageUrls = []
        urls = sel.xpath("//div[contains(@id,'postmessage')]//img[contains(@src,'http')]/@src").extract()
        for url in urls:
            imageUrls.append(url)
        item['image_urls'] = imageUrls
        return item