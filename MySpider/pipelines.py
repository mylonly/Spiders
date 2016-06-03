# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb


class tbModelPipeline(object):
    def process_item(self,item,spider):
        db = MySQLdb.connect("localhost","root","703003659txg","spider")
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        sql ="INSERT INTO tb_model(user_id,avatar_url,card_url,city,height,identity_url,model_url,real_name,total_fan_num,total_favor_num,view_flag,weight)\
                      VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(item['userId'],item['avatarUrl'],item['cardUrl'],item['city'],item['height'],item['identityUrl'],\
                      item['modelUrl'],item['realName'],item['totalFanNum'],item['totalFavorNum'],item['viewFlag'],item['weight'])
        try:
                print sql
                cursor.execute(sql)
                db.commit()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        db.close()
        return item
        
        
class tbAlbumPipeline(object):
    def process_item(self,item,spider):
        db = MySQLdb.connect("localhost","root","703003659txg","spider")
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        sql ="INSERT INTO tb_album(album_id,album_name,album_url,album_user_id)\
                      VALUES('%s','%s','%s','%s')"%(item['thumb_id'],item['thumb_name'],item['thumb_url'],item['thumb_userId'])
        try:
                print sql
                cursor.execute(sql)
                db.commit()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        db.close()
        return item