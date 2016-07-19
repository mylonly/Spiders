
import urllib2
import os
import re
import codecs
import json
import sys


from scrapy import Spider
from scrapy.selector import Selector
from MySpider.items import contactItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class tbmmSpider(Spider):
    name = "bby"
    allow_domians = ["pluto.babyun.cn"]
    
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
            'authority':'pluto.babyun.cn',
            'accept':'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate',
            'accept-language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'origin':'http://pluto.babyun.com.cn/pluto/user/signin',
            'referer':'http://pluto.babyun.com.cn/pluto/user/signin',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'x-requested-with':'XMLHttpRequest',
        },
        "ITEM_PIPELINES":{
            'MySpider.pipelines.contactPipeline': 300
        }
    } 
    
    def start_requests(self):
        url = "http://pluto.babyun.com.cn/pluto/api/user/signin"
        return [FormRequest(url,meta={'cookiejar':1},
                                          formdata = {
                                             'password':'3aF9Ac3R4M76e',
                                             'username':'admin',
                                             'remember':'true',
                                          },
                                          callback = self.after_login,
                                          )]
    
    def after_login(self,response):
        requests = []
        for i in range(1,37):
            url = "http://pluto.babyun.com.cn/pluto/api/authuser/list?nickname=&username=&card_no=&org_name=&role=21&status=0&province_id=0&city_id=0&page=%s&page_size=10" % str(i)
            requests.append(Request(url,meta={'cookiejar':1},callback=self.parse_contact))
        return requests

    def parse_contact(self,response):
        jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
        models = jsonBody['data']['list']
        items = []
        for dict in models:
            item = contactItem()
            item['username']=dict['username']
            item['password']=dict['password']
            items.append(item)
        return items