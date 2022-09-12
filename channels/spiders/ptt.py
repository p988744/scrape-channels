import urllib.parse

import scrapy
import unicodedata

from parsel import SelectorList

from channels.items import ChannelsItem


class PttSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['www.pttweb.cc']
    start_urls = ['http://www.pttweb.cc/']

    def start_requests(self):
        urls = [
            'https://www.pttweb.cc/cls/1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, method="POST")

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
            yield scrapy.Request(category.get('url'), callback=self.parse_category, method="POST",
                                 meta={'category': category})

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

            yield scrapy.Request(channel_url, callback=self.parse_channel, method="POST", meta={'item': item})

    def parse_channel(self, response, **kwargs):
        item = response.meta['item']
        posts = response.css('.e7-container .e7-meta-container > .e7-grey-text')
        latest_post = posts[0]
        last_post_time = latest_post.css('span::text')[-1].get()
        item['last_post_time'] = last_post_time

        return item
