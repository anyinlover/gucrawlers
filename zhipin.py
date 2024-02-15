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
        settings.set("PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT", 100*1000, priority="spider")
    
    def start_requests(self):
        url = "https://www.zhipin.com/web/geek/job?city=101210100&position=101310&page=1"
        yield scrapy.Request(url, meta={"playwright": True, "playwright_page_methods": [PageMethod('wait_for_selector', 'ul.job-list-box')]})
    
    def parse(self, response):
        if "job_detail" in response.url:
            yield {
                "title": response.css("h1::text").get(),
                "salary": response.css("span.salary::text").get(),
                "experience": response.css("span.text-desc.text-experiece::text").get(),
                "degree": response.css("span.text-desc.text-degree::text").get(),
                "description": response.css("div.job-sec-text::text").get(),
                "keywords": response.css("ul.job-keyword-list::text").getAll(),
                "update": response.css("p.gray::text").get()[4:],
                "company": response.css("div.company-info::text").get(),
                "address": response.css("div.location-address::text").get()
            }
        
        else:
            print("--------------Im----------------")
            list = response.css("ul.job-list-box")
            print(len(list.css("li")))
            for job in list.css("li"):
                url = "https://www.zhipin.com" + job.css("a::attr(href)").get()
                yield scrapy.Request(url, meta={"playwright": True})
            
            # button = response.css("i.ui-icon-arrow-right").get().root()
            # if not button.css(".disabled"):
            #     url = response.url[:-1] + str(int(response.url[-1])+1)
            #     yield scrapy.Request(url, meta={"playwright": True})



