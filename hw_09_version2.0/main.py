import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class QuoteItem(Item):
    keywords = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    date_born = Field()
    location_born = Field()
    bio = Field()


class QuotesPipLine:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append({
                "fullname": adapter["fullname"],
                "date_born": adapter["date_born"],
                "location_born": adapter["location_born"],
                "bio": adapter["bio"]
            })
        if "quote" in adapter.keys():
            self.quotes.append({
                "keywords": adapter["keywords"][0],
                "author": adapter["author"][0],
                "quote": adapter["quote"]
            })
        return item

    def close_spider(self, spider):    # PIPELINES його викличе після того як spider закриється
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False)
        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False)


class QuotesSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"ITEM_PIPELINES": {QuotesPipLine: 300}}        # Те що ми раніше розкоментовували в settings.py для перехоплення даних
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):  # noqa
        for quote in response.xpath("/html//div[@class='quote']"):
            keywords = quote.xpath("div[@class='tags']/a/text()").extract(),
            author = quote.xpath("span/small/text()").get().strip(),
            q = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(keywords=keywords, author=author, quote=q)
            yield response.follow(url=self.start_urls[0] + quote.xpath("span/a/@href").get(), callback=self.nested_parse_author)  # З url що ми передали виконай callback

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response):  # noqa
        author = response.xpath("/html//div[@class='author-details']")
        fullname = author.xpath("h3[@class='author-title']/text()").get().strip()
        date_born = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        location_born = author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        bio = author.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorItem(fullname=fullname, date_born=date_born, location_born=location_born, bio=bio)


process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
