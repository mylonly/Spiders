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
from MySpider.items import tbPhotoItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class tbModelPhoto(Spider):
    name='tbModelPhoto'
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
            'MySpider.pipelines.tbPhotoPipeline': 300
        }
    }
    
    def start_requests(self):
        db = MySQLdb.connect("localhost","root","*******","spider")
        cursor = db.cursor()
        sql ="select album_user_id,album_id from tb_album"
        count = cursor.execute(sql)
        results = cursor.fetchmany(count)
        requests = []
        for result in results:
            request = Request('https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s'%result,callback=self.pre_parse_photo)
            requests.append(request)
        return requests
        
    def pre_parse_photo(self,response):
        jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
        totoalPage = jsonBody['totalPage']
        requests = []
        for i in range(1,int(totoalPage)):
            request = Request(response.url+'&page=%d'%i,callback=self.parse_photo)
            requests.append(request)
        return requests;
        
    def parse_photo(self,response):
        jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
        picList = jsonBody['picList']
        photos = []
        for pic in picList:
            photoItem = tbPhotoItem()
            photoItem['user_id'] = pic['userId']
            photoItem['albumId'] = pic['albumId']
            photoItem['picId'] = pic['picId']
            photoItem['picUrl'] = pic['picUrl']
            photoItem['picWidth'] = pic['picWidth']
            photoItem['picHeight'] = pic['picHeight']
            photoItem['url'] = pic['url']
            photos.append(photoItem)
        return photos