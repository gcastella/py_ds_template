import pickle
import typing


def save_pickle(obj: typing.Any, file_name: str) -> None:
    """
    Save object in pickle file.
    Args:
        obj: object to dump.
        file_name: file name to dump to.
    """
    with open(file_name, 'ab') as file:
        pickle.dump(obj, file)
