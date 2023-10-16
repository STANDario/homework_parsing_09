import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response, *_):
        for q in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": q.xpath("div[@class='tags']/a[@class='tag']/text()").extract(),
                "author": q.xpath("span/small[@class='author']/text()").get().strip(),
                "quote": q.xpath("span[@class='text']/text()").get().strip(),
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(self.start_urls[0] + next_link)
