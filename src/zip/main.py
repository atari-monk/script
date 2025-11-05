#!/usr/bin/env python3
"""
Simple Project Zipping Utility
"""

import argparse
import json
import zipfile
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Color codes for output
COLORS: Dict[str, str] = {
    'RED': '\033[91m',
    'GREEN': '\033[92m', 
    'YELLOW': '\033[93m',
    'CYAN': '\033[96m',
    'RESET': '\033[0m'
}

def get_default_config_path() -> Path:
    """Get the default config path relative to the script location"""
    script_dir = Path(__file__).parent
    return script_dir / "config.json"

def color_print(message: str, color: str = "") -> None:
    """Print colored output"""
    if color and sys.stdout.isatty():
        print(f"{color}{message}{COLORS['RESET']}")
    else:
        print(message)

def load_config(project_name: str, config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load project configuration from JSON"""
    if config_path is None:
        config_path = str(get_default_config_path())
    
    config_file = Path(config_path)
    
    try:
        with open(config_file, 'r') as f:
            config: Dict[str, Any] = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Config file not found: {config_file}")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON in config file: {config_file}")
    
    if project_name not in config:
        available: str = ", ".join(config.keys())
        raise Exception(f"Project '{project_name}' not found. Available: {available}")
    
    return config[project_name]

def list_projects(config_path: Optional[str] = None) -> None:
    """List all available projects"""
    if config_path is None:
        config_path = str(get_default_config_path())
    
    config_file = Path(config_path)
    
    try:
        with open(config_file, 'r') as f:
            config: Dict[str, Any] = json.load(f)
        
        color_print("Available projects:", COLORS['CYAN'])
        for project in config.keys():
            print(f"  {project}")
    except FileNotFoundError:
        color_print(f"Config file not found: {config_file}", COLORS['RED'])

def should_include_file(file_path: Path, exclude_folders: List[str], exclude_files: List[str]) -> bool:
    """Check if file should be included (not excluded)"""
    file_path_str: str = str(file_path)
    file_name: str = file_path.name
    
    # Check folder exclusion
    for folder in exclude_folders:
        if folder in file_path_str:
            return False
    
    # Check file exclusion
    for pattern in exclude_files:
        if pattern.startswith('*') and pattern.endswith('*'):
            # *text* pattern
            pattern_content: str = pattern[1:-1]
            if pattern_content in file_name:
                return False
        elif pattern.startswith('*'):
            # *.ext pattern  
            if file_name.endswith(pattern[1:]):
                return False
        elif pattern.endswith('*'):
            # prefix* pattern
            if file_name.startswith(pattern[:-1]):
                return False
        else:
            # exact match
            if file_name == pattern:
                return False
    
    return True

def create_project_zip(project_name: str, config_path: Optional[str] = None) -> None:
    """Main function to create zip for a project"""
    color_print(f"Loading configuration for: {project_name}", COLORS['YELLOW'])
    
    # Load config
    config: Dict[str, Any] = load_config(project_name, config_path)
    
    root_path: Path = Path(config['rootPath'])
    output_zip: Path = Path(config['outputZip'])
    exclude_folders: List[str] = config.get('excludeFolders', [])
    exclude_files: List[str] = config.get('excludeFiles', [])
    
    color_print(f"Root path: {root_path}", COLORS['CYAN'])
    color_print(f"Output zip: {output_zip}", COLORS['CYAN'])
    
    if not root_path.exists():
        raise Exception(f"Root path does not exist: {root_path}")
    
    # Find all files to include
    color_print("Scanning files...", COLORS['YELLOW'])
    files_to_zip: List[Path] = []
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            if should_include_file(file_path, exclude_folders, exclude_files):
                files_to_zip.append(file_path)
    
    if not files_to_zip:
        color_print("No files found to include!", COLORS['RED'])
        return
    
    color_print(f"Found {len(files_to_zip)} files to include", COLORS['GREEN'])
    
    # Create zip
    color_print("Creating zip file...", COLORS['YELLOW'])
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            arcname: Path = file_path.relative_to(root_path)
            zipf.write(file_path, arcname)
    
    color_print(f"Zip created successfully: {output_zip}", COLORS['GREEN'])
    
    # Show sample files
    color_print("Sample of included files:", COLORS['CYAN'])
    for file_path in files_to_zip[:10]:
        size_kb: float = file_path.stat().st_size / 1024
        rel_path: Path = file_path.relative_to(root_path)
        print(f"  {rel_path} - {size_kb:.1f} KB")
    
    if len(files_to_zip) > 10:
        print(f"  ... and {len(files_to_zip) - 10} more files")

def main() -> None:
    parser = argparse.ArgumentParser(description='Create zip archives for projects')
    parser.add_argument('project', nargs='?', help='Project name to zip')
    parser.add_argument('--config', '-c', help='Config file path (default: auto-detect)')
    parser.add_argument('--list', '-l', action='store_true', help='List available projects')
    
    args: argparse.Namespace = parser.parse_args()
    
    try:
        if args.list:
            list_projects(args.config)
        elif args.project:
            create_project_zip(args.project, args.config)
        else:
            parser.print_help()
            print("\nExamples:")
            print("  zip cv")
            print("  zip cv --config /path/to/config.json") 
            print("  zip --list")
            
    except Exception as e:
        color_print(f"Error: {e}", COLORS['RED'])
        sys.exit(1)

if __name__ == "__main__":
    main()