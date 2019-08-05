# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don"t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql
import re
import redis


class FilterPipeline(object):

    def process_item(self, item, spider):
        for i in list(item.keys()):
            if "\"" in item[i]:
                item[i] = re.sub(r'\"', '  ', item[i])
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.count = 0
        self.db = pymysql.connect(host="45.89.229.114", port=3306, user="ubuntu", password="root", db="news",
                                  charset="utf8")
        self.table = "nn"
        self.cursor = self.db.cursor()
        self.sql = f"""CREATE TABLE IF NOT EXISTS nn(
                   count INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                   time VARCHAR (255) NOT NULL,
                   title VARCHAR (255) NOT NULL,
                   overview VARCHAR (255) NOT NULL,
                   link VARCHAR (255) NOT NULL)
                   """
        self.cursor.execute(self.sql)

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.count += 1

        sql = f"""INSERT INTO nn(count,time,title,overview,link) 
                VALUES ({self.count},'{item["time"]}','{item["title"]}','{item["overview"]}','{item["link"]}')"""

        try:
            self.count += 1
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("Fail")
            self.db.rollback()
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="45.89.229.114", port=27017)
        self.db = self.client["new"]
        self.collection = self.db["info"]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item


class RedisFipeline(object):
    def __init__(self):
        self.__redis = redis.StrictRedis(host='45.89.229.114', port=6379)

    def process_item(self, item, spider):
        print(item)
        self.__redis.lpush("conpany", str(item))
