# -*- coding:utf-8 -*-
import json
import time
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#用于获取已经取得的全部社区的url地址
def get_jobhrefs():
    with open("./overview.json",'r')as f:
        temp = json.loads(f.read())
        #注意json文件以一个空的字典{}结尾！
    f.close()
    list_href = []
    for item in temp:
        if bool(item) is True: #由于json文件中最后一个数据为空，因此设置此判断防止误读
            list_href.append(str(item["job_url"])) #注意这里unicode转为utf-8的方法...
    #print list_href
    return list_href

# l = get_jobhrefs()
# print type(l[0])
# print len(l)

#获取当前系统日期
def get_current_day():
    current_day = str(time.strftime("%Y_%m_%d"))
    #print current_day
    return current_day

#获取当前系统时间
def get_current_time():
    current_time = str(time.strftime("%H_%M_%S"))
    return current_time

#创建新的数据库名字
#我们设计的爬虫是要部署到云服务器上 利用脚本在每天固定时间对链家网进行爬取的
#因此 我们把每天得到的数据存进不同的表中 方便以后做数据的趋势分析
def create_daytime_table():
    houseInfo = "houseInfo"
    table_name = houseInfo + "_" + get_current_day()
    return table_name

def create_time_table():
    houseInfo = "houseInfo"
    table_name = houseInfo + "_" + get_current_day() + "_" + get_current_time()
    return table_name

# 本函数使用芝麻代理的API接口(HTTP类型,json格式)
# 并将获取到的数据储存为以dict为单元的list，直接对接到 settings.py 的 PROXIES 中使用
def get_zhima_agency(url):
    ip_list = []
    # 尝试获取芝麻代理API接口的ip数据，并组成一个dict，之后放在list中
    try:
        result = requests.get(url)
        content_dict = json.loads(result.content)
        # 可以通过打印 content_dict 来确定从API接口获取到的ip数据结构
        for item in content_dict['data']:
            ip_port_dict = {}
            ip_port_str = str(item['ip']) + ":" + str(item['port'])
            ip_port_dict['ip_port'] = ip_port_str
            ip_port_dict['user_pass'] = ''
            ip_port_dict['ip_status'] = 1 # 初始化ip状态为1 即可用状态。随后如果TCP连续3次未连接上则置0。ip失效。
            ip_list.append(ip_port_dict)
    except:
        print "Warnning!Check your web connection or your ZhiMa Ip agency url status."
    finally:
        # 最终，打印并返回从API中获取的list
        print ip_list
        return ip_list

#这个函数是用于转化浏览器上开发者工具里复制粘贴下来的COOKIE的
#先把cookie那一栏粘贴上从浏览器复制下来的一大长串COOKIE
#运行这个文件，会打印出字典格式的COOKIE
#把这个字典格式的COOKIE复制粘贴到settings里面，再在相关爬虫文件里引用就可以啦
class transCookie():
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

# if __name__ == "__main__":
#     #这个是现在我的COOKIE 大家要根据自己的浏览器复制进自己的COOKIE哟
#     cookie = 'RecentVisitCity=398_beijing; RecentVisitCityFullpathPc="34,398"; chrId=56f6aa7c02884c0ba2d8515a8d10f6e4; 58tj_uuid=bb7293e3-2b32-4bb4-8131-f90da10d07b9; channel=social; init_refer=https%253A%252F%252Fwww.google.com%252F; new_uv=1; utm_source=; spm=; gr_user_id=0085bbce-8e22-4e9e-b996-37f4c69f4bb4; wmda_uuid=dc107aa88a1338ad56cc2fdbe6eb01e4; wmda_new_uuid=1; wmda_session_id_1732047435009=1533176148779-c88ca0a2-9117-184d; wmda_visited_projects=%3B1732047435009; new_session=0; gtid=2437529ddc854086b4fa601f12c4b062'
#     trans = transCookie(cookie)
#     print trans.stringToDict()








#Testing code
#print get_comhrefs()
#print(temp)
#print(temp[1]['href_community'])