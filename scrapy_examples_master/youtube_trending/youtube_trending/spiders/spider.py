import re
import json
from urllib.parse import urlparse
import urllib
import pdb


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from youtube_trending.items import *
# from misc.log import *
from misc.spider import CommonSpider


class youtube_trendingSpider(CommonSpider):
    name = "youtube_trending"
    allowed_domains = ["youtube.com"]
    start_urls = [
        "https://www.youtube.com/feed/trending",
    ]
    rules = [
        Rule(sle(allow=("feed/trending$")), callback='parse_1', follow=True),
    ]

    list_css_rules = { 
        '.yt-lockup-content': {
            'video_title': '.yt-lockup-title a::text',
            'author': '.yt-lockup-byline a::text',
        }   
    }   

    content_css_rules = { 
        'text': '#Cnt-Main-Article-QQ p *::text',
        'images': '#Cnt-Main-Article-QQ img::attr(src)',
        'images-desc': '#Cnt-Main-Article-QQ div p+ p::text',
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        print(json.dumps(x, ensure_ascii=False, indent=2))
        # pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, youtube_trendingItem)
