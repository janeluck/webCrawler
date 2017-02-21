import lxml.html
from multiprocessing.dummy import Pool
import requests
import csv


'''
多线程抓取豆瓣电影TOP250
'''

class MovieSpider(object):
    def __init__(self):
        self.url = 'https://movie.douban.com/top250?start=0&filter='
        self.page_dict = {}

    def run(self, page):
        html = self.get_source(page)
        self.get_page(page, html)


    def get_source(self, page):
        '''
        获取网页源信息
        '''
        url = 'https://movie.douban.com/top250?start={}&filter='.format(page * 25)
        return  requests.get(url).content

    def get_page(self, page, html):

        page_content = []
        selector = lxml.html.fromstring(html)
        movies = selector.xpath('//div[@class="info"]')

        for movie in movies:
            # 组织每一页的电影数据
            page_content.append(
                # 提取每个电影的标题, 链接, 演职人员, 评分
                {
                    'title': movie.xpath('div[@class="hd"]/a/span[@class="title"][1]/text()')[0].strip(),
                    'link': movie.xpath('div[@class="hd"]/a[1]/@href')[0].strip(),
                    'actor': movie.xpath('div[@class="bd"]/p[1]/text()')[0].strip(),
                    'rate': movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"][1]/text()')[0].strip()
                }
            )


        self.page_dict[page] = page_content

    def write_csv(self):

        #按页码排序
        content_list = sorted(self.page_dict.items(), key=lambda x: x[0])

        result = []

        for page, content in content_list:
            result.extend(content)

        # 生成csv文件
        with open('movie.csv', 'w', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'actor', 'link', 'rate'])
            writer.writeheader()
            writer.writerows(result)

if __name__ == '__main__':

    pool = Pool(10)
    movieSpider = MovieSpider()
    #抓取前10页
    pool.map(movieSpider.run, [x for x in range(0, 10)])
    movieSpider.write_csv()
    print('抓取完成!')


