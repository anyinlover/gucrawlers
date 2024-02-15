import re
import scrapy
from scrapy.utils.sitemap import Sitemap

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
        url = "https://www.oxfordlearnersdictionaries.com/sitemap/sitemap_topic.xml"
        yield scrapy.Request(url, self.parse_sitemap)

    def parse_sitemap(self, response):
        s = Sitemap(response.body)
        for entry in s:
            url = entry['loc']
            if re.fullmatch(r'https://www.oxfordlearnersdictionaries.com/topic/\w+', url):
                yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        topic = response.css("h1::text").get()
        lists = response.css("ul.top-g")
        for item in lists.css("li"):
            yield {
                "topic": topic,
                "word": item.css("a::text").get(),
                "url": item.css("a::attr(href)").get(),
                "pos": item.css("span.pos::text").get(),
                "belong": item.css("span.belong-to::text").get(),
            }
