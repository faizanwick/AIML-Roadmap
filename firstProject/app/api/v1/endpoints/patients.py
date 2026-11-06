from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.repositories.patient_repository import PatientRepository
from app.services.patient_service import PatientService
from app.cores.exceptions import PatientNotFoundError, PatientAlreadyExistError

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

def get_patient_service() -> PatientService:
    repository = PatientRepository()
    return PatientService(repository)

ServiceDep = Annotated[PatientService, Depends(get_patient_service)]

@router.get("/", response_model=list[PatientResponse])
def get_patients(service : ServiceDep):
    return service.get_all_patient()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id : str, service : ServiceDep):
    try:
        return service.get_patient(patient_id)
    except PatientNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient Not Found")

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient : PatientCreate, service : ServiceDep):
    try:
        return service.create_patient(patient)
    except PatientAlreadyExistError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patient Already Exist")

@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id : str, change : PatientUpdate, service : ServiceDep):
    try:
        return service.update_patient(patient_id, change)
    except PatientNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient Not Found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id : str, service : ServiceDep):
    try:
        service.delete_patient(patient_id)
    except PatientNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient Not Found")  