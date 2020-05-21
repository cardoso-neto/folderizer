
import json
import subprocess
from pathlib import Path
from typing import Iterable


def create_dirs(directories: Iterable[Path]):
    for directory_path in directories:
        directory_path.mkdir(parents=True, exist_ok=True)


def git_mv(src: Path, dst: Path):
    subprocess.run(
        ["git", "mv", str(src), str(dst)]
    )


def save_json(obj, filepath: Path, **kwargs):
    with open(filepath, "w") as file_handler:
        json.dump(obj, file_handler, **kwargs)


def load_json(filepath: Path):
    with open(filepath) as file_handler:
        obj = json.load(file_handler)
    return obj
