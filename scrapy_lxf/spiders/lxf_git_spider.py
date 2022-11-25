import scrapy


class QuotesSpider(scrapy.Spider):
    name = "lxf_git"
    start_urls = [
        'https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': '20',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)',
#        'USER_AGENT': 'https://developers.whatismybrowser.com/useragents/parse/288205-safari-ios-ipad-webkit',
        'COOKIES_ENABLE': 'False',
    }

#    def start_requests(self):
#        urls = [
#            'https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000',
#            'https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001373962845513aefd77a99f4145f0a2c7a7ca057e7570000',
#
#        ]
#        for url in urls:
#            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
#        page = response.url.split("/")[-2]
#        filename = 'lxf_git-{}.html'.format(page)
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file {}'.format(filename))

        title = response.css("h4::text").extract_first()
        body = response.css(".x-wiki-content.x-main-content p::text")[:-2].extract()

        with open('lxf_git/'+title, 'wb') as f:
            for p in body:
                f.write(p.encode('utf-8'))
                f.write('\n'.encode('utf-8'))
        self.log('Saved file {}'.format(title))

        for href in response.css('.uk-nav.uk-nav-side a::attr(href)'):
            yield response.follow(href, self.parse)
