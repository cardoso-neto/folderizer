
import argparse
from pathlib import Path
from shutil import move

from superjson import json

from utils import create_dirs

def parse_args():
    parser = argparse.ArgumentParser(
        description='Snapshot the folder structure or restore from one.'
    )
    parser.add_argument(
        '--folder',
        type=Path,
        help='Folder where the files are located',
    )
    parser.add_argument(
        '--json_path',
        type=Path,
        help='JSON file path to read or save the snapshot.',
    )
    parser.add_argument(
        '--git',
        action="store_true",
        help='Signal whether the files are inside a git repo.',
    )
    parser.add_argument(
        '--restore',
        action="store_true",
        help='Signal whether to restore from a snapshot or create one.',
    )
    parser.add_argument(
        '-f',
        dest="overwrite_json",
        action="store_true",
        help='Signal whether to overwrite JSON.',
    )
    args = parser.parse_args()
    if args.json_path is None:
        args.json_path = args.folder.parent / "snapshot.json"
    return args


def save_snapshot(folder: Path, json_path: Path, overwrite=False):
    folders = {folder.name: folder for folder in args.folder.rglob("**")}
    files = {file.name: file for file in args.folder.rglob("*") if file.is_file()}
    snapshot = {"folders": folders, "files": files}
    json.dump(snapshot, str(json_path), indent=2, sort_keys=True, overwrite=overwrite)


def restore_snapshot(folder: Path, json_path: Path):
    snapshot = json.load(str(json_path))
    current_files = {file.name: file for file in folder.rglob("*")}
    missing_files = {
        filename for filename, filepath in snapshot["files"].items()
        if filename not in current_files
    }
    if missing_files:
        print("The following files are missing:")
        print(*missing_files, sep="\n")
    # TODO: only create deepest dirs to avoind unnecessary IO
    create_dirs(snapshot["folders"].values())
    for filename, snap_filepath in snapshot["files"].items():
        if filename in missing_files:
            continue
        move(current_files[filename], snap_filepath)


if __name__ == "__main__":
    args = parse_args()
    if args.restore:
        save_snapshot(args.folder, args.json_path.parent / "temp.json", overwrite=True)
        restore_snapshot(args.folder, args.json_path)
    else:
        save_snapshot(args.folder, args.json_path, overwrite=args.overwrite_json)
