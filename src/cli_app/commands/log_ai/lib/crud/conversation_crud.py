import os
from shared.crud.crud import CRUD
from cli_app.shared.json_storage import JSONStorage
from commands.log_ai.lib.config import DB
from commands.log_ai.lib.model.conversation import Conversation

class ConversationCRUD(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'conversations.json'))
        super().__init__(model=Conversation, storage=storage)
