from rich.console import Console
from rich.table import Table
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.conversation_crud import ConversationCRUD

class PrintConversationsCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.console = Console()
        self.conversation_crud = ConversationCRUD()

    def execute(self, *args):
        # Fetch all conversations
        conversations = self.conversation_crud.list_all()

        if not conversations:
            self.console.print("[bold red]Error:[/bold red] No conversations found.")
            return

        # Print all conversations in the format: id - name - description
        self.console.print("[bold green]Conversations in the database:[/bold green]")

        # Create a table to display the conversations
        table = Table(title="Conversations", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=10)
        table.add_column("Name", style="bold", width=30)
        table.add_column("Description", style="dim", width=50)

        # Add rows for each conversation
        for conversation in conversations:
            table.add_row(str(conversation['id']), conversation['name'], conversation['description'])

        self.console.print(table)

    @property
    def description(self):
        return "Prints all conversations with their ID, name, and description."
