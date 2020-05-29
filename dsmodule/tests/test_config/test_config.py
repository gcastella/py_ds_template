import unittest

from dsmodule.config import *


class TestConfig(unittest.TestCase):
    def test_env_vars(self):
        """
        Test that env is set to dev, pre, or prod
        """
        env_sample_space = ['dev', 'pre', 'prod']
        self.assertIn(ENV, env_sample_space)
        self.assertEqual(config.environment, ENV)

    def test_config_files(self):
        """
        Test that yaml config files are passed from .env to config.
        """
        self.assertEqual(config.log_file, LOG_FILE)
        self.assertEqual(config.run_file, RUN_FILE)
        self.assertEqual(config.config_file, CONFIG_FILE)

    def test_no_env_level_config(self):
        """
        Test that config has no env or base keys.
        """
        self.assertEqual(config.get(ENV, "no_key"), "no_key")
        self.assertEqual(config.get("base", "no_key"), "no_key")
