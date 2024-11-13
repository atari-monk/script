import os
from shared.json_repository import JSONRepository
from shared.json_file_storage import JSONFileStorage
from commands.log_project.lib.config import DB
from commands.log_project.lib.model.task import Task

class TaskCRUD(JSONRepository):
    def __init__(self):
        storage = JSONFileStorage(file_path=os.path.join(DB, 'tasks.json'))
        super().__init__(model=Task, storage=storage)
