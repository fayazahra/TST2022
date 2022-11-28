from mongoengine import Document, StringField, IntField, ListField

class User(Document):
    #id = IntField(max_length=32)
    #_id = ObjectId()
    username = StringField()
    password = StringField()
    meta={'allow_inheritance':True}