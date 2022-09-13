import random
import urllib.parse

import scrapy

from channels.items import ChannelsItem
from channels.utils import get_user_agent


class Mobile01Spider(scrapy.Spider):
    name = 'mobile01'
    allowed_domains = ['mobile01.com']
    start_urls = ['https://www.mobile01.com/']
    headers = {"User-Agent": get_user_agent()}

    def start_requests(self):
        urls = [
            'https://m.mobile01.com/'
        ]
        for url in urls:
            yield scrapy.Request(
                url=url, callback=self.parse, method="GET",
                headers=self.headers
            )

    def parse(self, response, **kwargs):
        menu_elem_list = response.xpath(
            '/html/body/div[1]/header/nav'
            '/div[@class="c-menuTab"]/div[@data-tab-id="forumlist"]'
            '/div[@class="l-menu"]/div[@class="l-menu__block"]/ul[@class="c-menuLv1"]/li')
        for menu_elem in menu_elem_list:
            patent_name = menu_elem.xpath('./a/text()').get()
            # print(patent_name)
            sub_menu_elem_list = menu_elem.xpath(
                './div[@class="c-menuLv1__child"]'
                '/div[@class="c-menuLv2"]'
                '/div[@class="c-menuLv2__subMenu"]'
                '/div'
            )
            if not sub_menu_elem_list:
                continue
            for sub_menu_elem in sub_menu_elem_list:
                sub_menu_name = sub_menu_elem.xpath('./div/span/text()').get()
                # print(sub_menu_name)
                channel_elem_list = sub_menu_elem.xpath('./div[@class="c-menuLv3__links"]/ul/li')
                for channel_elem in channel_elem_list:
                    channel_name = channel_elem.xpath('./a/text()').get()
                    channel_url = channel_elem.xpath('./a/@href').get()
                    channel_url = urllib.parse.urljoin(response.url, channel_url)
                    print(channel_name, channel_url)
                    item = ChannelsItem()
                    r = urllib.parse.urlparse(channel_url)
                    query_params = urllib.parse.parse_qs(r.query)
                    if 'f' in query_params:
                        channel_id = f"f{query_params['f'][0]}"
                    elif 'c' in query_params and 's' in query_params:
                        channel_id = f"c{query_params['c'][0]}s{query_params['s'][0]}"
                    else:
                        channel_id = None
                    item['_id'] = channel_id
                    item['name'] = channel_name
                    item['url'] = channel_url
                    item['parent_name'] = f'{patent_name} > {sub_menu_name}'
                    yield scrapy.Request(channel_url, callback=self.parse_channel, method="GET", meta={'item': item},
                                         headers=self.headers)

    def parse_channel(self, response):
        item = response.meta['item']
        posts = response.xpath(
            '/html/body/div[1]/main'
            '/div[1]/div/div[2]/div[5]/div/'
            'div[@class="l-articleList"]/div[@class="c-articleItem"]'
        )
        if posts:
            latest_post = posts[0]
            latest_post_meta = latest_post.xpath('./div[@class="c-articleItem__remark"]')[-1]
            last_post_time = latest_post_meta.xpath(
                './div[@class="c-articleItemRemark"]/div[@class="c-articleItemRemark__wAuto"]/span/text()').get()
            item['last_post_time'] = last_post_time

        return item
