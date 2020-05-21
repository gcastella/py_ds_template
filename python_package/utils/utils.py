import git
import os
import importlib
from datetime import date
from datetime import datetime


def get_git_hash() -> str:
    """
    Get hexsha for the current git commit.
    Useful for versioning pickled models for instance.
    """
    repo = git.Repo(search_parent_directories=True)
    return repo.head.object.hexsha


def get_date_str(date_in: date = date.today()) -> str:
    """
    Get date in string format.
    Args:
        date_in: date object to transform to string
    """
    return date_in.strftime("%Y%m%d")


def get_time_str(time_in: datetime = datetime.now()) -> str:
    """
    Get time in string format.
    Args:
        time_in: datetime object to transform to string
    """
    return time_in.strftime("%Y%m%d_%H%M%S")


def add_version(file: str,
                version: str = get_git_hash(),
                end: bool = True) -> str:
    """
    Add version to a file. Useful for creating file names
     containing git hexsha or times.

    Args:
        file: file to version.
        version: string version to add.
        end: if version should be appended at the end.
         Otherwise it's appended at the beginning.
    """
    file_name, file_extension = os.path.splitext(file)
    if end:
        versioned_file = f"{file_name}_{version}{file_extension}"
    else:
        versioned_file = f"{version}_{file_name}{file_extension}"
    return versioned_file


def get_from_module(module: str, attribute: str) -> object:
    """
    Get attribute or function from a module.
    """
    return getattr(importlib.import_module(module), attribute)
