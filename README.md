链家爬虫_多线程   
![](https://img.shields.io/badge/python-3.6-orange.svg)
===
环境
-----
* Python: 3.6.1
* beautifulsoup4: 4.6.0

代理
-----
使用的是大神[@jhao104](https://github.com/jhao104) 的代理池：https://github.com/jhao104/proxy_pool

下载
----
```Bash
git clone git@github.com:Shuangtonglee/MT_LianJiaSpider.git
```

配置
----
安装requests,beautifulsoup4,openpyxl,selenium等依赖，配置login.py 的PhantomJS路径

使用
----
1. 运行代理池  
2. python main.py 或者直接运行main.py(这里其实分三个步骤：先执行login.py,获得cookie,登陆（登陆与否好像获取的数据没差别），然后获取各区小区数据，最后获得各小区的二手房成交数据)

待实现与问题
----
* 由于代理免费，质量不稳定，多了许多不必要的判断。代理质量好的话，代码可以简化很多   
* 近一个月的成交数据没有在网页上直接显示，需要在APP上查看，故没有爬取。但可以通过直接访问爬虫获得的链接获得数据，待实现
* 数据写入MYSQL

数据截图
----
![](http://ww1.sinaimg.cn/large/a656336agy1ftwwv9ncizj20p80ccmy9.jpg) 

![](http://ww1.sinaimg.cn/large/a656336agy1ftwwxkfzitj20zd0b9406.jpg)
