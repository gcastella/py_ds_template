import pickle
import typing


def read_pickle(file_name: str) -> typing.Any:
    """
    Read pickle file
    Args:
        file_name: file to read
    """
    with open(file_name, 'rb') as file:
        obj_pick = pickle.load(file)
    return obj_pick
