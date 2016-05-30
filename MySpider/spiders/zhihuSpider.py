import urllib2
import os
import re
import codecs


from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import zhihuItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class zhihuSpider(CrawlSpider):
    name = "zhihu"
    allow_domians = ["zhihu.com"]
    start_urls = ["https://www.zhihu.com/collection/38624707"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/question/\d*')),process_request="request_question"),
    )
    
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36",
    "Referer": "http://www.zhihu.com"
    }
    
    def start_requests(self):
        return [Request("https://www.zhihu.com/",headers = self.headers,meta={"cookiejar":1},callback=self.post_login)]
        
    def post_login(self,response):
        self.log("preparing login...")
        xsrf = Selector(response).xpath('//div[@data-za-module="SignInForm"]//form//input[@name="_xsrf"]/@value').extract()[0]
        self.log(xsrf)
        return FormRequest("https://www.zhihu.com/login/email",meta={'cookiejar':response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata = {
                                             '_xsrf':xsrf,
                                             'referer':'https://www.zhihu.com',
                                             'password':'xgBKQTx7VnVLK9tv',
                                             'captcha_type':'cn',
                                             'email':'tianxianggen@gmail.com',
                                             'remember_me':'true',
                                          },
                                          callback = self.after_login,
                                          )
                                                      
    def after_login(self,response):
        for url in self.start_urls:
            yield Request(url,meta={'cookiejar':1},headers = self.headers)
   
    def request_question(self,request):
        return Request(request.url,meta={'cookiejar':1},headers = self.headers,callback=self.parse_question)
        
    def parse_question(self,response):
        sel = Selector(response)
        item = zhihuItem()
        item['qestionTitle'] = sel.xpath("//div[@id='zh-question-title']//h2/text()").extract_first()
        item['image_urls'] = sel.xpath("//img[@class='origin_image zh-lightbox-thumb lazy']/@data-original").extract()
        return item