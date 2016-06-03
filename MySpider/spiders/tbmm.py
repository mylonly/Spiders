
import urllib2
import os
import re
import codecs
import json

import sys


from scrapy import Spider
from scrapy.selector import Selector
from MySpider.items import tbModelItem,tbThumbItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

reload(sys)
sys.setdefaultencoding('utf8')

class tbmmSpider(Spider):
    name = "tbmm"
    allow_domians = ["mm.taobao.com"]
    
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS":{
            'authority':'mm.taobao.com',
            'accept':'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate',
            'accept-language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'origin':'https://mm.taobao.com',
            'referer':'https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.KDdsmP',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'x-requested-with':'XMLHttpRequest',
            'cookie':'cna=/oN/DGwUYmYCATFN+mKOnP/h; tracknick=adimtxg; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; thw=cn; v=0; cookie2=1b2b42f305311a91800c25231d60f65b; t=1d8c593caba8306c5833e5c8c2815f29; _tb_token_=7e6377338dee7; CNZZDATA30064598=cnzz_eid%3D1220334357-1464871305-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464871305; CNZZDATA30063600=cnzz_eid%3D1139262023-1464874171-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464874171; JSESSIONID=8D5A3266F7A73C643C652F9F2DE1CED8; uc1=cookie14=UoWxNejwFlzlcw%3D%3D; l=Ahoatr-5ycJM6M9x2/4hzZdp6so-pZzm; mt=ci%3D-1_0'
        },
        "ITEM_PIPELINES":{
            'MySpider.pipelines.tbModelPipeline': 300
        }
    } 
    
    
    def start_requests(self):
        url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
        requests = []
        for i in range(1,60):
            formdata = {"q":"",
                        "viewFlag":"A",
                        "sortType":"default",
                        "searchStyle":"",
                        "searchRegion":"city:",
                        "searchFansNum":"",
                        "currentPage":str(i),
                        "pageSize":"100"}
            request = FormRequest(url,callback=self.parse_model,formdata=formdata)
            requests.append(request)
        return requests
        
    def parse_model(self,response):
        jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
        models = jsonBody['data']['searchDOList']
        modelItems = []
        for dict in models:
            modelItem = tbModelItem()
            modelItem['avatarUrl'] = dict['avatarUrl']
            modelItem['cardUrl'] = dict['cardUrl']
            modelItem['city'] = dict['city']
            modelItem['height'] = dict['height']
            modelItem['identityUrl'] = dict['identityUrl']
            modelItem['modelUrl'] = dict['modelUrl']
            modelItem['realName'] = dict['realName']
            modelItem['totalFanNum'] = dict['totalFanNum']
            modelItem['totalFavorNum'] = dict['totalFavorNum']
            modelItem['userId'] = dict['userId']
            modelItem['viewFlag'] = dict['viewFlag']
            modelItem['weight'] = dict['weight']
            modelItems.append(modelItem)
        return modelItems
        