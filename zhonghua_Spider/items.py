# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhonghuaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class IndustrialItem(scrapy.Item):
    Region = scrapy.Field() # 所在地区
    IndustrialName = scrapy.Field() # 行业名称
    IndustrialUrl = scrapy.Field()  #行业相应url
    pass


