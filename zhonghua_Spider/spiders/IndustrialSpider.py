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
        'http://www.chinahr.com/sou/?city=34%2C398&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 北京
        'http://www.chinahr.com/sou/?city=36%2C400&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 上海
        'http://www.chinahr.com/sou/?city=25%2C291&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 广州
        'http://www.chinahr.com/sou/?city=25%2C292&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 深圳
        'http://www.chinahr.com/sou/?city=37%2C401&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 重庆
        'http://www.chinahr.com/sou/?city=27%2C312&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 成都
        'http://www.chinahr.com/sou/?city=16%2C169&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 南京
        'http://www.chinahr.com/sou/?city=16%2C173&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 苏州
        'http://www.chinahr.com/sou/?city=22%2C247&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 郑州
        'http://www.chinahr.com/sou/?city=23%2C264&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 武汉
        'http://www.chinahr.com/sou/?city=17%2C182&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 杭州
        'http://www.chinahr.com/sou/?city=11%2C111&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 石家庄
        'http://www.chinahr.com/sou/?city=13%2C133&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 沈阳
        'http://www.chinahr.com/sou/?city=21%2C230&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 济南
        'http://www.chinahr.com/sou/?city=24%2C277&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 长沙
        'http://www.chinahr.com/sou/?city=30%2C358&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 西安
        'http://www.chinahr.com/sou/?city=18%2C193&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 合肥
        'http://www.chinahr.com/sou/?city=21%2C231&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 青岛
        'http://www.chinahr.com/sou/?city=25%2C307&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 东莞
        'http://www.chinahr.com/sou/?city=15%2C156&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 哈尔滨
        'http://www.chinahr.com/sou/?city=13%2C134&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 大连
        'http://www.chinahr.com/sou/?city=14%2C147&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 长春
        'http://www.chinahr.com/sou/?city=25%2C308&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 中山
        'http://www.chinahr.com/sou/?city=16%2C170&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 无锡
        'http://www.chinahr.com/sou/?city=28%2C333&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 贵阳
        'http://www.chinahr.com/sou/?city=17%2C183&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 宁波
        'http://www.chinahr.com/sou/?city=12%2C122&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 太原
        'http://www.chinahr.com/sou/?city=11%2C116&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 保定
        'http://www.chinahr.com/sou/?city=26%2C309&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 海口
        'http://www.chinahr.com/sou/?city=19%2C211&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 厦门
        'http://www.chinahr.com/sou/?city=42%2C440&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 乌鲁木齐
        'http://www.chinahr.com/sou/?city=39%2C416&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 呼和浩特
        'http://www.chinahr.com/sou/?city=43%2C454&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1',# 香港
        'http://www.chinahr.com/sou/?city=44%2C455&industrys=0&companyType=0&degree=-1&refreshTime=-1&workAge=-1' # 澳门
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
        region = response.xpath("//div[@class='search']/div[@class='wp-input']/h3/text()").extract_first()
        url_part = (response.url).split("industrys=0",1)

        for item in response.xpath("//div[@class='select-type'][@data-type='industry']/div[@class='select-cont']/dl/a"):
            infoItem['Region'] = region
            infoItem['IndustrialName'] = item.xpath("./dt/text()").extract_first()
            industrial_num = str(item.xpath("./@data-val").extract_first())
            # print industrial_num
            infoItem['IndustrialUrl'] = url_part[0] + "industrys=" + industrial_num + url_part[1]
            if infoItem['IndustrialName'] is not None:
                yield infoItem
            else:
                pass
            pass




        pass