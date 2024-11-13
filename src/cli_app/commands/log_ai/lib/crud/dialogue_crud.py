import os
from shared.crud.crud import CRUD
from cli_app.shared.json_file_storage import JSONFileStorage
from commands.log_ai.lib.config import DB
from commands.log_ai.lib.model.dialogue import Dialogue

class DialogueCRUD(CRUD):
    def __init__(self):
        storage = JSONFileStorage(file_path=os.path.join(DB, 'dialogs.json'))
        super().__init__(model=Dialogue, storage=storage)

    def get_dialogs_by_conversation_id(self, conversation_id: str):
        # Assuming you have a way to fetch dialogs by conversation_id
        # This could query a dialogs database or list where dialogs are stored
        dialogs = self.list_all()
        return [dialog for dialog in dialogs if dialog['conversation_id'] == conversation_id]
    