
import argparse
from datetime import datetime
from operator import methodcaller
from pathlib import Path
from shutil import move
from typing import Iterable

from rename_with_datetime import get_creation_date


# modes
# flat tree (by month)
# 2018.11/ 2018.12/ 2019.01/
# deep tree
# 2018/2018.11/ 2018/2018.12/ 2019/2019.01

# determine which datetime element to use
# get all unique folders to create
# create them
# move files appropriately


def parse_args():
    parser = argparse.ArgumentParser(
        description='Group files by their month of creation.'
    )
    parser.add_argument(
        '--folder',
        type=Path,
        help='Folder where the files are located',
    )
    args = parser.parse_args()
    return args


def get_all_filepaths(folder_path: Path):
    """
    Return a list with everything under folder/
    """
    # What if there are subdirectories
    # should we explore them or ignore them? 
    return list(filter(methodcaller("is_file"), folder_path.iterdir()))


def create_dirs(directories: Iterable[Path]):
    for directory_path in directories:
        directory_path.mkdir(parents=True, exist_ok=True)


def year_month(x: datetime):
    return f"{x.year}.{x.month:02}"


if __name__ == "__main__":
    args = parse_args()
    files = get_all_filepaths(args.folder)
    datetime_objs = list(map(get_creation_date, files))
    folders = set(map(year_month, datetime_objs))
    create_dirs(map(args.folder.joinpath, folders))
    for file_path, creation_date in zip(files, datetime_objs):
        new_file_path = args.folder.joinpath(
            year_month(creation_date),
            file_path.name,
        )
        move(str(file_path), str(new_file_path))
