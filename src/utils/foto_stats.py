import os
import shutil
from datetime import datetime
from collections import defaultdict
from typing import Optional, Any, Dict, Tuple, Union
import argparse
from PIL import Image
from PIL.ExifTags import TAGS

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.heic', '.tiff', '.bmp', '.jfif')


def get_exif_date(file_path: str) -> Optional[int]:
    """
    Return the year from EXIF DateTimeOriginal if available.
    """
    try:
        image: Image.Image = Image.open(file_path)
        exif_raw = image._getexif()  # type: ignore[attr-defined]

        if not isinstance(exif_raw, dict):
            return None

        # Keep only int keys to satisfy type checker
        exif_data: Dict[int, Any] = {k: v for k, v in exif_raw.items() if isinstance(k, int)}

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


def scan_photos(source_dir: str) -> Tuple[defaultdict[Union[int, str], int], int]:
    """
    Scan folder and count photos per year without moving files.
    Returns a tuple (year_stats, total_files)
    """
    year_stats: defaultdict[Union[int, str], int] = defaultdict(int)
    total_files: int = 0

    for root, _, files in os.walk(source_dir):
        if root != source_dir:
            continue

        for filename in files:
            if not filename.lower().endswith(IMAGE_EXTENSIONS):
                continue

            file_path: str = os.path.join(root, filename)
            total_files += 1

            year: Union[int, str] = get_creation_year(file_path)
            year_stats[year] += 1

    return year_stats, total_files


def print_stats(year_stats: defaultdict[Union[int, str], int], total_files: int) -> None:
    """
    Print statistics nicely.
    """
    print("\n=== Photo Year Statistics ===\n")
    print(f"Total image files scanned: {total_files}\n")

    for year in sorted(year_stats, key=lambda x: (x == "Unknown", x)):
        print(f"{year}: {year_stats[year]} files")


def move_photos(source_dir: str) -> None:
    """
    Move photos into year folders. Handles duplicates and unknown years.
    """
    for root, _, files in os.walk(source_dir):
        if root != source_dir:
            continue

        for filename in files:
            if not filename.lower().endswith(IMAGE_EXTENSIONS):
                continue

            file_path: str = os.path.join(root, filename)
            year: Union[int, str] = get_creation_year(file_path)
            year_folder: str = os.path.join(source_dir, str(year))
            os.makedirs(year_folder, exist_ok=True)

            destination: str = os.path.join(year_folder, filename)

            # Handle duplicates by appending a counter
            counter: int = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(destination):
                destination = os.path.join(year_folder, f"{base}_{counter}{ext}")
                counter += 1

            shutil.move(file_path, destination)
            print(f"Moved: {filename} → {year}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan and optionally organize photos by year based on EXIF/creation date."
    )
    parser.add_argument(
        "source_dir", type=str, help="Source folder containing photos"
    )
    parser.add_argument(
        "-m", "--move", action="store_true", help="Move photos into year folders"
    )

    args = parser.parse_args()
    source_dir: str = args.source_dir

    year_stats, total_files = scan_photos(source_dir)
    print_stats(year_stats, total_files)

    if args.move:
        print("\nMoving files into year folders...\n")
        move_photos(source_dir)
        print("\nAll files moved successfully.")


if __name__ == "__main__":
    main()
