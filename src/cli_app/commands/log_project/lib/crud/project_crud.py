import os
from shared.crud import CRUD
from shared.json_storage import JSONStorage
from commands.log_project.lib.config import DB
from commands.log_project.lib.model.project import Project
from commands.log_project.lib.model.project2 import Project2

class ProjectCRUD(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'projects.json'))
        super().__init__(model=Project, storage=storage)

class ProjectCRUD2(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'projects2.json'))
        super().__init__(model=Project2, storage=storage)
