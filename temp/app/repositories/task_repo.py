from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int):
        statement = select(Task).where(Task.user_id == user_id)
        return self.db.scalars(statement).all()

    def get_by_id(self, task_id: int, user_id: int):
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        return self.db.scalars(statement).first()

    def create(self, task_data: dict):
        task = Task(**task_data)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def update(self, task_id: int, task_data: dict, user_id: int):
        task = self.get_by_id(task_id, user_id)

        if task is None:
            return None

        # Ownership is controlled by the authenticated user, never by request data.
        task_data.pop("user_id", None)

        for key, val in task_data.items():
            setattr(task, key, val)

        self.db.commit()
        self.db.refresh(task)
        return task

    def modify(self, task_id: int, task_data: dict, user_id: int):
        task = self.get_by_id(task_id, user_id)

        if task is None:
            return None

        # Do not allow PATCH to transfer a task to another user.
        task_data.pop("user_id", None)

        for key, val in task_data.items():
            setattr(task, key, val)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int, user_id: int):
        task = self.get_by_id(task_id, user_id)

        if task is None:
            return False

        self.db.delete(task)
        self.db.commit()

        return True

    def get_all_user_task(self, user_id: int):
        statement = select(Task).where(Task.user_id == user_id)
        return self.db.scalars(statement).all()
