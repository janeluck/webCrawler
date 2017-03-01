# -*- coding: utf-8 -*-
import scrapy
from Program.items import ProgramItem


class DoubanbookSpider(scrapy.Spider):
    name = "doubanbook"
    allowed_domains = ["book.douban.com/tag"]
    #start_urls = ['https://book.douban.com/tag/']

    def parse(self, response):
        with open('douban.txt', 'w') as f:
            f.write(response.text)

        book_list_group = response.xpath('//div[@class="article"]/div[2]/div')

        book_list_urls = []
        for book_group in book_list_group:
            # print({
            #     'book_group_title': book_group.xpath('a[@class="tag-title-wrapper"]/@name').extract()[0],
            #    # 'book_lists': book_group.xpath('table/tbody/tr/td/a/@href').extract(),
            # })
            book_list_urls.extend(book_group.xpath('table/tbody/tr/td/a/@href').extract())

        for book_list in book_list_urls:
            yield scrapy.Request('https://book.douban.com' + book_list, callback=self.parse_book_list_detail)


            # item = ProgramItem()
            # item['book_list_title'] = book_list.xpath('header/h3/a/text()').extract()[0]
            # item['book_number'] = book_list.xpath('p/a/text()').extract()[0]
            # book_list_url = book_list.xpath('header/h3/a/@href').extract()[0]
            # yield scrapy.Request(self.url + book_list_url, callback=self.parse_book_list_detail, meta={'item': item})

    def parse_book_list_detail(self, response):
        # item = response.meta['item']
        # summary = response.xpath('//div[@id="list-description"]/p/text()').extract()
        # item['book_list_summary'] = '\n'.join(summary)
        # yield item #将item提交给pipelines处理
        items = response.xpath('//li[@class="subject-item"]')
        print(items)
        print('11111111111111111111111')
        for item in items:
            print({
                'book_title': item.xpath('div[@class="info"]/h2/a/text()').extract()[0]
            })
            yield  item