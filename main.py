import json
import pickle
import uvicorn
#from server.auth.jwt_handler import verify_token
#import sklearn
from models import User as UserDB
from models import User, model_input
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from mongoengine import connect, Document, StringField, IntField
from pymongo import MongoClient
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

connect = MongoClient('mongodb+srv://asteresrh:F4iruzzz@tubestst.1iohpll.mongodb.net/test')
db = connect.tst
user123 = db['user']

SECRET_KEY = "tubestst"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.get("/")
def home():
    return {"Name": "Faiza"}

@app.get("/getUsers")
def getUsers():
    user = json.loads(User.objects().to_json())

    return {"users": user}

@app.post("/register")
def register(new_user: User):
    user = User(username = new_user.username,
                password = new_user.password)
    user.save()

    return {"message":"New user created"}

#user_db = {
#    "cobates": {
#        "username": "cobates",
#        "hashed_password": "$2b$12$S7PXtKLxl/QScidl0bCA4OEXvhDOgDCRf0QUpLuV1Z0n6m2HAVdoe",
#        "disabled": False,
#    }
#}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

#def get_password_hash(password):
    #return pwd_context.hash(password)

def get_user(db, username: str):
    for user in db:
        if username == user.username:
            return user

def authenticate_user(user_db, username: str, password: str):
    user = get_user(User.objects(), username)
    if not user:
        return False
    #if not verify_password(password, user.hashed_password):
        #return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print (payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(User.objects(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return {"user": user }

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    #if current_user.disabled:
        #raise HTTPException(status_code=400, detail="Inactive user")

    return current_user

@app.post("/token", tags=['Auth'], response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(User.objects, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", tags=['Auth'], response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

#loading model
diabetes_model = pickle.load(open('diabetes_model.sav','rb'))

@app.post('/Diabetes_Prediction')
def diabetes_pred(input_parameter : model_input):

    input_data = input_parameter.json()
    input_dictionary = json.loads(input_data)

    preg = input_dictionary['Pregnancies']
    glu = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    skin = input_dictionary['SkinThickness']
    ins = input_dictionary['Insulin']
    bmi = input_dictionary['BMI']
    dpf = input_dictionary['DiabetesPedigreeFunction']
    age = input_dictionary['Age']

    input_list = [preg, glu, bp, skin, ins, bmi, dpf, age]

    prediction = diabetes_model.predict([input_list])

    if (prediction[0] == 0):
        return 'Not Diabetic'
    else:
        return 'Diabetic'



#if __name__ == "__main__":
#  uvicorn.run("main:app", host="0.0.0.0", reload=True, port="8080")