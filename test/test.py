from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id : int
    name : str
    email : str
    salary : int

class PutEmp(BaseModel):
    name : str
    email : str
    salary : int

employee = []

@app.get("/")
def home():
    return {"message" : "FastAPI is Running..."}

@app.post("/create")
def create_employee(emp : Employee):
    employee.append(emp)
    return emp

@app.get("/employee")
def get_all():
    return employee

@app.get("/employee/{emp_id}")
def get_emp(emp_id : int):
    for x in employee:
        if emp_id == x.id:
            return x
    else:
        raise HTTPException(status_code=404, detail="Emp not found")

@app.put("/{emp_id}")
def put_emp(emp_id : int, emp : PutEmp):
    new_data = emp
    for x in employee:
        if emp_id == x.id:
            changes = []
            if new_data.email != x.email:
                x.email = new_data.email
                changes.append("Email changed to " + str(new_data.email))

            if new_data.salary != x.salary:
                x.salary = new_data.salary
                changes.append("Salara change to " + str(new_data.salary))

            if not changes:
                return {"message" : "No updates"}
            else:
                return {"Changes" : changes}
        else:
            raise HTTPException(status_code=404, detail="Emp not found")

@app.get("/sal")
def get_sal():
    salaries = []
    for x in employee:
        if x.salary > 20000:
            salaries.append(x)

    return salaries