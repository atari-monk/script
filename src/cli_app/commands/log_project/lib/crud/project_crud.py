import os
from libs.crud.crud import CRUD
from libs.crud.json_storage import JSONStorage
from commands.log_project.lib.config import DB
from libs.model.project import Project

class ProjectCRUD(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'projects.json'))
        super().__init__(model=Project, storage=storage)
