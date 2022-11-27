from fastapi import FastAPI
from models import User
from mongoengine import connect
import json

app = FastAPI()
connect(db="tst", host="localhost", port=27017)

@app.get("/")
def home():
    return{"message":"Hello World!"}

@app.get("/getUsers")
def getUsers():
    users = json.loads(User.objects().to_json())

    return {"users": users}