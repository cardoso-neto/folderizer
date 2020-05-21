
import argparse
from collections import Counter
from pathlib import Path
from shutil import move, rmtree
from typing import Iterable

from more_itertools import consume

from utils import git_mv


# get all files in a list
# move them to root folder
# delete all the empty folders

def parse_args():
    parser = argparse.ArgumentParser(
        description='Flatten folder structure; moving files to root folder.'
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
    parser.add_argument(
        '--fast',
        action="store_true",
        help='Signal whether to run safety checks.',
    )
    args = parser.parse_args()
    return args


def just_move(folder: Path, paths: Iterable[Path]):
    for file in paths:
        if file.is_file():
            move_function(str(file), str(folder / file.name))


def check_and_move(folder: Path, paths: Iterable[Path]):
    files = list(paths)
    filenames = set(file.name for file in files)
    if len(files) != len(filenames):
        counts = Counter(file.name for file in files)
        repeated = {
            item: count for item, count in counts.items() if count > 1
        }
        print(repeated)
        raise("Non-unique filenames found. Aborting.")
    just_move(folder, files)


def delete_folders(paths: Iterable[Path]):
    for dir_path in root_level_files:
        if dir_path.is_dir():
            try:
                rmtree(dir_path)
            except OSError as e:
                print(f"Error: {dir_path} : {e.strerror}")


if __name__ == "__main__":
    args = parse_args()
    move_function = git_mv if args.git else move
    paths = args.folder.rglob("*")
    root_level_files = args.folder.glob("*")
    if args.fast:
        just_move(args.folder, paths)
    else:
        check_and_move(args.folder, paths)
    delete_folders(root_level_files)
