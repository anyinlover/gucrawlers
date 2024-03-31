import scrapy
from scrapy_playwright.page import PageMethod


class Oxford3000Spider(scrapy.Spider):
    name = "oxford3000"

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("DOWNLOAD_HANDLERS", {"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler"}, priority="spider")
        settings.set("TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor", priority="spider")
        settings.set("USER_AGENT", None, priority="spider")
        settings.set("PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT", 1000*1000, priority="spider")
    
    def start_requests(self):
        url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
        yield scrapy.Request(url, meta={"playwright": True, "playwright_page_methods": [PageMethod('wait_for_selector', 'ul.top-g')]})
    
    def parse(self, response):
        lists = response.css("ul.top-g")
        for item in lists.css("li"):
            yield {
                "word": item.css("a::text").get(),
                "url": item.css("a::attr(href)").get(),
                "pos": item.css("span.pos::text").get(),
                "ox3000": item.css("::attr(data-ox3000)").get(),
                "ox5000": item.css("::attr(data-ox5000)").get()
            }
