from fastapi import APIRouter, Depends
from app.repositories.task_repo import TaskRepository
from app.services.task_service import TaskService
from typing import Annotated
from app.schemas.task_schemas import TaskCreate, TaskReplace, TaskUpdate, TaskResponse
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.user import User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def get_task_service(db : Session = Depends(get_db)):
    repository = TaskRepository(db)
    return TaskService(repository)

@router.get("/users")
def get_user(db : Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(service : TaskService = Depends(get_task_service)):
    return service.get_all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id : int, service : TaskService = Depends(get_task_service)):
    return service.get_task(task_id)

@router.post("/", response_model=TaskResponse)
def create_task(task : TaskCreate, service : TaskService = Depends(get_task_service)):
    return service.create_task(task)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id : int, task : TaskReplace, service : TaskService = Depends(get_task_service)):
    return service.update_task(task_id, task)

@router.patch("/{task_id}", response_model=TaskResponse)
def modify_task(task_id : int, task : TaskUpdate, service : TaskService = Depends(get_task_service)):
    return service.modify_task(task_id, task)

@router.delete("/{task_id}")
def delete_task(task_id : int, service : TaskService = Depends(get_task_service)):
    return service.delete_task(task_id)