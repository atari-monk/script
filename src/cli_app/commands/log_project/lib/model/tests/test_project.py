import pytest
from datetime import date
from project import Project  # Replace with the correct import path

def test_valid_project():
    # Test valid project initialization
    project = Project(
        name="Project_Alpha",
        description="This is a test project with at least five words.",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status="In Progress",
        priority="High",
        technologies=["Python", "Django"],
        milestones=["Milestone 1", "Milestone 2"],
        current_tasks=["Task 1", "Task 2"],
        last_updated=date(2024, 11, 11)
    )

    assert project.name == "Project_Alpha"
    assert project.description == "This is a test project with at least five words."
    assert project.start_date == date(2024, 1, 1)
    assert project.end_date == date(2024, 12, 31)
    assert project.status == "In Progress"
    assert project.priority == "High"
    assert project.technologies == ["Python", "Django"]
    assert project.milestones == ["Milestone 1", "Milestone 2"]
    assert project.current_tasks == ["Task 1", "Task 2"]
    assert project.last_updated == date(2024, 11, 11)

def test_invalid_name():
    # Test invalid project name
    with pytest.raises(ValueError, match="Project name must contain only alphanumeric characters, spaces, hyphens, and underscores."):
        Project(
            name="Project!Alpha",
            description="Valid description.",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )

def test_invalid_description():
    # Test invalid project description (less than 5 words)
    with pytest.raises(ValueError, match="Description should contain at least 5 words."):
        Project(
            name="Valid Project",
            description="Short description.",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )

def test_end_date_before_start_date():
    # Test invalid project dates (end date before start date)
    with pytest.raises(ValueError, match="End date must be after the start date."):
        Project(
            name="Valid Project",
            description="Valid description.",
            start_date=date(2024, 12, 1),
            end_date=date(2024, 1, 1)
        )

def test_default_empty_lists():
    # Test that the lists default to empty when not provided
    project = Project(
        name="Project_Alpha",
        description="This is a valid description with at least five words.",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31)
    )
    
    assert project.technologies == []
    assert project.milestones == []
    assert project.current_tasks == []

def test_optional_fields():
    # Test that optional fields can be left empty
    project = Project(
        name="Project_Alpha",
        description="This is a valid description with at least five words.",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31)
    )
    
    assert project.repo_link is None
    assert project.status is None
    assert project.priority is None
    assert project.last_updated is None
