from bs4 import BeautifulSoup
import re


class HtmlInfo:

    def __init__(self):
        pass

    def get_xiaoqu_info(self,htmls):
        xiaoqu_list = []
        for xiaoqu_html in htmls:
            xiaoquUrl_bsObj = BeautifulSoup(xiaoqu_html.text,'html.parser')
            xiaoquInfos = xiaoquUrl_bsObj.findAll('li',{'class':'clear xiaoquListItem'})
            for xiaoquInfo in xiaoquInfos:
                try:
                    name = xiaoquInfo.find('div',{'class':'title'}).find('a').get_text().strip()
                except:
                    name = ''

                try:
                    average_price = xiaoquInfo.find('div',{'class':'totalPrice'}).find('span').get_text()
                except:
                    average_price = ''

                try:
                    sale_number = xiaoquInfo.find('div',{'class':'xiaoquListItemSellCount'}).find('span').get_text()
                except:
                    sale_number = ''

                district_location_year = xiaoquInfo.find('div',{'class':'positionInfo'}).get_text().replace('/','').strip().split()
                try:
                    district = district_location_year[0]
                except:
                    district = ''
                try:
                    location = district_location_year[1]
                except:
                    location = ''
                try:
                    year = district_location_year[2]
                except:
                    year = ''
                try:
                    subway = xiaoquInfo.find('div',{'class':'tagList'}).find('span').get_text().strip()
                except:
                    subway = ''
                xiaoqu_list.append([name,average_price,sale_number,district,location,subway,year])
        return xiaoqu_list


    def get_xiaoqu_chengjiao_info(self,htmls):
        chengjiao_list = []
        for chengjiao_html in htmls:
            chengjiao_bsObj = BeautifulSoup(chengjiao_html.text,'html.parser')
            chengjiaoInfos =  chengjiao_bsObj.findAll('div',{'class':'info'})
            for chengjiaoInfo in chengjiaoInfos:
                houseArea = chengjiaoInfo.find('div',{'class':'title'}).find('a').get_text().strip().split(' ')
                try:
                    xiaoqu_name = houseArea[0]
                except:
                    xiaoqu_name = ''
                try:
                    room = houseArea[1]
                except:
                    room = ''
                try:
                    area = houseArea[-1].replace('平米','')
                except:
                    area = ''

                try:
                    href = chengjiaoInfo.find('div',{'class':'title'}).find('a').attrs['href']
                except:
                    href = ''

                houseinfo = chengjiaoInfo.find('div',{'class':'houseInfo'}).get_text()
                houseinfo = re.sub('\s','',houseinfo).split('|')
                try:
                    orientation = houseinfo[0]
                except:
                    orientation = ''
                try:
                    decoration = houseinfo[1]
                except:
                    decoration = ''
                try:
                    elevator = houseinfo[-1]
                except:
                    elevator = ''

                try:
                    total_price = chengjiaoInfo.find('span',{'class':'number'}).get_text()
                except:
                    total_price = ''

                floor_type = chengjiaoInfo.find('div',{'class':'positionInfo'}).get_text().split(' ')
                try:
                    floor = floor_type[0]
                except:
                    floor = ''
                try:
                    type = floor_type[-1]
                except:
                    type = ''

                try:
                    subway_fangben = chengjiaoInfo.find('span',{'class':'dealHouseTxt'}).findAll('span')
                    if len(subway_fangben) == 1 and '距' in subway_fangben[0].get_text():
                        subway  = subway_fangben[0].get_text()
                        fangben = ''
                    elif len(subway_fangben) == 2:
                        fangben  = subway_fangben[0].get_text()
                        subway  = subway_fangben[-1].get_text()
                    else:
                        subway  = ''
                        fangben = subway_fangben[0].get_text()
                except:
                        subway  = ''
                        fangben = ''

                try:
                    unit_price = chengjiaoInfo.find('div',{'class':'unitPrice'}).get_text().strip().replace('元/平','')
                except:
                    unit_price = ''
                try:
                    dealInfo = chengjiaoInfo.find('span',{'class':'dealCycleTxt'}).findAll('span')
                    if len(dealInfo) ==2:
                        guapai_price = dealInfo[0].get_text().replace('挂牌','').replace('万','')
                        deal_cycle = dealInfo[-1].get_text().replace('成交周期','').replace('天','')
                    elif len(dealInfo) ==1 and '成交周期' in dealInfo[-1].get_text():
                        guapai_price = ''
                        deal_cycle = dealInfo[0].get_text().replace('成交周期','').replace('天','')
                    else:
                        deal_cycle = ''
                        guapai_price= dealInfo[0].get_text().replace('挂牌','').replace('万','')
                except:
                        guapai_price = ''
                        deal_cycle = ''
                try:
                    deal_date = chengjiaoInfo.find('div',{'class':'dealDate'}).get_text().strip()
                except:
                    deal_date = ''

                chengjiao_list.append([xiaoqu_name,room,area,floor,unit_price,total_price,guapai_price,subway,orientation,decoration,fangben,elevator,type,deal_cycle,deal_date,href])
        return chengjiao_list
