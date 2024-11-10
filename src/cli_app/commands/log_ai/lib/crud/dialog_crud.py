import os
from commands.log_ai.lib.config import DB_DIR
from commands.log_ai.lib.model.dialog import Dialog
from libs.crud.crud import CRUD
from libs.crud.json_storage import JSONStorage

class DialogCRUD(CRUD):
    def __init__(self):
        # Initialize with Dialog model and JSONStorage instance for 'dialogs.json'
        storage = JSONStorage(file_path=os.path.join(DB_DIR, 'dialogs.json'))
        super().__init__(model=Dialog, storage=storage)
