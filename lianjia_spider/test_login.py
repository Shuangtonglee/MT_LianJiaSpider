from bs4 import BeautifulSoup
import requests
from lianjia_spider.my_session import MySession

session = MySession()

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def is_login():
    proxies={"http": "http://{}".format(get_proxy().decode('utf-8'))}
    profileUrl = 'http://user.lianjia.com'
    profilePage = session.get(profileUrl,proxies=proxies)
    profilePage_bsObj = BeautifulSoup(profilePage.text,'html.parser')
    try:
        user_name = profilePage_bsObj.find('div',{'class':'user-name'}).get_text()
        return user_name
    except:
        return '未登入'

print(is_login())