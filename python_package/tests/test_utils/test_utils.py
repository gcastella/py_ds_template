import re
import unittest

from python_package.utils import *


class TestUtils(unittest.TestCase):
    def test_get_git_hash(self):
        """
        Test that hex is returned.
        """
        p = re.compile("[0-9a-f]{5,40}")
        self.assertRegex(get_git_hash(), p)

    def test_get_date_str(self):
        """
        Test that date is returned.
        """
        d = date(2020, 5, 21)
        self.assertEqual(get_date_str(date_in=d), "20200521")

    def test_get_time_str(self):
        """
        Test that time is returned.
        """
        t = datetime(2020, 5, 21, 8, 0, 0)
        self.assertEqual(get_time_str(time_in=t), "20200521_080000")

    def test_add_version(self):
        """
        Test that version is added correctly.
        """
        t = datetime(2020, 5, 21, 8, 0, 0)
        self.assertEqual(
            add_version(file="test.csv",
                        version=get_time_str(time_in=t),
                        end=True),
            "test_20200521_080000.csv"
        )
        self.assertEqual(
            add_version(file="test.csv",
                        version=get_time_str(time_in=t),
                        end=False),
            "20200521_080000_test.csv"
        )

    def test_get_from_module(self):
        """
        Test that you can get attribute from package.
        """
        import pandas
        self.assertEqual(
            get_from_module(module="pandas", attribute="read_csv"),
            pandas.read_csv
        )
