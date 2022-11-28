from models import User
from pydantic import BaseModel
from mongoengine import connect
import json
import jwt
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()
connect(db="tst", host="localhost", port=27017)
JWT_SECRET = 'tubestst'
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.get("/")
def home():
    return{"Name":"Faiza Kamilah"}

@app.get("/getUsers")
def getUsers():
    users = json.loads(User.objects().to_json())

    return {"users": users}

class NewUser(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(new_user: NewUser):
    user = User(username = new_user.username,
                password = new_user.password)
    user.save()

    return {"message":"New user created"}