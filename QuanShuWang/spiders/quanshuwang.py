# -*- coding: utf-8 -*-
import scrapy
from ..items import QuanshuwangItem

class QuanshuwangSpider(scrapy.Spider):
    name = 'quanshuwang'
    allowed_domains = ['www.quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/']

    def parse(self, response):
        item = QuanshuwangItem()
        links = response.xpath("//ul[@class='channel-nav-list']/li/a")
        for link in links:
            category = link.xpath("./text()").get().strip()
            url = link.xpath("./@href").get()
            item["category"] = category
            yield scrapy.Request(url=url, callback=self.parse_category_page, meta={"item": item})

    def parse_category_page(self, response):
        base_url = response.url.split("_")[0] + "_%d.html"
        max_page = int(response.xpath("//div[@id='pagelink']/a[last()]/text()").get())
        for page in range(1, max_page + 1):
            url = base_url % page
            yield scrapy.Request(url=url, callback=self.parse_page_info, meta={"item": response.meta["item"]})

    def parse_page_info(self, response):
        infos = response.xpath("//ul[@class='seeWell cf']/li")
        for info in infos:
            url = info.xpath("./a/@href").get()
            yield scrapy.Request(url=url, callback=self.parse_novel_info, meta={"item": response.meta["item"]})

    def parse_novel_info(self, response):
        item = response.meta["item"]
        item["bookUrl"] = response.url
        item["name"] = response.xpath("//div[@class='b-info']/h1/text()").get().strip()
        item["author"] = response.xpath("//div[@class='bookDetail']/dl[2]/dd/text()").get().strip()
        item["status"] = response.xpath("//div[@class='bookDetail']/dl[1]/dd/text()").get().strip()
        item["introduction"] = response.xpath("//div[@id='waa']/text()").get().strip()
        url = response.xpath("//div[@class='b-oper']/a[1]/@href").get()
        scrapy.Request(url=url, callback=self.parse_novel_chapter, meta={"item": item})

    def parse_novel_chapter(self, response):
        item = response.meta["item"]
        chapters = response.xpath("//div[@class='clearfix dirconone']/li/a")
        chapters_list = []
        for chapter in chapters:
            chapter_name = chapter.xpath("./a/text()").get().strip()
            chapter_url = chapter.xpath("./a/@href").get().strip()

            chapters_list.append((chapter_name, chapter_url))

        item["chapter_info"] = chapters_list
        return item





