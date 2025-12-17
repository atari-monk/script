import os
from collections import defaultdict
from typing import Optional, Any, Dict, Union
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import argparse

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.heic', '.tiff', '.bmp', '.jfif')

def get_exif_date(file_path: str) -> Optional[int]:
    """
    Return the year from EXIF DateTimeOriginal if available.
    """
    try:
        image: Image.Image = Image.open(file_path)
        exif_raw: Optional[Dict[Any, Any]] = image._getexif()  # type: ignore[attr-defined]

        if not isinstance(exif_raw, dict):
            return None

        # Pylance-friendly: explicitly type keys/values
        exif_data: Dict[int, Any] = {int(k): v for k, v in exif_raw.items() if isinstance(k, int)}

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id)
            if tag == "DateTimeOriginal" and isinstance(value, str):
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").year

        return None
    except Exception:
        return None

def get_creation_year(file_path: str) -> Union[int, str]:
    """
    Try EXIF first, then fallback to file creation date.
    Returns year as int or "Unknown" if not available.
    """
    year: Optional[int] = get_exif_date(file_path)
    if year is not None:
        return year
    try:
        ctime: float = os.path.getctime(file_path)
        return datetime.fromtimestamp(ctime).year
    except Exception:
        return "Unknown"

def check_photos_in_year_folders(source_dir: str) -> None:
    """
    Scan year folders and check if photos are in correct folders.
    Prints statistics and misplacements.
    """
    year_stats: defaultdict[Union[int, str], int] = defaultdict(int)
    misplaced_files: list[str] = []
    total_files: int = 0

    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(IMAGE_EXTENSIONS):
                continue

            file_path = os.path.join(folder_path, filename)
            total_files += 1

            correct_year: Union[int, str] = get_creation_year(file_path)
            year_stats[correct_year] += 1

            # Check if current folder matches the correct year
            try:
                folder_year = int(folder_name)
            except ValueError:
                folder_year = folder_name  # could be "Unknown" folder

            if folder_year != correct_year:
                misplaced_files.append(f"{filename} → Folder: {folder_name}, Should be: {correct_year}")

    # Print statistics
    print("\n=== Photo Year Statistics ===\n")
    print(f"Total image files scanned: {total_files}\n")
    for year in sorted(year_stats, key=lambda x: (x == "Unknown", x)):
        print(f"{year}: {year_stats[year]} files")

    if misplaced_files:
        print("\n=== Misplaced Files ===\n")
        for item in misplaced_files:
            print(item)
    else:
        print("\nAll files are in correct year folders.")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check photos in year folders and print stats/misplacements."
    )
    parser.add_argument(
        "source_dir", type=str, help="Source folder containing year subfolders"
    )

    args = parser.parse_args()
    check_photos_in_year_folders(args.source_dir)

if __name__ == "__main__":
    main()
