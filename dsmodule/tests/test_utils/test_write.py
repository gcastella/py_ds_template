import os
import unittest

from dsmodule.utils.read import read_pickle
from dsmodule.utils.write import save_pickle


class TestWrite(unittest.TestCase):
    def setUp(self):
        self.file_pkl = "test.pkl"
        self.obj_pkl = ["test1", "test2"]

    def test_save_pkl(self):
        """
        Test that pickle file is saved correctly.
        """
        save_pickle(self.obj_pkl, self.file_pkl)
        self.assertEqual(read_pickle(self.file_pkl), self.obj_pkl)

    def tearDown(self):
        os.remove(self.file_pkl)
