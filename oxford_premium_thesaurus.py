import re
import scrapy
from scrapy.utils.sitemap import Sitemap


class TopicSpider(scrapy.Spider):
    name = "topic_spider"

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0", priority="spider")
        settings.set("CONCURRENT_REQUESTS", 1000, priority="spider")
    
    def start_requests(self):
        login_url = "https://premium.oxforddictionaries.com/account/loginLibraryCard?acc_id=67833&library_card=H3265481"
        yield scrapy.Request(login_url, self.start_scrap)


    def start_scrap(self, response):
        sitemap_url = "https://premium.oxforddictionaries.com/sitemap/english-thesaurus/sitemap1.xml"

        yield scrapy.Request(sitemap_url, self.parse_sitemap)

    def parse_sitemap(self, response):
        s = Sitemap(response.body)
        for entry in s:
            url = entry['loc']
            yield scrapy.Request(url)

    def parse(self, response):
        filename = "thesaurus/" + response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
