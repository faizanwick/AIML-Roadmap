from fastapi import HTTPException
from app.repositories.task_repo import TaskRepository
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskReplace, TaskResponse


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all(self, user_id: int) -> list[TaskResponse]:
        tasks = self.repository.get_all(user_id)
        return [
            TaskResponse.model_validate(task)
            for task in tasks
        ]

    def get_task(self, task_id: int, user_id: int) -> TaskResponse:
        task = self.repository.get_by_id(task_id, user_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task Not Found")

        return TaskResponse.model_validate(task)

    def create_task(self, task: TaskCreate, user_id: int) -> TaskResponse:
        task_data = task.model_dump()
        # Never trust a user_id supplied by the client.
        task_data["user_id"] = user_id

        new_task = self.repository.create(task_data)
        return TaskResponse.model_validate(new_task)

    def update_task(
        self,
        task_id: int,
        task: TaskReplace,
        user_id: int
    ) -> TaskResponse:
        task_data = task.model_dump()
        updated_task = self.repository.update(task_id, task_data, user_id)

        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task Not Found")

        return TaskResponse.model_validate(updated_task)

    def modify_task(
        self,
        task_id: int,
        task: TaskUpdate,
        user_id: int
    ) -> TaskResponse:
        task_data = task.model_dump(exclude_unset=True)
        updated_task = self.repository.modify(task_id, task_data, user_id)

        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task Not Found")

        return TaskResponse.model_validate(updated_task)

    def delete_task(self, task_id: int, user_id: int):
        deleted = self.repository.delete(task_id, user_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Task Not Found")

        return {"message": "Task Deleted"}

    def get_user_tasks(self, user_id: int) -> list[TaskResponse]:
        tasks = self.repository.get_all_user_task(user_id)
        return [TaskResponse.model_validate(task) for task in tasks]
