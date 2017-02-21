from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TaobaoSpider(object):
    '''
    通过关键字抓取淘宝商品(第一页)
    '''

    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.run()


    def run(self):

        keyword = self.get_input()
        self.get_source(keyword)

    def get_input(self):
        '''
        获取用户输入的关键字
        '''
        return input('请输入要搜索的词:\n').strip()

    def get_source(self, keyword):
        '''
        发起搜索并获取网页信息
        '''
        self.driver.get('https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170221&ie=utf8'.format(keyword))

        #等待ajax返回数据
        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "m-itemlist")))

        goodsList = self.driver.find_elements_by_css_selector('.J_MouserOnverReq')

        for goods in goodsList:
            print(goods.text)

        #self.driver.close()

if __name__ == '__main__':
    TaobaoSpider()
