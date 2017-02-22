from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
from datetime import date


class TaobaoJsonSpider(object):
    '''
    通过关键字抓取淘宝商品(第一页)
    '''

    def __init__(self):

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
        发起搜索并获取json
        '''

        source = requests.get('https://s.taobao.com/search?q={}&ajax=true'.format(keyword)).json()

        # 拿到当页所有的商品信息
        items = source['mods']['itemlist']['data']['auctions']

        goods_list = []

        for item in items:

            goods = {
                'name': item['raw_title'],
                'link': item['detail_url'],
                'price': item['view_price'],
                'shop': item['nick'],
                'location': item['item_loc'],
                'deal-cnt': item['view_sales'][:-3]

            }

            goods_list.append(goods)
            # 打印每个商品的信息
            print(goods)

        return goods_list




    def write_csv(self, goods_list):
        '''
        #生成csv文件
        '''

        with open('taobao.csv', 'w', encoding='UTF-8') as f:

            writer = csv.DictWriter(f, fieldnames=['name', 'price', 'shop', 'location', 'deal-cnt', 'link'])
            writer.writeheader()
            writer.writerows(goods_list)


if __name__ == '__main__':
    TaobaoJsonSpider()
