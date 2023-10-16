import json

from src.models import Authors, Quotes
from src.db import connect


with open(r"authors.json", "r", encoding="utf-8") as fd:
    authors = json.load(fd)

with open(r"quotes.json", "r", encoding="utf-8") as fd:
    quotes = json.load(fd)


if __name__ == '__main__':

    for author in authors:
        author_to_add = Authors(fullname=author.get("fullname"), born_date=author.get("date_born"),
                               born_location=author.get("location_born"), description=author.get("bio")).save()
        for quote in quotes:
            if quote.get("author") == author.get("fullname"):
                quote_for_add = Quotes(tags=quote.get("keywords"), author=author_to_add, quote=quote.get("quote")).save()

    # Authors.objects().delete()
    # Quotes.objects().delete()
