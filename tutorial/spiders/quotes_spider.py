import scrapy
from pymongo import MongoClient
import time

timestamp = int(time.time())
client = MongoClient('localhost', 27017)
db = client['osc']
collection = db[str(timestamp)]


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.oschina.net/',
    ]

    def parse(self, response):
        for tab_page in response.css('div.tab-page'):
            for item in tab_page.css('div.item'):
                d = {
                    'url': item.css('a::attr(href)').get(),
                    'title': item.css('a::attr(title)').get(),
                    'date': item.css('div.item-extra').get()[24:29],
                }
                collection.insert(d)
