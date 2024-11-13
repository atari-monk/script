import os
from shared.json_repository import JSONRepository
from shared.json_file_storage import JSONFileStorage
from commands.log_project.lib.config import DB
from commands.log_project.lib.model.project import Project
from commands.log_project.lib.model.project2 import Project2

class ProjectCRUD(JSONRepository):
    def __init__(self):
        storage = JSONFileStorage(file_path=os.path.join(DB, 'projects.json'))
        super().__init__(model=Project, storage=storage)

class ProjectCRUD2(JSONRepository):
    def __init__(self):
        storage = JSONFileStorage(file_path=os.path.join(DB, 'projects2.json'))
        super().__init__(model=Project2, storage=storage)
