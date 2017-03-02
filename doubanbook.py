# -*- coding: utf-8 -*-
import scrapy
from Program.items import ProgramItem


class DoubanbookSpider(scrapy.Spider):
    name = "doubanbook"
    allowed_domains = ["book.douban.com"]
    start_urls = ['https://book.douban.com/tag/?view=cloud']

    def parse(self, response):
        book_list_group = response.xpath('//div[@class="article"]/div[2]/div')[0]
        book_list_urls = book_list_group.xpath('table/tbody/tr/td/a/@href').extract()
        for book_list in book_list_urls:
            yield scrapy.Request('https://book.douban.com' + book_list, callback=self.parse_book_list_detail,
                                 dont_filter=True, meta={
                    'book_list_name': book_list[5:],
                    'book_list_link': 'https://book.douban.com' + book_list
                })

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


        book_list_info = {
            'name': response.meta['book_list_name'],
            'books': [],
            'link': response.meta['book_list_link']
        }

        items = response.xpath('//li[@class="subject-item"]')
        for item in items:
            book_list_info['books'].append({
                'book_link': item.xpath('div[@class="info"]/h2/a/@href').extract()[0].strip(),
                'book_title': item.xpath('div[@class="info"]/h2/a/text()').extract()[0].strip(),
                'book_pub': item.css('.pub').xpath('text()').extract()[0].strip(),
                'book_rate': '少于10人评价' if item.css('.rating_nums') is None else item.css('.rating_nums').xpath('text()').extract()[0].strip(),

            })

            yield book_list_info
