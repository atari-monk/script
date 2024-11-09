import os
import json

def read_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def generate_file_structure(folder_path, exclude_files, excluded_folders, excluded_files, print_file_content=False, indent=""):
    folder_suffix = "/\n"
    indent_space = "    "
    file_structure = ""
    
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.name in excluded_folders or entry.name in excluded_files:
                continue
            if entry.is_dir():
                file_structure += f"{indent}{entry.name}{folder_suffix}"
                file_structure += generate_file_structure(
                    os.path.join(folder_path, entry.name),
                    exclude_files,
                    excluded_folders,
                    excluded_files,
                    print_file_content,
                    indent + indent_space
                )
            elif not exclude_files:
                file_structure += f"{indent}{entry.name}\n"
                if print_file_content:
                    file_content = read_file_content(os.path.join(folder_path, entry.name))
                    file_structure += f"{indent_space}{file_content}\n"
    return file_structure

def main():
    config_file_path = '../../config/print_code.json'
    folder_path_key = 'folder_path'
    output_file_key = 'output_file'
    exclude_files_key = 'exclude_files'
    excluded_folders_key = 'excluded_folders'
    excluded_files_key = 'excluded_files'
    print_file_content_key = 'print_file_content'
    is_active_key = 'isActive'

    folder_error_message = "Please make sure 'folder_path' and 'output_file' are set in the config file."
    output_written_message = "File structure for {} has been written to {}"
    
    config_data = read_config(config_file_path)
    default_output = config_data.get('default_output', './')
    printouts = config_data.get('printouts', {})

    for section, configs in printouts.items():
        for config_name, config in configs.items():
            if not config.get(is_active_key, True):  # Default to True if not specified
                continue

            folder_path = config.get(folder_path_key)
            output_file = config.get(output_file_key)
            exclude_files = config.get(exclude_files_key, False)
            excluded_folders = config.get(excluded_folders_key, [])
            excluded_files = config.get(excluded_files_key, [])
            print_file_content = config.get(print_file_content_key, False)

            # Set default output file path if not provided
            if not output_file:
                output_file = os.path.join(default_output, f"{config_name}.txt")

            if not folder_path or not output_file:
                print(folder_error_message)
                continue

            # Generate the file structure and write to the output file
            file_structure = generate_file_structure(
                folder_path, exclude_files, excluded_folders, excluded_files, print_file_content
            )

            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(file_structure)

            print(output_written_message.format(folder_path, output_file))
