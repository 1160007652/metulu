# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from urllib import parse
from meitulu.items import MeituluItem
from meitulu.utils.common import get_md5

class MetuluSpider(scrapy.Spider):
    name = 'metulu'
    dont_filter = True
    allowed_domains = ["www.meitulu.com"]
    start_urls = ["https://www.meitulu.com/guochan/"]

    def parse(self, response):
        #提取下一页 翻页爬虫 地址
        page_down = response.xpath("//div[@id='pages']/a[last()]/@href").extract_first('')
        yield Request(url=parse.urljoin(response.url,page_down), callback=self.parse)

        # 提取详情数据的 url
        post_urls = response.xpath("//div[@class='boxs']/ul/li/a/@href").extract()
        for post_url in post_urls:
            yield Request(url=post_url, callback=self.parse_detaild)

    def parse_detaild(self, response):
        meitulu = MeituluItem()
        # 提取列表详情数据 选择器
        title = response.xpath("//div[@class='weizhi']/h1/text()").extract_first('')
        info = response.xpath("//div[@class='c_l']/p/text()").extract()[1:]
        message = response.xpath("//p[@class='buchongshuoming']/text()").extract_first('')
        pirc_srcs = response.xpath("//div[@class='content']/center/img/@src").extract()
        #pirc_src = response.xpath("//div[@class='content']/center/img/@src").extract_first('')
        page_down = response.xpath("//div[@id='pages']/a[last()]/@href").extract_first('')
        yield Request(url=parse.urljoin(response.url,page_down), callback=self.parse_detaild)

        meitulu["title"] = title
        meitulu["info"] = info
        meitulu["message"] = message
        meitulu["pirc_srcs"] = pirc_srcs
        meitulu["meitu_id"] = get_md5(pirc_srcs[0])
        yield meitulu
