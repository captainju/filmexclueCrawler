from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from filmexclue.items import filmexclueItem

class filmexclueSpider(BaseSpider):
    name = "filmexclue"
    allowed_domains = ["fs-exclue.com/"]
    start_urls = [
        "http://www.fs-exclue.com/",
        "http://www.fs-exclue.com/page/2/"
    ]

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        posts = hxs.select("//div[@class='post']")
        for post in posts:
            item = filmexclueItem()
            url = post.select('descendant::h2/a/@href').extract()
            title = post.select('descendant::h2/a/text()').extract()
            desc = post.select('descendant::i/text()').extract()
            if desc == []:
                desc = post.select('descendant::em/text()').extract()
            imgurl = post.select("descendant::div[@class='entry']/descendant::img/@src").extract()
            item['url'] = url
            item['title'] = title
            item['desc'] = desc
            item['imgurl'] = imgurl
            items.append(item)
        return items