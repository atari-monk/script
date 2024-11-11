from rich.console import Console
from rich.table import Table
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.conversation_crud import ConversationCRUD

class SearchConversationsCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.console = Console()
        self.conversation_crud = ConversationCRUD()

    def execute(self, *args):
        # Check if the user has provided search keywords
        if len(args) < 1:
            self.console.print("[bold red]Error:[/bold red] Please provide a search keyword.")
            return

        search_term = args[0].lower()  # Get the search term from the command line argument

        # Fetch all conversations
        conversations = self.conversation_crud.list_all()

        # Filter conversations based on the search term in name or description
        filtered_conversations = [
            conversation for conversation in conversations
            if search_term in conversation['name'].lower() or search_term in conversation['description'].lower()
        ]

        if not filtered_conversations:
            self.console.print(f"[bold red]Error:[/bold red] No conversations found matching '{search_term}'.")
            return

        # Print the filtered conversations
        self.console.print(f"[bold green]Filtered Conversations matching '{search_term}':[/bold green]")

        # Create a table to display the filtered conversations
        table = Table(title="Filtered Conversations", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=10)
        table.add_column("Name", style="bold", width=30)
        table.add_column("Description", style="dim", width=50)

        # Add rows for each filtered conversation
        for conversation in filtered_conversations:
            table.add_row(str(conversation['id']), conversation['name'], conversation['description'])

        self.console.print(table)

    @property
    def description(self):
        return "Searches conversations by name or description based on a given keyword."
