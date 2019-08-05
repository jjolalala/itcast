# -*- coding: utf-8 -*-
import scrapy
from ..items import ItcastItem
import json
import re
from scrapy_redis.spiders import RedisSpider


class ItcatSpider(RedisSpider):
    name = 'itcat'
    allowed_domains = ['www.itcast.cn']
    redis_key = 'redis:itcast'

    # start_urls = ['http://www.itcast.cn/newsvideo/newslist.html']

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.url_parse, dont_filter=True)
    #
    # def url_parse(self, response):
    #     url = re.findall(r'http.*\.json', response.text)[0]
    #     yield scrapy.Request(url,, dont_filter=True)

    def parse(self, response):
        url = re.findall(r'http.*\.json', response.text)[0]
        yield scrapy.Request(url=url, callback=self.parse_second)

    def parse_second(self, response):
        data = json.loads(response.text)
        for content in data['data']:
            time = content['uuid'][:8]
            title = content['title']
            overview = content['lead']
            link = response.urljoin(content['url'])
            item = ItcastItem(
                time=time,
                title=title,
                overview=overview,
                link=link)

            yield item
