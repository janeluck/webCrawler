from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv

class TaobaoSpider(object):
    '''
    通过关键字抓取淘宝商品(第一页)
    '''

    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.run()


    def run(self):

        keyword = self.get_input()
        result = self.get_source(keyword)
        self.write_csv(result)

    def get_input(self):
        '''
        获取用户输入的关键字
        '''
        return input('请输入要搜索的词:\n').strip()

    def get_source(self, keyword):
        '''
        发起搜索并获取网页信息
        返回可用信息列表
        '''

        self.driver.get('https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170221&ie=utf8'.format(keyword))

        #等待ajax返回数据
        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "m-itemlist")))

        #拿到当页所有的商品信息
        goodsElement = self.driver.find_elements_by_css_selector('.J_MouserOnverReq')


        goods_list = []

        #遍历每一个商品, 取出名称name, 链接link, 价格price, 店名shop, 地址location, 已付款人数deal-cnt
        for goods in goodsElement:

            goods_dict = {
                'name': goods.find_element_by_xpath('.//a[starts-with(@id, "J_Itemlist_TLink_")]').text,
                'link': goods.find_element_by_xpath('.//a[starts-with(@id, "J_Itemlist_TLink_")]').get_attribute(
                    'href'),
                'price': goods.find_element_by_css_selector('.price').text[1:],
                'shop': goods.find_elements_by_css_selector('.shopname>span')[1].text,
                'location': goods.find_element_by_css_selector('.location').text,
                'deal-cnt': goods.find_element_by_css_selector('.deal-cnt').text[:-3]
            }


            goods_list.append(goods_dict)

            # 打印每个商品的信息
            print(goods_dict)
            print('\n')

        self.driver.close()
        return  goods_list



    def write_csv(self, goods_list):
        '''
        #生成csv文件
        '''

        with open('taobao.csv', 'w', encoding='UTF-8') as f:

            writer = csv.DictWriter(f, fieldnames=['name', 'price', 'shop', 'location', 'deal-cnt', 'link'])
            writer.writeheader()
            writer.writerows(goods_list)


if __name__ == '__main__':
    TaobaoSpider()
