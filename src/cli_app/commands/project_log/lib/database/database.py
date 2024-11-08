# database.py
from tinydb import TinyDB
import os
from ..config import DB_DIR

class Database:
    def __init__(self, db_dir: str):
        self.db_dir = db_dir
        self._db = None
        self._table = None
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

    def set_table(self, db_name: str):
        try:
            db_path = os.path.join(self.db_dir, f"{db_name}.json")
            self._db = TinyDB(db_path)
            self._table = self._db.table(db_name)
            print(f"Table '{db_name}' has been set with database at: {db_path}")
            print(f"Table is: {self._table}")  # Additional debug print here
        except Exception as e:
            print(f"Error setting table '{db_name}': {e}")
            raise ValueError("Failed to set the table.") from e

    def get_table(self):
        if self._table is None:
            print("No table has been set yet.")
            raise ValueError("No table has been set.")
        print(f"Current table: {self._table}")
        return self._table

# Initialize the db context
db_context = Database(DB_DIR)
