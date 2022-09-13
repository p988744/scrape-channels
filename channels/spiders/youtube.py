import os
import urllib.parse as urlparse
import random

import scrapy

from channels.items import YoutubeItem
from channels.utils import get_user_agent

YT_API_KEY = os.environ.get('YT_API_KEY')


class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    headers = {"User-Agent": get_user_agent()}
    allowed_domains = ['youtube.com']
    start_urls = ['https://youtube.com/']
    base_url = 'https://youtube.googleapis.com/youtube/v3/channels'
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": None,
        "key": YT_API_KEY,
    }

    def start_requests(self):
        channels = ["UCOz7W0VH--2WlqAE_3jtL4w"]
        for channel in channels:
            params = self.params.copy()
            params['id'] = channel
            url_parts = list(urlparse.urlparse(self.base_url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update(params)

            url_parts[4] = urlparse.urlencode(query)
            url = urlparse.urlunparse(url_parts)
            yield scrapy.Request(url, callback=self.parse, method="GET",
                                 meta={'params': self.params},
                                 headers=self.headers)

    def parse(self, response, **kwargs):
        resp = response.json()
        item = YoutubeItem()
        item['_id'] = resp['items'][0]['id']
        item['name'] = resp['items'][0]['snippet']['title']
        item['url'] = f"https://www.youtube.com/channel/{resp['items'][0]['id']}"
        item['description'] = resp['items'][0]['snippet']['description']
        item['viewCount'] = resp['items'][0]['statistics']['viewCount']
        item['subscriberCount'] = resp['items'][0]['statistics']['subscriberCount']
        item['videoCount'] = resp['items'][0]['statistics']['videoCount']
        return item
