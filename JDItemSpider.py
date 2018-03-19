import csv
import requests
from datetime import date


class JDItemSpider(object):
    '''
    通过关键字抓取淘宝商品(第一页)
    '''

    def __init__(self):
        self.run()

    def run(self):
        # keyword = self.get_input()
        result = self.get_source()
       # self.write_csv(keyword, result)

    def get_input(self):
        '''
        获取用户输入的关键字
        '''
        #return input('请输入要搜索的词:\n').strip()

    def get_source(self):
        '''
        发起搜索并获取json
        '''

        source = requests.get('http://item.jd.com/211934.html')



        print(source.content)
        return ''

    def write_csv(self, keyword, goods_list):
        '''
        生成csv文件
        '''

        with open(keyword + 'JD' + date.today().strftime('%Y-%m-%d') + '.csv', 'w', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'price', 'images', 'content'])
            writer.writeheader()
            writer.writerows(goods_list)


if __name__ == '__main__':
    JDItemSpider()

