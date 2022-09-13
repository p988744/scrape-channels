import unicodedata
import urllib.parse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import scrapy

from channels.items import ChannelsItem
from channels.utils import get_user_agent

PERIOD_MAPPING = {
    '天': 'days',
    '週': 'weeks',
    '周': 'weeks',
    '月': 'months',
    '年': 'years',
    '小時': 'hours',
    '分鐘': 'minutes',
}


class PttSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['www.pttweb.cc']
    start_urls = ['https://www.pttweb.cc/']
    headers = {"User-Agent": get_user_agent()}

    def start_requests(self):
        urls = [
            'https://www.pttweb.cc/cls/1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, method="GET", headers=self.headers)

    def parse(self, response, **kwargs):
        category_list = []
        category_elem_list = response.xpath('//*[@id="app"]/div/main/div/div/div/div/div/div/div[3]/div[1]/ul/li')

        for category in category_elem_list:
            category_name = unicodedata.normalize('NFKC', category.xpath('./a/text()').get().strip())
            category_url = category.xpath('./a/@href').get()
            category_list.append({
                'name': category_name,
                'url': urllib.parse.urljoin(response.url, category_url)
            })

        category_elem_list = response.xpath(
            '//*[@id="app"]/div/main/div/div/div/div/div/div/div[3]/div[3]/ul/div')
        for category in category_elem_list:
            category_name = unicodedata.normalize('NFKC', category.xpath('./li/a/text()').get().strip())
            category_url = category.xpath('./li/a/@href').get()
            category_list.append({
                'name': category_name,
                'url': urllib.parse.urljoin(response.url, category_url)
            })

        for category in category_list:
            yield scrapy.Request(category.get('url'), callback=self.parse_category, method="GET",
                                 meta={'category': category}, headers=self.headers)

    def parse_category(self, response, **kwargs):
        channel_elem_list = response.xpath('//*[@class="e7-box"]')

        for channel in channel_elem_list:
            channel_alias = unicodedata.normalize('NFKC',
                                                  channel.xpath('./a/div[@class="e7-board-name"]/text()').get().strip(
                                                      '[]').strip())
            channel_info_list = channel.xpath('./div')
            channel_name = channel_info_list[0].xpath('./text()').get()
            if not channel_name:
                channel_name = channel_alias
            channel_url = channel.xpath('./a/@href').get()
            channel_url = urllib.parse.urljoin(response.url, channel_url)
            item = ChannelsItem()
            item['_id'] = channel_alias
            item['name'] = channel_name
            item['url'] = channel_url
            item['parent_name'] = response.meta.get('category').get('name')

            yield scrapy.Request(channel_url, callback=self.parse_channel, method="GET", meta={'item': item},
                                 headers=self.headers)

    def parse_channel(self, response, **kwargs):
        item = response.meta['item']
        posts = response.css('.e7-container .e7-meta-container > .e7-grey-text')
        if posts:
            latest_post = posts[0]
            post_time = latest_post.css('span::text')[-2].get()
            post_date = latest_post.css('span::text')[-1].get()
            last_post_time = post_date
            for key, value in PERIOD_MAPPING.items():
                if key in post_time:
                    time_value = int(post_time.split(key)[0])
                    post_datetime = datetime.now()
                    post_datetime = post_datetime + relativedelta(**{value: -time_value})
                    # post_time = post_time.replace(key, '')
                    last_post_time = post_datetime.strftime(f'%Y/{post_date}')
                    break
            item['last_post_time'] = last_post_time.replace('/', '-')

        return item
