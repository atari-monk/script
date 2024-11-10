import os
from commands.log_ai.lib.config import DB_DIR
from commands.log_ai.lib.model.conversation import Conversation
from libs.crud.crud import CRUD
from libs.crud.json_storage import JSONStorage

class ConversationCRUD(CRUD):
    def __init__(self):
        # Initialize with Conversation model and JSONStorage instance for 'conversations.json'
        storage = JSONStorage(file_path=os.path.join(DB_DIR, 'conversations.json'))
        super().__init__(model=Conversation, storage=storage)
