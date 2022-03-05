import json
import os
from unittest import TestCase

from config import Config, LoadingError


class TestConfig(TestCase):
	filename = "test_config.json"

	def tearDown(self):
		if os.path.exists(self.filename):
			os.remove(self.filename)

	def test_has_filename_saved(self):
		config = Config(self.filename)
		self.assertEqual(config.filename, self.filename)

	def test_load_non_existing_config(self):
		config = Config(self.filename)
		self.assertRaises(LoadingError, lambda: config.load())
		self.assertTrue(os.path.exists(self.filename))

	def test_load_existing_config(self):
		expected_config = {
			"SERVER_URL": "TEST.labs.overthewire.org",
			"SERVER_PORT": 2220,
			"USERNAME_FORMAT": "TEST{}",
			"DEFAULT_LEVEL": 1,
		}

		with open(self.filename, 'w') as f:
			json.dump(expected_config, f)

		config = Config(self.filename)
		config.load()

		self.assertEqual(config.server_url, expected_config.get('SERVER_URL'))
		self.assertEqual(config.server_port, expected_config.get('SERVER_PORT'))
		self.assertEqual(config.default_level, expected_config.get('DEFAULT_LEVEL'))
		self.assertEqual(config.username(1), 'TEST1')

	def test_set_default_level(self):
		config = Config(self.filename)
		default_level = 123
		config.set_default_level(default_level)
		self.assertEqual(config.default_level, default_level)