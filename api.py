import uvicorn
from fastapi import FastAPI, Depends
from routes.user import user_router
from routes.diabetesRoute import diabetes_router
from model.userModel import User
from auth.authenticate import get_current_user

description = """
Ini adalah API untuk mencatat kondisi medis pengguna, dan memprediksi apakah pengguna terindikasi diabetes atau tidak."""

app = FastAPI()

@app.get("/")
def home():
    return {"Tugas Besar II3160 Teknologi Sistem Terintegrasi": "18220075 Faiza Kamilah"}

@app.get("/home")
def print_home(current_user:User = Depends(get_current_user)):
	return ("Selamat Datang!")

app.include_router(user_router)
app.include_router(diabetes_router)