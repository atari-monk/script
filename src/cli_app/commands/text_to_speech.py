from base.base_command import BaseCommand
import subprocess
import os

class TextToSpeechCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        self.run_powershell_script('commands/text_to_speech.ps1')

    @property
    def description(self):
        return "Text To Speech."
    
    def run_powershell_script(self, script_path):
        # Ensure the script path is absolute
        script_path = os.path.abspath(script_path)
        
        # Build the command
        command = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
        
        try:
            # Run the PowerShell script
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Print the output
            if result.returncode == 0:
                if len(result.stdout) > 0:
                    print("Script output:")
                    print(result.stdout)
            else:
                print("Error occurred:")
                print(result.stderr)
        except Exception as e:
            print(f"An error occurred while running the script: {e}")
