from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.cores.exceptions import PatientNotFoundError, PatientAlreadyExistError

class PatientService:
    def __init__(self, repository : PatientRepository):
        self.repository = repository

    # Retrive patients from repository
    def get_all_patient(self) -> list[PatientResponse]:
        data = self.repository.get_all()

        return [
            PatientResponse(id=patient_id, **patient)
            for patient_id, patient in data.items()
        ]

    # Retrive specific patient
    def get_patient(self, patient_id : str) -> PatientResponse:
        patient = self.repository.get_by_id(patient_id)

        if patient is None:
            raise PatientNotFoundError()

        return PatientResponse(id=patient_id, **patient)

    # Create a patient
    def create_patient(self, patient : PatientCreate) -> PatientResponse:
        if self.repository.get_by_id(patient.id) is not None:
            raise PatientAlreadyExistError()

        data = patient.model_dump(exclude=["id"])

        self.repository.create(patient.id, data)

        return PatientResponse(id=patient.id, **data)

    # Update patient
    def update_patient(self, patient_id : str, change : PatientUpdate) -> PatientResponse:
        existing  = self.repository.get_by_id(patient_id)

        if existing is None:
            raise PatientNotFoundError()

        updates = change.model_dump(exclude_unset=True)

        updated = {**existing, **updates}

        patient = PatientResponse(id=patient_id, **updated)

        self.repository.update(patient_id, updates)

        return patient

    # Delete patient
    def delete_patient(self, patient_id : str):
        if self.repository.get_by_id(patient_id) is None:
            raise PatientNotFoundError()

        self.repository.delete(patient_id)
        return {"message" : "Patient Deleted"}