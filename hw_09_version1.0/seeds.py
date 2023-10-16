import json

from src.models import Author, Quote
from src.db import connect


with open(r"project_9/authors.json", "r", encoding="utf-8") as fd:
    authors = json.load(fd)

with open(r"project_9/quotes.json", "r", encoding="utf-8") as fd:
    quotes = json.load(fd)


if __name__ == '__main__':

    for author in authors:
        author_to_add = Author(fullname=author.get("fullname"), born_date=author.get("born_date"),
                               born_location=author.get("born_location"), description=author.get("description")).save()
        for quote in quotes:
            if quote.get("author") == author.get("fullname"):
                quote_for_add = Quote(tags=quote.get("tags"), author=author_to_add, quote=quote.get("quote")).save()

    # Author.objects().delete()
    # Quote.objects().delete()
