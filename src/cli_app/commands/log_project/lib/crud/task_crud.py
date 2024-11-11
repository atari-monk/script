import os
from libs.crud.crud import CRUD
from libs.crud.json_storage import JSONStorage
from commands.log_project.lib.config import DB
from commands.log_project.lib.model.task import Task

class TaskCRUD(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'tasks.json'))
        super().__init__(model=Task, storage=storage)
