from fastapi import APIRouter, FastAPI, HTTPException, Depends, Request ,status
from model.userModel import User, Token
from config.db import connect
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from auth.hash import Hash
from datetime import timedelta
from auth.jwt_handler import ACCESS_TOKEN_EXPIRE_MINUTES
from config.db import userDB
from auth.authenticate import get_current_user
import json

user_router = APIRouter()

def users_serializer(users) -> list:
    return [userDB(user) for user in users]


@user_router.get("/getUsers")
def read_root(current_user:User = Depends(get_current_user)):
	return {"data":"Ini udh terautentikasi"}
#def getUsers():
#    user = json.loads(User.objects().to_json())

#    return {"users": user}
@user_router.get("/users/me/", tags=['Auth'], response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


#async def register(new_user: User):
#    user = User(username = new_user.username,
#                password = new_user.password)
#    user.save()

#    return {"message":"New user created"}
@user_router.post("/register")
def create_user(request:User):
	hashed_pass = Hash.bcrypt(request.password)
	user_object = dict(request)
	user_object["password"] = hashed_pass
	if userDB.find_one({"username": request.username}):
		return {"Message": "Username already exist"}
	userDB.insert_one(user_object)
	# print(user)
	return {"User":"created"}

@user_router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
	user = userDB.find_one({"username":request.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
	if not Hash.verify(user["password"],request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
	access_token = create_access_token(data={"sub": user["username"] })
	return {"access_token": access_token, "token_type": "bearer"}
#def login(request:OAuth2PasswordRequestForm = Depends()):
#	user = userDB.find_one({"username":request.username})
#	if not user:
#		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
#	if not Hash.verify(user["password"],request.password):
#		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
#	access_token = create_access_token(data={"sub": user["username"] })
#	return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/token", tags=['Auth'], response_model=Token)
def get_user(db, username2: str):
    for user in db:
        if username2 == user.username:
            return user

def authenticate_user(user_db, username: str, password: str):
    user = get_user(User.objects(), username)
    if not user:
        return False
    #if not verify_password(password, user.hashed_password):
        #return False
    return user

#def user_serializer(user) -> dict:
#    return{
#        "username": User["username"],
#        "password": User["password"]
#    }

#def users_serializer(users) -> list:
#    return [user_serializer(user) for user in users]

#@user_router.get('/show_user')
#def show_user():
#    list_user = []
#    for user in users_serializer(userDB.find()):
#        list_user.append(user)
#    return list_user
@user_router.get('/show_user')
def show_user():
    list_user = []
    for user in users_serializer(userDB.find()):
        list_user.append(user)
    return list_user