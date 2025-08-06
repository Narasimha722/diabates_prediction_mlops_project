from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    Pregnancies: int = Form(...),
    Glucose: float = Form(...),
    BloodPressure: float = Form(...),
    BMI: float = Form(...),
    Age: int = Form(...)
):
    input_data = np.array([[Pregnancies, Glucose, BloodPressure, BMI, Age]])
    prediction = model.predict(input_data)[0]
    result = "Diabetic" if prediction else "Not Diabetic"
    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result
    })
