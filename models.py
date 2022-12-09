#from mongoengine import Document, StringField, IntField, ListField
#from pydantic import BaseModel
from pydantic import BaseModel

#class User(BaseModel):
#    username: str
#    password: str
#class User(Document):
    #id = IntField(max_length=32)
    #_id = ObjectId()
    #username = StringField()
    #password = StringField()
    #meta={'allow_inheritance':True}

class User(BaseModel):
    username: str
    password: str

class model_input(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int