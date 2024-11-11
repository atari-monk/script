from rich.console import Console
from rich.table import Table
from base.base_command import BaseCommand
from commands.log_ai.lib.crud.dialogue_crud import DialogueCRUD

class PrintDialogueCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.console = Console()
        self.dialog_crud = DialogueCRUD()

    def execute(self, *args):
        # Validate arguments: conversation_id
        if len(args) < 1:
            self.console.print("[bold red]Error:[/bold red] Missing argument: conversation_id.")
            return
        
        conversation_id = args[0]

        # Fetch the dialogs for the given conversation ID using the new CRUD class
        dialogs = self.dialog_crud.list_all()  # Fetch all dialogs, or you could filter by conversation_id if needed
        conversation_dialogs = [dialog for dialog in dialogs if dialog["conversation_id"] == conversation_id]

        if not conversation_dialogs:
            self.console.print(f"[bold red]Error:[/bold red] No dialogs found for conversation ID '{conversation_id}'.")
            return

        # Print all dialogs in the format: id - message
        self.console.print("[bold green]Dialogs in the conversation:[/bold green]")

        # Create a table to display the dialogs
        table = Table(title="Conversation Dialogs", show_header=True, header_style="bold magenta")
        table.add_column("Dialog ID", style="dim", width=10)
        table.add_column("Message", style="bold", width=60)

        # Add rows for each dialog in the conversation
        for dialog in conversation_dialogs:
            table.add_row(str(dialog['id']), dialog['message'])

        self.console.print(table)

        # Ask the user to select a dialog ID to view the details
        dialog_id_to_print = input("Enter dialog ID to view its message and response: ")
        dialog = next((d for d in conversation_dialogs if str(d["id"]) == dialog_id_to_print), None)

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
        return "Prints all dialogs in a conversation and allows selection of a dialog ID to view its details."
