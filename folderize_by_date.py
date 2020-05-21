
import argparse
import os
import subprocess
from contextlib import contextmanager
from datetime import datetime
from operator import methodcaller
from pathlib import Path
from shutil import move
from typing import List, Iterable

from rename_with_datetime import get_creation_date
from utils import create_dirs, git_mv

# modes
# flat tree (by month)
# 2018.11/ 2018.12/ 2019.01/
# deep tree
# 2018/2018.11/ 2018/2018.12/ 2019/2019.01

# algo
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
    parser.add_argument(
        '--git',
        action="store_true",
        help='Signal whether the files are inside a git repo.',
    )
    args = parser.parse_args()
    return args


def get_all_filepaths(folder_path: Path) -> List[Path]:
    """
    Return a list with every file under folder_path
    """
    # TODO: What if there are subdirectories? explore or ignore?
    # equiv: return [x for x in folder_path.iterdir() if x.is_file()]
    return list(filter(methodcaller("is_file"), folder_path.iterdir()))


def year_month(x: datetime):
    return f"{x.year}.{x.month:02}"


@contextmanager
def chcwd(newdir: Path):
    if not newdir.is_dir():
        raise ValueError(f"Folder {newdir!r} does not exist.")
    prevdir = Path.cwd()
    os.chdir(newdir.expanduser())
    try:
        yield
    finally:
        os.chdir(prevdir)


if __name__ == "__main__":
    args = parse_args()
    move_function = git_mv if args.git else move
    files = get_all_filepaths(args.folder)
    datetime_objs = list(map(get_creation_date, files))
    folders = set(map(year_month, datetime_objs))
    create_dirs(map(args.folder.joinpath, folders))
    with chcwd(args.folder):
        for file_path, creation_date in zip(files, datetime_objs):
            new_file_path = args.folder.joinpath(
                year_month(creation_date),
                file_path.name,
            )
            move_function(str(file_path), str(new_file_path))
