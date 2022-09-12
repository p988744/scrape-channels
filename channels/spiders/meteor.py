import json

import scrapy

import urllib.parse

from channels.items import ChannelsItem


class MeteorSpider(scrapy.Spider):
    name = 'meteor'
    allowed_domains = ['meteor.today']
    start_urls = ['https://meteor.today/']

    def start_requests(self):
        urls = [
            'https://meteor.today/board/get_boards'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, method="POST")

    def parse(self, response, **kwargs):
        # do url decode
        result = response.json()
        result = json.loads(urllib.parse.unquote(result.get('result')))
        for idx, rs in enumerate(result):
            channel_url = 'https://meteor.today/board/{}'.format(rs.get('alias'))
            item = ChannelsItem()
            item['_id'] = rs.get('id')
            item['name'] = rs.get('name')
            item['url'] = channel_url
            item['parent_name'] = rs.get('category')

            payload = {"boardId": item['_id'], "page": 0, "isCollege": False, "pageSize": 30}
            yield scrapy.Request(url='https://meteor.today/article/get_new_articles', callback=self.parse_channel,
                                 method="POST", body=json.dumps(payload), meta={'item': item})

    def parse_channel(self, response, **kwargs):
        item = response.meta['item']
        result = response.json()
        if result.get('result'):
            result = json.loads(urllib.parse.unquote(result.get('result')))
            if isinstance(result, list) and len(result) > 0:
                item['last_post_time'] = result[0].get('createdAt')
        return item

