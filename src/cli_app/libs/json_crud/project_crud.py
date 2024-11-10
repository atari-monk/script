import os
from .crud import CRUD
from .json_storage import JSONStorage
from ..model.project import Project
from ...commands.log_project.lib.config import DB_DIR

class ProjectCRUD(CRUD):
    def __init__(self):
        # Initialize with Project model and JSONStorage instance for 'projects.json'
        storage = JSONStorage(file_path=os.path.join(DB_DIR, 'projects.json'))
        super().__init__(model=Project, storage=storage)
