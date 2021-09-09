import scrapy
import sys
import time
import hashlib
import re
import urllib3
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['github']
collection = db['user']

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
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}


class QuotesSpider(scrapy.Spider):
    name = "github"
    start_urls = [
        'https://github.com/rajeevsrao?tab=followers',
    ]

    def parse(self, response):
        if float(re.findall(r"\d+\.?\d*", response.css('span.text-bold.color-text-primary')[0].get())[0]) > 0:
            for follower in response.css('a.d-inline-block.no-underline.mb-1::attr(href)'):
                d = {
                    'username': follower.get()[1:],
                    'url': response.urljoin(follower.get()),
                }

                collection.insert(d)

                next_link = "https://github.com/" + follower.get()[1:] + "?tab=followers"
                yield scrapy.Request(next_link, callback=self.parse, meta=proxy, headers=headers)
