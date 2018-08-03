import requests
import json


class MySession(requests.Session):
    def __init__(self):
        super(MySession,self).__init__()

        with open('./lianjia_spider/cookie.json','r') as f: #运行main.py 时路径
        #with open('cookie.json','r') as f:  #运行test_login.py 时路径。为啥路径不一致，和执行文件的路径有关，原因？
            data = json.load(f)


        for cookie in data:
            c = {cookie['name']: cookie['value']}
            self.cookies.update(c)
