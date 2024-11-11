import os
from libs.crud.crud import CRUD
from libs.crud.json_storage import JSONStorage
from commands.log_ai.lib.config import DB
from commands.log_ai.lib.model.dialogue import Dialogue

class DialogueCRUD(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'dialogs.json'))
        super().__init__(model=Dialogue, storage=storage)

    def get_dialogs_by_conversation_id(self, conversation_id: str):
        # Assuming you have a way to fetch dialogs by conversation_id
        # This could query a dialogs database or list where dialogs are stored
        dialogs = self.storage.get_all()
        return [dialog for dialog in dialogs if dialog['conversation_id'] == conversation_id]
    