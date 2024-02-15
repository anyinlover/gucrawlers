import scrapy

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
        url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford-phrase-list"
        yield scrapy.Request(url, meta={"playwright": True})
    
    def parse(self, response):
        lists = response.css("ul.top-g")
        for item in lists.css("li"):
            yield {
                "phrase": item.css("a::text").get(),
                "url": item.css("a::attr(href)").get(),
                "list": item.css("::attr(data-oxford_phrase_list)").get(),
            }
