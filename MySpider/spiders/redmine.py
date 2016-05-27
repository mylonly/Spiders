#coding: utf-8

import urllib2
import os
import re

from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MySpider.items import girlItem
from scrapy.http import Request
from scrapy.http import FormRequest


class redmine(CrawlSpider):
    name = "redmine"
    allowed_domians = ["babyun.cn"]
    start_urls = ["http://redmine.babyun.cn/projects/babyun/issues"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/issues/\d*')),callback='parse_issues',follow=False),
    )
    
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36",
    "Referer": "http://redmine.babyun.cn"
    }
    
    def start_requests(self):
        return [Request("http://redmine.babyun.cn/login",meta={"cookiejar":1},callback=self.post_login)]
        
    def post_login(self,response):
        self.log("preparing login...")
        csrf_token = Selector(response).xpath("//head//meta[@name='csrf-token']/@content").extract()[0]
        self.log(csrf_token)
        return [FormRequest.from_response(response,meta={'cookiejar':response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata = {
                                             'authenticity_token':csrf_token,
                                             'back_url':'http://redmine.babyun.cn/',
                                             'username':'tianxianggen',
                                             'password':'txg123456',
                                             'login':'登录 »'
                                          },
                                          formxpath = "//div[@id='login-form']//form",
                                          callback = self.post_after_login,
                                          dont_filter = True)]
                                                      
    def post_after_login(self,response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
            
    def parse_issues(self,response):
        self.log("find a issues")