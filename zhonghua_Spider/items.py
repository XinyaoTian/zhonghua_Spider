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

# 适配 IndustrialSpider
class IndustrialItem(scrapy.Item):
    Region = scrapy.Field() # 所在地区
    IndustrialName = scrapy.Field() # 行业名称
    IndustrialUrl = scrapy.Field()  #行业相应url
    pass

# 适配 JobSpider
class JobItem(scrapy.Item):
    job_name = scrapy.Field() # 职位名称
    salary = scrapy.Field() # 月薪
    condition = scrapy.Field() # 职位条件(格式： [省/市/] 工作经验/学历 )
    publish_date = scrapy.Field() # 发布日期
    company_name = scrapy.Field() # 企业名称
    company_nature = scrapy.Field() # 公司性质
    company_type = scrapy.Field() # 公司类型
    company_scale = scrapy.Field() # 公司规模
    pass
