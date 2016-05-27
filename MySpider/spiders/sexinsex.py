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
from scrapy.utils.response import open_in_browser




class sexInSexSpider(CrawlSpider):
    name="sexinsex"
    allowed_domains=["sexinsex.net"]
    start_urls=["http://sexinsex.net/bbs/forum-186-1.html"]
    cookie = ""
    rules = (
        Rule(SgmlLinkExtractor(allow=('/bbs/forum-186-\d*.html')),callback='parse_forum',follow=True),
        Rule(SgmlLinkExtractor(allow=('/bbs/thread-\d*-1-1.html')),callback='parse_thread',follow=False),
    )
    
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
                                          dont_filter = True)]
                                                      
    def after_login(self,response):
        for url in self.start_urls:
            yield Request(url,headers = self.headers,meta={'cookiejar':self.cookie},dont_filter = True)
            
    def parse_forum(self,response):
        self.log("find a forum")
        
    def parse_thread(self,response):
        self.log("find a thread")