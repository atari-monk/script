from rich.console import Console
from rich.table import Table
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.dialogue_crud import DialogueCRUD

class SearchDialogCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.console = Console()
        self.dialog_crud = DialogueCRUD()

    def execute(self, *args):
        # Validate arguments: search query (keyword)
        if len(args) < 1:
            self.console.print("[bold red]Error:[/bold red] Missing argument: search query.")
            return
        
        search_query = args[0].lower()  # Make the search case-insensitive

        # Fetch all dialogs
        dialogs = self.dialog_crud.list_all()

        # Filter dialogs that match the search query in the message or response
        matching_dialogs = [
            dialog for dialog in dialogs if search_query in dialog["message"].lower() or search_query in dialog["response"].lower()
        ]

        if not matching_dialogs:
            self.console.print(f"[bold red]Error:[/bold red] No dialogs found matching the search query '{search_query}'.")
            return

        # Print matching dialogs in the format: id - message
        self.console.print(f"[bold green]Dialogs matching '{search_query}':[/bold green]")

        # Create a table to display the matching dialogs
        table = Table(title="Search Results", show_header=True, header_style="bold magenta")
        table.add_column("Dialog ID", style="dim", width=10)
        table.add_column("Message", style="bold", width=60)

        # Add rows for each matching dialog
        for dialog in matching_dialogs:
            table.add_row(str(dialog['id']), dialog['message'])

        self.console.print(table)

        # Ask the user to select a dialog ID to view its details
        dialog_id_to_print = input("Enter dialog ID to view its message and response: ")
        dialog = next((d for d in matching_dialogs if str(d["id"]) == dialog_id_to_print), None)

        if dialog:
            # Print the selected dialog's message and response in a nice format
            self.console.print(f"\n[bold cyan]Dialog ID {dialog_id_to_print}:[/bold cyan]")
            self.console.print(f"[bold]Message:[/bold] {dialog['message']}")
            self.console.print(f"[bold]Response:[/bold] {self.remove_markdown_markers(dialog['response'])}")
        else:
            self.console.print(f"[bold red]Error:[/bold red] No dialog found with ID '{dialog_id_to_print}'.")

    def remove_markdown_markers(self, md_text):
        lines = md_text.splitlines()  # Split the content into lines

        clean_lines = []

        for line in lines:
            # Remove headers (e.g., # Header, ## Subheader)
            line = line.lstrip('#').strip()

            # Remove bullet points (e.g., - item or * item)
            if line.startswith('- ') or line.startswith('* '):
                line = line[2:].strip()

            # Remove emphasis (e.g., *italic* or **bold**)
            line = line.replace('*', '').replace('_', '')

            # Remove inline code (e.g., `code here`)
            line = line.replace('`', '')

            # Remove links (e.g., [text](url))
            if '[' in line and ']' in line and '(' in line and ')' in line:
                line = line.split('](')[0].strip('[]')  # Keep only the text inside the link

            # Remove images (e.g., ![alt text](url))
            if line.startswith('!['):
                line = ''

            # Add the cleaned line
            clean_lines.append(line)

        # Join the lines back together with newlines
        clean_text = '\n'.join(clean_lines)

        return clean_text

    @property
    def description(self):
        return "Searches for dialogues by a keyword in either the message or the response."
