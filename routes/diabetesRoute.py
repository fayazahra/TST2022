import json
from fastapi import APIRouter, FastAPI, HTTPException, Depends, Request,status
from model.userModel import User, Token
from config.db import connect
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from auth.hash import Hash
from model.diabetesModel import model_input, diabetes_model
from auth.authenticate import get_current_user
from model.diabetesModel import diabetes2_serializer
from config.db import diabetesDB

diabetes_router = APIRouter()

#@diabetes_router.get("/Diabeete")
#async def get_diabetes(current_user:User = Depends(get_current_user)):
#    house = diabetes2_serializer(diabetesDB.find())
#    return {"status": "ok", "data": house}
#@diabetes_router.get('/')
#def 

@diabetes_router.post('/Diabetes_Prediction')
def diabetes_pred(input_parameter : model_input, current_user:User = Depends(get_current_user)):

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
        return 'This Person is Not Diabetic'
    else:
        return 'This Person is Diabetic'


#@diabetes_router.get("/Diabetes/filter")
#async def get_filtered_patient(input_parameter: model_input, current_user:User = Depends(get_current_user)):
#    print("TESSS")
#    return carSchema.filter_mobil(nama_mobil, odo_min, odo_max, tahun_min, tahun_max, transmisi, harga_min, harga_max)
