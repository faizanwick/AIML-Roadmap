from app.repositories.task_repo import TaskRepository
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskReplace, TaskResponse
from fastapi import HTTPException

class TaskService:
    def __init__(self, repository : TaskRepository):
        self.repository = repository

    def get_all(self) -> list[TaskResponse]:
        tasks = self.repository.get_all()
        return [
            TaskResponse.model_validate(task)
            for task in tasks
        ]

    def get_task(self, task_id : str) -> TaskResponse:
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task Not Found")
        return TaskResponse.model_validate(task)

    def create_task(self, task : TaskCreate) -> TaskResponse:
        task_data = task.model_dump()
        new_task = self.repository.create(task_data)
        return TaskResponse.model_validate(new_task)
    
    def update_task(self, task_id : str, task : TaskReplace) -> TaskResponse:
        updated_task = self.repository.update(task_id, task.model_dump())
        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task Not Found")
        return TaskResponse.model_validate(updated_task)

    def modify_task(self, task_id : str, task : TaskUpdate) -> TaskResponse:
        task_data = task.model_dump(exclude_unset=True)
        updated_task = self.repository.modify(task_id, task_data)
        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task Not Found")
        return TaskResponse.model_validate(updated_task)


    def delete_task(self, task_id : str):
        deleted = self.repository.delete(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task Not Found")
        return {"message" : "Task Deleted"}

    def get_user_tasks(self, user_id : int):
        tasks = self.repository.get_all_user_task(user_id)
        # return [TaskResponse.model_validate(task) for task in tasks]
        return [task for task in tasks]