import importlib
import os
from datetime import date
from datetime import datetime
import pandas as pd
from pathlib import Path
import typing

import git


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
                path: str = "",
                version: str = get_time_str(),
                end: bool = True,
                **kwargs) -> str:
    """
    Add version to a file. Useful for creating file names
     containing git hexsha or times.

    Args:
        file: file to version.
        path: path of the file.
        version: string version to add.
        end: if version should be appended at the end.
         Otherwise it's appended at the beginning.
    """
    file_name, file_extension = os.path.splitext(file)
    if end:
        versioned_file = \
            Path(path) / f"{file_name}_{version}{file_extension}"
    else:
        versioned_file = \
            Path(path) / f"{version}_{file_name}{file_extension}"
    return str(versioned_file)


def get_from_module(module: str, name: str, **kwargs) -> typing.Callable:
    """
    Get attribute or function from a module.
    """
    attributes = name.split(".")
    curr_name = attributes.pop(0)
    mod = [getattr(importlib.import_module(module), curr_name)]
    while len(attributes) > 0:
        curr_name = attributes.pop(0)
        mod.append(getattr(mod[-1], curr_name))
    return mod[-1]


def func_def(module: str, name: str, params=None, **kwargs) -> typing.Callable:
    """
    Create a function call from function name and parameters.
    """
    if params is None:
        params = {}
    func = get_from_module(module=module, name=name)

    def custom_fun(*args, **kwargs):
        return func(*args, **kwargs, **params)

    return custom_fun


def is_number(s: str):
    """
    Checks if a string is a float.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def print_row(df: pd.Series):
    """
    Print every value in a pd.Series.
    """
    for value, index in zip(df, df.index):
        print(index, ": \n", value)
