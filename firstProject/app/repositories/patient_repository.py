import json
from pathlib import Path

from app.cores.config import settings

class PatientRepository:
    def __init__(self, file_path : Path | None = None):
        self.file_path = Path(file_path or settings.DATA_FILE)

    # Get all patient data
    def get_all(self) -> dict:
        if not self.file_path.exists():
            return {}

        with self.file_path.open("r") as f:
            return json.load(f)

    # Get specific patient data    
    def get_by_id(self, patient_id : str) -> dict:
        return self.get_all().get(patient_id)

    # Save data
    def save_all(self, data : dict) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_file = self.file_path.with_suffix(".tmp")

        with temp_file.open("w") as f:
            json.dump(data, f, indent=4)

        temp_file.replace(self.file_path)

    # Create patient
    def create(self, patient_id : str, patient : dict) -> None:
        data = self.get_all()
        data[patient_id] = patient
        self.save_all(data)

    # Update patient
    def update(self, patient_id : str, change : dict) -> None:
        data = self.get_all()
        data[patient_id].update(change)
        self.save_all(data)

    def delete(self, patient_id : str) -> None:
        data = self.get_all()
        del data[patient_id]
        self.save_all(data)

repository = PatientRepository()