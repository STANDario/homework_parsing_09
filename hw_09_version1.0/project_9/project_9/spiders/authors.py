import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response, *_):
        for q in response.xpath("/html//div[@class='quote']"):
            author = q.xpath("span/a/@href").get()
            yield response.follow(url=self.start_urls[0] + author, callback=self.nested_parse_author)  # Переходить на url який ми вказали та виконує з ним функцію яка написана в callback
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response):
        author = response.xpath("/html//div[@class='author-details']")
        fullname = author.xpath("h3[@class='author-title']/text()").get().strip()
        date_born = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        location_born = author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        bio = author.xpath("div[@class='author-description']/text()").get().strip()
        yield {
            "fullname": fullname,
            "born_date": date_born,
            "born_location": location_born,
            "description": bio
        }
