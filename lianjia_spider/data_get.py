import queue
import random
import threading
import time
from urllib import parse
import requests
from bs4 import BeautifulSoup
from .html_analyse import HtmlInfo
from lianjia_spider.my_session import MySession


hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


#session = requests.Session()
session = MySession()
htmls = []


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


class myThread(threading.Thread):

    def __init__(self,que,name=''):
        super(myThread,self).__init__()
        self.que = que
        self.name = name

    def run(self):
        while True:
            try:
                Url = self.que.get(timeout = 60)
                while Url:
                    try:
                        proxies={"http": "http://{}".format(get_proxy().decode('utf-8'))}   #变量名必须为proxies
                        time.sleep(random.randint(1,3))
                        Url_page = session.get(Url,headers=hds[random.randint(0,len(hds)-1)],proxies=proxies,timeout=10)

                        #判断得到的网页是否符合要求
                        bsObj = BeautifulSoup(Url_page.text,'html.parser')
                        Infos = bsObj.findAll('div',{'class':'info'})[0] #如果获得的网页中没有这个元素，报错再重新访问该url()
                        htmls.append(Url_page)                             #接上：可能是代理原因，有时获取的页面并不正确，所以添加此判断（对小区页面和成交页面都适用）
                        Url = ''                                           # Url=''时循环终止，当Info出错时，Url一直未真，循环继续，直到得到Info时，代码继续执行，Url=''，循环终止
                    except Exception as e:
                        print(e)
            except:
                break
            self.que.task_done()



class XiaoQu:

    def __init__(self):
        pass

    def xiaoqu_total_pages(self,url):
        while True:
            proxies={"http": "http://{}".format(get_proxy().decode('utf-8'))}
            try:
                bsObj = session.get(url,headers=hds[random.randint(0,len(hds)-1)],proxies=proxies,timeout=10)
                html = BeautifulSoup(bsObj.text,'html.parser')
                total_pages = eval(html.find('div',{'comp-module':'page'}).attrs['page-data'])['totalPage']  #eval 字符串转变为dict
                return total_pages
            except Exception as e:
                print(e)


    def url(self,region_name):
        urls = []
        page_url = 'http://sh.lianjia.com/xiaoqu/'+region_name+'/'
        total_pages = self.xiaoqu_total_pages(page_url)
        #total_pages = 1
        print(total_pages)
        for page_number in range(1,total_pages+1):
            url = 'http://sh.lianjia.com/xiaoqu/'+region_name+'/pg'+str(page_number)+'/'
            urls.append(url)
        return urls


    def xiaoqu_data(self,urls):
        que = queue.Queue(maxsize=50)       #If maxsize is less than or equal to zero, the queue size is infinite.(默认maxsize=0)
        global htmls

        for xiaoquUrl in urls:
            que.put(xiaoquUrl)

        for i in range(20):
            t = myThread(que,self.xiaoqu_data.__name__)
            t.start()

        que.join()
        xiaoquData = HtmlInfo().get_xiaoqu_info(htmls)
        htmls = []

        return xiaoquData




class Chengjiao:

    def __init__(self):
        pass

    def chengjiao_total_pages(self,url):
        print(url)
        while True:
            proxies={"http": "http://{}".format(get_proxy().decode('utf-8'))}
            try:
                bsObj = session.get(url,headers=hds[random.randint(0,len(hds)-1)],proxies=proxies,timeout=10)
                html = BeautifulSoup(bsObj.text,'html.parser')
                deal_number = html.find('div',{'class':'total'}).find('span').get_text()
                if eval(deal_number) == 0:

                    #偶尔会出现成交房源不为0，却显示为0的情况，可能和代理质量有关。检查两次，减少这种情况的放生
                    bsObj = session.get(url,headers=hds[random.randint(0,len(hds)-1)],proxies=proxies,timeout=10)
                    html = BeautifulSoup(bsObj.text,'html.parser')
                    deal_number = html.find('div',{'class':'total'}).find('span').get_text()
                    if eval(deal_number) == 0:
                        total_pages = 0
                        return total_pages
                total_pages = eval(html.find('div',{'comp-module':'page'}).attrs['page-data'])['totalPage']
                return total_pages
            except Exception as e:
                print(e)


    def url(self,xiaoqu_name):
        urls = []
        chengjiao_url = 'http://sh.lianjia.com/chengjiao/'+'rs'+ parse.unquote(xiaoqu_name)+'/'#没有最后的“/”,有时会出现有成交房源但却显示0套的现象
        total_pages =self.chengjiao_total_pages(chengjiao_url)                                      #url最后加上“/”比较好
        #total_pages = 1
        print(total_pages)
        if total_pages == 0:
            return urls
        for page_number in range(1,total_pages+1):
            url = 'http://sh.lianjia.com/chengjiao/'+'pg'+str(page_number)+'rs'+ parse.unquote(xiaoqu_name)+'/'
            urls.append(url)
        return urls

    def chengjiao_data(self,urls):
        que = queue.Queue(maxsize=50)   #放入队列的元素必须<=队列长度maxsize,否则会阻塞
        global htmls                    #使htmls 为全局变量，和函数外的htmls变量相同
        for chengjiao_xiaoquUrl in urls:
            que.put(chengjiao_xiaoquUrl)

        for i in range(20):
            t = myThread(que,self.chengjiao_data.__name__)
            t.start()

        que.join()

        chengjiaoData = HtmlInfo().get_xiaoqu_chengjiao_info(htmls)
        htmls = []   #使队列为空
        return chengjiaoData

