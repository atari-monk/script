import os
from .....libs.json_crud.crud import CRUD
from .....libs.json_crud.json_storage import JSONStorage
from .....libs.model.project import Project
from ..config import DB_DIR

class ProjectCRUD(CRUD):
    def __init__(self):
        # Initialize with Project model and JSONStorage instance for 'projects.json'
        storage = JSONStorage(file_path=os.path.join(DB_DIR, 'projects.json'))
        super().__init__(model=Project, storage=storage)
