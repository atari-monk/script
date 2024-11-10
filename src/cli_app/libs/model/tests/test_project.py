import pytest
from pydantic import ValidationError
from datetime import date
from ..project import Project  # Replace with the actual import

def test_valid_project():
    project = Project(
        name="My Project",
        description="This is a valid project description with more than five words.",
        repo_link="https://github.com/example",
        status="In Progress",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        priority="Medium",
        technologies=["Python", "Pydantic"],
        milestones=["Milestone 1", "Milestone 2"],
        current_tasks=["Task 1", "Task 2"],
        last_updated=date(2024, 10, 1)
    )
    assert project.name == "My Project"
    assert project.description == "This is a valid project description with more than five words."
    assert str(project.repo_link) == "https://github.com/example"
    assert project.status == "In Progress"
    assert project.start_date == date(2024, 1, 1)
    assert project.end_date == date(2024, 12, 31)
    assert project.priority == "Medium"
    assert project.technologies == ["Python", "Pydantic"]
    assert project.milestones == ["Milestone 1", "Milestone 2"]
    assert project.current_tasks == ["Task 1", "Task 2"]
    assert project.last_updated == date(2024, 10, 1)

def test_invalid_project_name():
    with pytest.raises(ValidationError):
        Project(
            name="Invalid@Name",  # Invalid name (contains non-allowed characters)
            description="Valid description.",
        )

def test_description_too_short():
    with pytest.raises(ValidationError):
        Project(
            name="Valid Project",
            description="Short.",
        )

def test_end_date_before_start_date():
    with pytest.raises(ValidationError):
        Project(
            name="Valid Project",
            description="Valid description.",
            start_date=date(2024, 1, 1),
            end_date=date(2023, 12, 31),
        )

def test_optional_fields():
    project = Project(
        name="Project with optional fields",
        description="Valid description with optional fields.",
    )
    assert project.repo_link is None
    assert project.status is None
    assert project.start_date is None
    assert project.end_date is None
    assert project.priority is None
    assert project.technologies == []
    assert project.milestones == []
    assert project.current_tasks == []
    assert project.last_updated is None
