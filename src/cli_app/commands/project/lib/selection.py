import random

# Project list
projects = ["game_engine", "json_editor", "character_editor", "unreal_project", "documentation"]

# Decision methods dictionary to store different strategies
decision_methods = {}

# Decorator to register decision methods
def register_method(func):
    decision_methods[func.__name__] = func
    return func

# Logical method: selects based on project priorities
@register_method
def priority_based():
    # Example priority order (customize as needed)
    priorities = {
        "game_engine": 1,        # Highest priority
        "json_editor": 2,
        "character_editor": 3,
        "unreal_project": 4,
        "documentation": 5       # Lowest priority
    }
    return min(projects, key=lambda p: priorities.get(p, float('inf')))

# Random method: picks a project randomly
@register_method
def random_choice():
    return random.choice(projects)

# Example method based on length of time since last worked (hypothetical times)
@register_method
def longest_idle():
    last_worked = {
        "game_engine": 7,         # days since last worked
        "json_editor": 3,
        "character_editor": 14,
        "unreal_project": 1,
        "documentation": 5
    }
    return max(projects, key=lambda p: last_worked.get(p, 0))

# Decision maker function
def decide_project(method_name="random_choice"):
    if method_name not in decision_methods:
        raise ValueError(f"Method '{method_name}' not found. Available methods: {list(decision_methods.keys())}")
    return decision_methods[method_name]()

def main() :
    # Choose a method (you can replace 'random_choice' with other method names like 'priority_based')
    chosen_method = "priority_based"  # Change to test different methods
    project = decide_project(chosen_method)
    print(f"Selected project to work on: {project} (using '{chosen_method}' method)")
