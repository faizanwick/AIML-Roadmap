from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import date

class TaskCreate(BaseModel):
    title : str
    description : str | None = None
    priority : Literal["low", "medium", "high"] = "medium"
    status : Literal["active", "pending", "completed"] = "pending"
    due_date : date | None = None
    user_id : int

class TaskReplace(BaseModel):
    title : str
    description : str | None = None
    priority : Literal["low", "medium", "high"]
    status : Literal["active", "pending", "completed"]
    due_date : date | None = None

class TaskUpdate(BaseModel):
    id : int | None = None
    title : str | None = None
    description : str | None = None
    priority : Literal["low", "medium", "high"] | None = None
    status : Literal["active", "pending", "completed"] | None = None
    due_date : date | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    description : str | None
    priority : Literal["low", "medium", "high"]
    status : Literal["active", "pending", "completed"]
    due_date : date | None