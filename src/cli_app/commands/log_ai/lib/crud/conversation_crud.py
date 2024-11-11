import os
from libs.crud.crud import CRUD
from libs.crud.json_storage import JSONStorage
from commands.log_ai.lib.config import DB
from commands.log_ai.lib.model.conversation import Conversation

class ConversationCRUD(CRUD):
    def __init__(self):
        storage = JSONStorage(file_path=os.path.join(DB, 'conversations.json'))
        super().__init__(model=Conversation, storage=storage)
