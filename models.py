from mongoengine import Document, StringField, IntField, ListField


class User(Document):
    id = IntField(max_length=32)
    username = StringField()
    password = StringField()
