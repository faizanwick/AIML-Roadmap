from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
    name : Annotated[str, Field(..., description="Patient Name", min_length=2)]
    city : Annotated[str, Field(..., description="Patient Name", min_length=2)]
    age : Annotated[int, Field(..., description="Patietn Age", gt=0)]
    gender : Annotated[Literal["male", "female", "Male", "Female"], Field(..., description="Gender")]
    height : Annotated[float, Field(..., description="Patient Height", gt=0, lt=250)]
    weight : Annotated[float, Field(..., description="Patient Height", gt=0, lt=250)]

class PatientCreate(Patient):
    id : Annotated[str, Field(..., min_length=1, examples=["1"])]

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt=0)]
    gender : Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None, gt=0)]
    weight : Annotated[Optional[float], Field(default=None, gt=0)]

class PatientResponse(Patient):
    id : str

    @computed_field
    @property
    def bmi(self) -> float:
        from app.utils.patient_utils import calculate_bmi
        return calculate_bmi(self.height, self.weight)

    @computed_field
    @property
    def bmi_verdict(self) -> str:
        from app.utils.patient_utils import get_bmi_verdict
        return get_bmi_verdict(self.bmi)