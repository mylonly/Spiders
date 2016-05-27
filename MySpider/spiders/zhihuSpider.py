import urllib2
import os
import re
import codecs


from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import girlItem
from scrapy.http import Request
from scrapy.http import FormRequest


class zhihuSpider(CrawlSpider):
    name = "zhihu"
    allow_domians = ["zhihu.com"]
    start_urls = ["https://www.zhihu.com/collection/38624707"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/question/\d*')),callback='parse_question',follow=False),
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
        return [Request("https://www.zhihu.com/",meta={"cookiejar":1},callback=self.post_login)]
        
    def post_login(self,response):
        self.log("preparing login...")
        xsrf = Selector(response).xpath('//body//div[@data-za-module="SignInForm"]//form//input[@name="_xsrf"]/@value').extract()[0]
        self.log(xsrf)
        return [FormRequest.from_response(response,meta={'cookiejar':response.meta['cookiejar']},
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
                                          dont_filter = True)]
                                                      
    def after_login(self,response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
            # yield Request(url,meta={'cookiejar':response.meta['cookiejar']},dont_filter = True)
        