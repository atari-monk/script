import json
import os
from typing import Optional, Dict
from pydantic import BaseModel, ValidationError
from ..config import DB_DIR

# Define the Project Pydantic model for validation
class Project(BaseModel):
    name: str
    description: str

class ProjectCRUD:
    def __init__(self):
        self.file_path = os.path.join(DB_DIR, 'projects.json')
        # Ensure the file exists, if not create it with an empty list
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _read_data(self) -> list:
        """Reads the current data from the JSON file."""
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: list):
        """Writes the data back to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def create_project(self, name: str, description: str) -> Optional[dict]:
        """Creates a new project and adds it to the JSON file."""
        try:
            # Validate data
            project = Project(name=name, description=description)
            
            # Generate the project data as a dictionary (exclude 'id')
            project_data = project.dict()
            projects = self._read_data()
            
            # Assign a unique ID
            project_id = len(projects) + 1
            project_data['id'] = project_id
            
            # Add the new project to the data list
            projects.append(project_data)
            
            # Save the updated data back to the file
            self._write_data(projects)
            
            return project_data

        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_project(self, project_id: int) -> Optional[dict]:
        """Retrieves a project by its ID from the JSON file."""
        projects = self._read_data()
        for project in projects:
            if project['id'] == project_id:
                return project
        print(f"Project with ID {project_id} not found.")
        return None

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Updates a project in the JSON file."""
        projects = self._read_data()
        for project in projects:
            if project['id'] == project_id:
                if name:
                    project['name'] = name
                if description:
                    project['description'] = description
                
                # Write the updated list back to the file
                self._write_data(projects)
                print(f"Project {project_id} updated successfully.")
                return True
        print(f"Failed to update project with ID {project_id}.")
        return False

    def delete_project(self, project_id: int) -> bool:
        """Deletes a project by its ID from the JSON file."""
        projects = self._read_data()
        updated_projects = [project for project in projects if project['id'] != project_id]
        
        if len(updated_projects) == len(projects):
            print(f"Project with ID {project_id} not found.")
            return False
        
        # Write the updated list back to the file
        self._write_data(updated_projects)
        print(f"Project with ID {project_id} deleted.")
        return True
