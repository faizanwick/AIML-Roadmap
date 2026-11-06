from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="Patient ID", examples=["1"])]
    name : Annotated[str, Field(..., description="Patient Name", examples=["Red John"])]
    city : Annotated[str, Field(..., description="Patient City", examples=["Hyd"])]
    age : Annotated[int, Field(..., description="Patient Age", examples=["25"], gt=0, lt=100)]
    gender : Annotated[Literal["male", "female"], Field(..., description="Gender", examples=["male"])]
    height : Annotated[float, Field(..., description="Patient Height in cm", examples=["150"], gt=0, lt=250)]
    weight : Annotated[float, Field(..., description="Patient Weight in kgs", examples=["60"], gt=0, lt=250)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt=0)]
    gender : Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None, gt=0)]
    weight : Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def hello():
    return {"message" : "Hello world again!"}

@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id : str = Path(description="Patient ID", examples=["1", "2"])):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return data[patient_id]

@app.get("/sort")
def sorting(sort_by : Literal["height", "weight", "bmi"] = Query(description="Sort data by Height, Weight or BMI"), order_by : Literal["asc", "desc"] = Query(description="Order data in Ascending or Descending")):
    data = load_data()

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=order_by == "desc")

    return sorted_data

@app.post("/create")
def create_patient(patient : Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")

    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={"message" : "Patient Added Successfully"})

@app.put("/edit/{patient_id}")
def update_patient(patient_id : str, patient_update : PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    exist_dict = data[patient_id]

    updated_info = patient_update.model_dump(exclude_unset=True)

    for key, val in updated_info.items():
        exist_dict[key] = val

    data[patient_id] = exist_dict

    save_data(data)

    return JSONResponse(status_code=200, content={"message" : "Patient Updated Successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message" : "Patient Deleted"})