from mongoengine import Document, CASCADE
from mongoengine.fields import StringField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField(max_length=100)
    born_date = StringField(max_length=100)
    born_location = StringField(max_length=300)
    description = StringField()


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
