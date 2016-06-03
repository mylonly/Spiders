
import urllib2
import os
import re
import codecs
import json
import MySQLdb
import sys
from urllib import unquote
from scrapy import Spider
from scrapy.selector import Selector
from MySpider.items import tbThumbItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class tbModelAlbum(Spider):
    name='tbModelAlbum'
    allow_domains = ['mm.taobao.com']
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
            'MySpider.pipelines.tbAlbumPipeline': 300
        }
    }
    
    def start_requests(self):
        db = MySQLdb.connect("localhost","root","703003659txg","spider")
        cursor = db.cursor()
        sql ="select user_id from tb_model"
        count = cursor.execute(sql)
        results = cursor.fetchmany(count)
        requests = []
        for user_id in results:
            request = Request('https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id=%d'%user_id,callback=self.pre_parse_album,meta={'user_id':user_id[0]})
            requests.append(request)
        return requests
        
    def pre_parse_album(self,response):
        sel = Selector(response)
        total_page = sel.xpath("//input[@name='totalPage']/@value").extract()[0]
        user_id = response.meta['user_id']
        requests = []
        for i in range(1,int(total_page)):
            request = Request("https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id=%s&page=%s" % (str(user_id),str(i)),callback=self.parse_album,meta={'user_id':user_id})
            requests.append(request)
        return requests
    
    def urldecode(self,query):
        d = {}
        a = query.split('&')
        for s in a:
            if s.find('='):
                k,v = map(unquote, s.split('='))
                try:
                    d[k].append(v)
                except KeyError:
                    d[k] = [v]
    
        return d
        
    def parse_album(self,response):
        sel = Selector(response)
        tbThumbItems = []
        thumb_url_list = sel.xpath("//div[@class='mm-photo-cell-middle']//h4//a/@href").extract()       
        thumb_name_list = sel.xpath("//div[@class='mm-photo-cell-middle']//h4//a/text()").extract()
        user_id = response.meta['user_id']
        for i in range(0,len(thumb_url_list)-1):
            thumbItem = tbThumbItem()
            thumbItem['thumb_name'] = thumb_name_list[i].replace('\r\n','').replace(' ','')
            thumbItem['thumb_url'] = thumb_url_list[i]
            thumbItem['thumb_userId'] = str(user_id)
            temp = self.urldecode(thumbItem['thumb_url'])
            thumbItem['thumb_id'] = temp['album_id'][0]
            tbThumbItems.append(thumbItem)
        return tbThumbItems