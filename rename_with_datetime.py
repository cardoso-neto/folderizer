
import os
import platform
import sys
from datetime import datetime


# import pathlib
# print(pathlib.Path('yourPathGoesHere').suffix)
# If you need all the suffixes (eg if you have a .tar.gz), .suffixes will return a list of them!

def get_creation_timestamp(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def get_creation_date(filepath: str):
    t = get_creation_timestamp(filepath)
    return datetime.fromtimestamp(t)


def format_datettime(d: datetime) -> str:
	return f'{d.year}.{d.month:02}.{d.day:02} {d.hour:02}{d.minute:02}'


def rename_file(directory_path: str, filename: str):
    path_to_file = directory_path + filename
    _, file_extension = os.path.splitext(filename)
    new_file_name = format_datettime(get_creation_date(path_to_file))
    path_to_output = directory_path + new_file_name + file_extension
    os.rename(path_to_file, path_to_output)


if __name__ == "__main__":
    error_message = 'Usage: python datetime_filename.py folderpath'
    assert sys.argv[1] is not None, error_message
    directory_path = sys.argv[1]

    for old_file_name in os.listdir(directory_path):
        rename_file(directory_path, old_file_name)
