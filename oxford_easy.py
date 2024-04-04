import re
import scrapy
from scrapy.utils.sitemap import Sitemap


class TopicSpider(scrapy.Spider):
    name = "topic_spider"

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0", priority="spider")
    
    def start_requests(self):
        urls = ["https://www.oxfordlearnersdictionaries.com/sitemap/english/sitemap1.xml",
                "https://www.oxfordlearnersdictionaries.com/sitemap/english/sitemap2.xml",
                "https://www.oxfordlearnersdictionaries.com/sitemap/english/sitemap3.xml"]
        for url in urls:
            yield scrapy.Request(url, self.parse_sitemap)


    def parse_sitemap(self, response):
        s = Sitemap(response.body)
        for entry in s:
            url = entry['loc']
            yield scrapy.Request(url)

    def parse(self, response):
        filename = "items/" + response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
