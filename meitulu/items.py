# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituluItem(scrapy.Item):
    title = scrapy.Field()
    info = scrapy.Field()
    message = scrapy.Field()
    pirc_srcs = scrapy.Field()
    meitu_id = scrapy.Field()

