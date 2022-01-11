import scrapy
import sys
import time
import hashlib
import re
from scrapy.selector import Selector
import urllib3
import urllib
from pymongo import MongoClient
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
csv = pd.read_csv('/home/csdn/Downloads/scrapy_tutorial/tutorial/spiders/csv_merge.csv')

project_url = list(csv['术语'])
for i in range(len(project_url)):
    project_url[i] = "https://baike.baidu.com/item/" + str(project_url[i])


client = MongoClient('localhost', 27017)
db = client['github']
collection = db['user4']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_version = sys.version_info

is_python3 = (_version[0] == 3)

orderno = "ZF20219881550F64bH"
secret = "4a1536a5560b4459bcdf6b46e9928b47"

ip = "forward.xdaili.cn"
port = "80"

ip_port = ip + ":" + port

timestamp = str(int(time.time()))
string = ""
string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

if is_python3:
    string = string.encode()

md5_string = hashlib.md5(string).hexdigest()
sign = md5_string.upper()
# print(sign)
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

# print(auth)
proxy = {"http": "http://" + ip_port, "https": "http://" + ip_port}
headers = {"Proxy-Authorization": auth,
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


class QuotesSpider(scrapy.Spider):
    name = "baidu1"
    start_urls = project_url

    def parse(self, response):
        selector = Selector(response)
        title = selector.xpath('//div/dl/dd/h1/text()').extract_first()
        content = selector.xpath('//html').extract()
        basic_introduction_list = selector.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()').extract()
        basic_introduction = ''.join([item.strip('\n') for item in basic_introduction_list])

        d = {
                'title': title,
                'basic_introduction': basic_introduction
            }
        collection.insert(d)
