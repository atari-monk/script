import json
import os
from jsonschema import validate, ValidationError
from typing import Any, Dict

SCHEMA_FILE: str = "C:/Atari-Monk/projects/script/src/log/project_log_schema.json"
LOG_FOLDER: str = "C:/Atari-Monk/projects/checkpoint/docs/logs"

def load_schema(schema_path: str) -> Dict[str, Any]:
    """Load JSON schema from a file."""
    with open(schema_path, "r") as f:
        return json.load(f)

def validate_log(file_path: str, schema: Dict[str, Any]) -> int:
    """
    Validate a single JSON log file against the schema,
    print a per-day task log, and return total duration in minutes.
    """
    total_duration = 0
    with open(file_path, "r") as f:
        data = json.load(f)

    # Validate file
    try:
        validate(instance=data, schema=schema)
        print(f"✅ VALID: {file_path}")
    except ValidationError as e:
        print(f"❌ INVALID: {file_path}")
        print(f"  Path: {'/'.join(map(str, e.path))}")
        print(f"  Message: {e.message}")
        return 0  # Skip summing if invalid

    # Print per-day task log and sum durations
    for day_entry in data:
        day_total = 0
        date = day_entry.get('Date', 'Unknown')
        tag = day_entry.get('Tag', '')
        print(f"\n📅 Date: {date} | Tag: {tag}")

        for idx, interval in enumerate(day_entry.get("Interval", []), start=1):
            duration = interval.get("Duration", 0)
            try:
                duration_int = int(duration)
                day_total += duration_int
                total_duration += duration_int
            except (ValueError, TypeError):
                print(f"⚠️ Skipping invalid duration: {duration}")
                duration_int = 0

            goals = interval.get("Goals", [])
            notes = interval.get("Notes", [])

            print(f"  Interval {idx}: {duration_int} min")
            for g in goals:
                print(f"    ✅ Todo: {g}")
            for n in notes:
                print(f"    📝 Note: {n}")

        print(f"  ➤ Total for day: {day_total} minutes")

    return total_duration

def main() -> None:
    """Main entry point to validate all JSON logs and calculate totals."""
    schema = load_schema(SCHEMA_FILE)
    grand_total = 0

    for root, _, files in os.walk(LOG_FOLDER):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                monthly_total = validate_log(file_path, schema)
                print(f"\n📊 Total duration in {file}: {monthly_total} minutes\n")
                grand_total += monthly_total

    print(f"📌 GRAND TOTAL DURATION: {grand_total} minutes")

if __name__ == "__main__":
    main()
