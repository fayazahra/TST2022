from pydantic import BaseModel
import pickle 
#import sklearn

diabetes_model = pickle.load(open('./diabetes_model.sav','rb'))


class model_input(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int
    class Config:
        schema_extra = {
            "diabetes_demo" : {
                "preg": 6,
                "glu": 148,
                "bp": 72,
                "skin": 35,
                "ins": 0,
                "bmi": 33.6,
                "dpf": 0.627,
                "age": 50
            }
        }