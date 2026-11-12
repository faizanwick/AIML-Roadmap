from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.user import User
from app.repositories.task_repo import TaskRepository
from app.schemas.task_schemas import TaskCreate, TaskReplace, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.api.v1.endpoints.auth import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_task_service(db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return TaskService(repository)


@router.get("/users")
def get_user(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    curr_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.get_all(user_id=curr_user.user_id)


@router.get("/task/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    curr_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.get_task(task_id, curr_user.user_id)


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    curr_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.create_task(task, curr_user.user_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskReplace,
    curr_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.update_task(task_id, task, curr_user.user_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def modify_task(
    task_id: int,
    task: TaskUpdate,
    curr_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.modify_task(task_id, task, curr_user.user_id)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    curr_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
):
    return service.delete_task(task_id, curr_user.user_id)