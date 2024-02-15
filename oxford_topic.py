import re
from scrapy.spiders import SitemapSpider


class TopicSpider(SitemapSpider):
    name = "topic_spider"
    sitemap_urls = ["https://www.oxfordlearnersdictionaries.com/sitemap/sitemap_topic.xml"]

    def sitemap_filter(self, entries):
        for entry in entries:
            url = entry["loc"]
            if re.fullmatch(r'https://www.oxfordlearnersdictionaries.com/topic/\w+', url):
                yield entry 

    