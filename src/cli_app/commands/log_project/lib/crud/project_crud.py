import os
from commands.log_project.lib.config import DB
from commands.log_project.lib.model.project import Project
from commands.log_project.lib.model.project2 import Project2
from shared.json_file_storage import JSONFileStorage
from shared.jsonl_file_storage import JSONLFileStorage
from shared.json_repository import JSONRepository

class ProjectCRUD(JSONRepository):
    def __init__(self):
        storage = JSONFileStorage(file_path=os.path.join(DB, 'projects.json'))
        super().__init__(model=Project, storage=storage)

class ProjectCRUD2(JSONRepository):
    def __init__(self):
        storage = JSONFileStorage(file_path=os.path.join(DB, 'projects2.json'))
        super().__init__(model=Project2, storage=storage)

class ProjectCRUD3(JSONRepository):
    def __init__(self):
        storage = JSONLFileStorage(file_path=os.path.join(DB, 'projects2.jsonl'))
        super().__init__(model=Project2, storage=storage)