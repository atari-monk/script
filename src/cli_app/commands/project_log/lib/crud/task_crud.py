import os
from .....libs.json_crud.crud import CRUD
from .....libs.json_crud.json_storage import JSONStorage
from ..model.task import Task
from ..config import DB_DIR

class TaskCRUD(CRUD):
    def __init__(self):
        # Initialize with Task model and JSONStorage instance for 'tasks.json'
        storage = JSONStorage(file_path=os.path.join(DB_DIR, 'tasks.json'))
        super().__init__(model=Task, storage=storage)