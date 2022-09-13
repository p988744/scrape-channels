# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChannelsItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    parent_name = scrapy.Field()
    last_post_time = scrapy.Field()


class YoutubeItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    viewCount = scrapy.Field()
    subscriberCount = scrapy.Field()
    videoCount = scrapy.Field()
