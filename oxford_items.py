import re
import scrapy
from scrapy.utils.sitemap import Sitemap
from scrapy_playwright.page import PageMethod


class TopicSpider(scrapy.Spider):
    name = "topic_spider"

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("DOWNLOAD_HANDLERS", {"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler"}, priority="spider")
        settings.set("TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor", priority="spider")
        settings.set("USER_AGENT", None, priority="spider")
        settings.set("PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT", 1000*1000, priority="spider")
    
    def start_requests(self):
        urls = ["https://www.oxfordlearnersdictionaries.com/sitemap/english/sitemap1.xml",
                "https://www.oxfordlearnersdictionaries.com/sitemap/english/sitemap2.xml",
                "https://www.oxfordlearnersdictionaries.com/sitemap/english/sitemap3.xml"]
        for url in urls:
            yield scrapy.Request(url, self.parse_sitemap)

        #url = "https://www.oxfordlearnersdictionaries.com/definition/english/cook_1"
        #yield scrapy.Request(url, meta={"playwright": True,"playwright_page_methods": [PageMethod('wait_for_selector', 'entryContent')]})
        #yield scrapy.Request(url, meta={"playwright": True})

    def parse_sitemap(self, response):
        s = Sitemap(response.body)
        for entry in s:
            url = entry['loc']
            #yield scrapy.Request(url, meta={"playwright": True,"playwright_page_methods": [PageMethod('wait_for_selector', 'entryContent')]})
            yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        #content = response.css("entryContent")
        filename = "items/" + response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
