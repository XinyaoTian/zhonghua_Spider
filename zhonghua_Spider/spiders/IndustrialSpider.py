# -*- encoding:utf-8 -*-
import scrapy

# 导入正则模块用于匹配 url 和 xpath
import re

import time
import sys

import logging
logging.basicConfig(level = logging.DEBUG)

from zhonghua_Spider.items import IndustrialItem

from func_pack import get_current_day
from func_pack import get_current_time

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.conf import settings
from urlparse import urljoin

# 由于python中的string是以ascii编码的,所以在这里要手动转换为utf-8,这样utf-8才可以使用unicode函数解码~
reload(sys)
sys.setdefaultencoding('utf-8')

class IndustrialSpider(CrawlSpider):

    name = "IndustrialSpider"

    custom_settings = {
        'ITEM_PIPELINES':{
            'zhonghua_Spider.pipelines.industrial_JsonWithEncodingPipeline':300, # 将行业数据存入相应的json文件夹中
        }
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept - Encoding":"gzip, deflate",
        "Accept - Language":"zh-CN,zh;q=0.9,en;q=0.8",
        "Cache - Control":"max-age=0",
        "Connection":"keep-alive",
        "Host": "www.chinahr.com",
        # "Referer":" http: // bj.lianjia.com /?utm_source = baidu & utm_medium = pinzhuan & utm_term = biaoti & utm_content = biaotimiaoshu & utm_campaign = sousuo & ljref = pc_sem_baidu_ppzq_x",
        "Upgrade-Insecure-Requests":"1",
        "User - Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    meta = {
        'dont_redirect':True,
        'handle_httpstatus_list': [301, 302],
    }

    allowed_domains = ["chinahr.com"]

    # 用于测试的初始url
    start_urls = [
        'http://www.chinahr.com/sou/?city=34%2C398&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1'
    ]

    cookie = settings['COOKIE']

    # 设置发起请求的各项参数。为避免重复爬取起始页，如注释掉这个函数，转而用parse方法发起首次请求。
    # def start_requests(self):
    #     for href in self.start_urls:
    #         yield scrapy.Request(url=href , callback=self.parse ,method= 'GET',headers = self.headers ,
    #                              meta=self.meta, cookies=self.cookie, encoding='utf-8')

    # 此函数用于发起请求计算总页数并翻页
    def parse(self, response):

        infoItem = IndustrialItem() # 用于存储行业信息的Item
        region = response.xpath("//div[@class='logo']/span/em/text()").extract_first()
        url_part = (response.url).split("industrys=0",1)

        for item in response.xpath("//div[@class='select-cont']/dl[@class='select-l1']/a"):
            infoItem['Region'] = region
            infoItem['IndustrialName'] = item.xpath("./dt/text()").extract_first()
            industrial_num = str(item.xpath("./@data-val").extract_first())
            print industrial_num
            infoItem['IndustrialUrl'] = url_part[0] + industrial_num + url_part[1]
            yield infoItem
            pass




        pass