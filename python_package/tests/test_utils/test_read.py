import os
import unittest

from python_package.utils.read import read_pickle
from python_package.utils.write import save_pickle


class TestRead(unittest.TestCase):
    def setUp(self):
        self.file_pkl = "test.pkl"
        self.obj_pkl = ["test1", "test2"]
        save_pickle(self.obj_pkl, self.file_pkl)

    def test_read_pkl(self):
        """
        Test that pickle file is read correctly.
        """
        self.assertEqual(read_pickle(self.file_pkl), self.obj_pkl)

    def tearDown(self):
        os.remove(self.file_pkl)
