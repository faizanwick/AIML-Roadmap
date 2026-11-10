# File commands
# Dir commands
# apt commands
# curl 
# ping
# wget
from fastapi import FastAPI, Depends, HTTPException

temp = FastAPI()

# Session (Engine)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.cores.config import settings

# Base
from sqlalchemy.orm import DeclarativeBase

# Task Table
from datetime import date
from sqlalchemy import Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker

# Schemas
from app.schemas.task_schemas import TaskCreate, TaskReplace, TaskUpdate, TaskResponse

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title : Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description : Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    priority : Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="medium"
    )

    status : Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="pending"
    )

    due_date : Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    # user_id : Mapped[int] = mapped_column(
    #     ForeignKey("users.user_id"),
    #     nullable=False
    # )

    # owner : Mapped["User"] = relationship(
    #     back_populates="tasks"
    # )

# class User(Base):
#     __tablename__ = "users"

#     user_id : Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#     )

#     name : Mapped[str] = mapped_column(
#         String(100),
#         nullable=False
#     )

#     email : Mapped[str] = mapped_column(
#         String(100),
#         nullable=False
#     )

#     tasks : Mapped[list["Task"]] = relationship(
#         back_populates="owner"
#     )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@temp.get("/")
def home():
    return {"message" : "FastAPI is running..."}

@temp.get("/tasks")
def get_tasks(db : Session = Depends(get_db)) -> list[TaskResponse]:
    return db.query(Task).all()

@temp.get("/tasks/{task_id}")
def get_task(task_id : int, db : Session = Depends(get_db)) -> TaskResponse:
    return db.get(Task, task_id)

@temp.post("/create")
def create_task(task : TaskCreate, db : Session = Depends(get_db)) -> TaskResponse:
    data = task.model_dump(mode="json")
    new_task = Task(**data)
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@temp.put("/replace/{task_id}")
def replace_task(task_id : int, task_data : TaskReplace, db : Session = Depends(get_db)) -> TaskResponse:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task Not Found")

    task_dict = task_data.model_dump(mode="json")
    for key, val in task_dict.items():
        setattr(task, key, val)

    db.commit()
    db.refresh(task)
    return task

@temp.delete("/delete/{task_id}")
def delete_task(task_id : int, db : Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task Not Found")
    
    db.delete(task)
    db.commit()

    return True