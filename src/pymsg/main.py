import json
import pyperclip
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SimpleDiagnostic:
    message: str
    line: int
    column: int

def extract_diagnostics(data: List[Dict[str, Any]]) -> List[SimpleDiagnostic]:
    return [
        SimpleDiagnostic(
            message=str(item.get('message', '')),
            line=int(item.get('startLineNumber', 0)),
            column=int(item.get('startColumn', 0))
        )
        for item in data
    ]

def format_output(data: List[SimpleDiagnostic]) -> str:
    return "\n".join(f"Line {d.line}:{d.column} - {d.message}" for d in data)

def main() -> None:
    try:
        clipboard_content = pyperclip.paste()
        data: List[Dict[str, Any]] = json.loads(clipboard_content)
        diagnostics = extract_diagnostics(data)
        
        print("Extracted messages:")
        for d in diagnostics:
            print(f"Line {d.line}:{d.column} - {d.message}")
        
        pyperclip.copy(format_output(diagnostics))
        print(f"\nCopied {len(diagnostics)} messages to clipboard!")
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON data in clipboard")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
