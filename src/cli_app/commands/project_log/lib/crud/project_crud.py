from typing import Optional, Dict
from tinydb import Query
from pydantic import ValidationError
from ..database.database import db_context  # Get the shared db context
from ..model.project import Project
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectCRUD:
    def __init__(self):
        #import pdb; pdb.set_trace()
        db_context.set_table("projects")
        print("Table set, now calling get_table...")
        self.table = db_context.get_table()

    def create_project(self, name: str, description: str) -> Optional[dict]:
        """Creates a new project with validation and adds it to the database."""
        try:
            # Validate data
            project = Project(name=name, description=description)
            
            # Insert into TinyDB and automatically assign an ID
            project_data = project.dict(exclude={"id"})  # Exclude the id to let TinyDB manage it
            project_id = self.table.insert(project_data)
            project_data['id'] = project_id  # Manually assign the id here after insertion
            
            logger.info(f"Project created with ID: {project_id}")
            return project_data
        
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return None

    def get_project(self, project_id: int) -> Optional[dict]:
        """Retrieves a project by ID."""
        return self._get_project_by_id(project_id)

    def _get_project_by_id(self, project_id: int) -> Optional[dict]:
        """Helper method to reduce repetitive code when querying by project ID."""
        project = self.table.get(Query().id == project_id)
        if project:
            return project
        else:
            logger.warning(f"Project with ID {project_id} not found.")
            return None

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Updates an existing project with new data."""
        updates = {}
        if name:
            updates["name"] = name
        if description:
            updates["description"] = description
        
        if updates:
            result = self.table.update(updates, Query().id == project_id)
            if result:
                logger.info(f"Project {project_id} updated successfully.")
                return True
            else:
                logger.warning(f"Failed to update project with ID {project_id}.")
        return False

    def delete_project(self, project_id: int) -> bool:
        """Deletes a project by ID."""
        result = self.table.remove(Query().id == project_id)
        if result:
            logger.info(f"Project with ID {project_id} deleted.")
            return True
        else:
            logger.warning(f"Project with ID {project_id} not found.")
            return False
