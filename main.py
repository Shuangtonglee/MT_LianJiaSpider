from lianjia_spider.excel_write import ExcelWrite
from lianjia_login import login


def run():
    login.login()
    writer = ExcelWrite()
    writer.xiaoqu_write_into_excel()
    writer.chengjiao_write_into_excel()

if __name__ =='__main__':
    run()