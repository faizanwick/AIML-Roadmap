from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task

class TaskRepository:
    def __init__(self, db : Session):
        self.db = db

    def get_all(self):
        statement = select(Task)
        result = self.db.scalars(statement).all()
        return result

    def get_by_id(self, task_id : int):
        return self.db.get(Task, task_id)

    def create(self, task_data : dict):
        task = Task(**task_data)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def update(self, task_id : int, task_data : dict):
        task = self.db.get(Task, task_id)

        if task is None:
            return None
        for key, val in task_data.items():
            setattr(task, key, val)

        self.db.commit()
        self.db.refresh(task)
        return task

    def modify(self, task_id : int, task_data : dict):
        task = self.db.get(Task, task_id)

        if task is None:
            return None

        for key, val in task_data.items():
            setattr(task, key, val)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id : int):
        task = self.db.get(Task, task_id)

        if task is None:
            return None

        self.db.delete(task)
        self.db.commit()
        
        return True