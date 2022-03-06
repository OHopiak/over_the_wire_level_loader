import json
import os
from unittest import TestCase

from config import Config
from level_loader import LevelLoader


class TestLevelLoader(TestCase):
	filename = "test_levels.json"

	def setUp(self):
		self.config = Config('')
		self.config.config = {
			"SERVER_URL": "TEST.labs.overthewire.org",
			"SERVER_PORT": 2220,
			"USERNAME_FORMAT": "TEST{}",
			"DEFAULT_LEVEL": 1,
		}

	def tearDown(self):
		if os.path.exists(self.filename):
			os.remove(self.filename)

	def test_has_filename_saved(self):
		loader = LevelLoader(self.config, self.filename)
		self.assertEqual(loader.filename, self.filename)

	def test_load_non_existing_config(self):
		loader = LevelLoader(self.config, self.filename)
		loader.load()
		self.assertTrue(os.path.exists(self.filename))
		self.assertEqual(len(loader.levels), 1)

	def test_get_default_level(self):
		loader = LevelLoader(self.config, self.filename)
		loader.load()
		level = loader.get_level(0)
		self.assertEqual(level.level_number, 0)
		self.assertEqual(level.username, 'TEST0')
		self.assertEqual(level.password, 'TEST0')
		self.assertEqual(len(loader.levels), 1)

	def test_load_existing_config_one_entry(self):
		expected_levels = {
			'0': {
				"username": "TEST0",
				"password": "Some Random Password",
				"description": "Description",
				"solution": "Solution",
				"tip": "Tip"
			}
		}
		with open(self.filename, 'w') as f:
			json.dump(expected_levels, f)

		loader = LevelLoader(self.config, self.filename)
		loader.load()
		level = loader.get_level(0)
		self.assertEqual(level.level_number, 0)
		self.assertEqual(level.username, 'TEST0')
		self.assertEqual(level.password, 'Some Random Password')
		self.assertEqual(level.description, 'Description')
		self.assertEqual(level.solution, 'Solution')
		self.assertEqual(level.tip, 'Tip')

		self.assertEqual(len(loader.levels), 1)

	def test_load_existing_config_multiple_entries(self):
		expected_levels = {
			'0': {
				"username": "TEST0",
				"password": "Some Random Password",
				"description": "Description",
				"solution": "Solution",
				"tip": "Tip"
			},
			'1': {
				"username": "TEST1",
				"password": "Some Random Password 2",
				"description": "Description 2",
				"solution": "Solution 2",
				"tip": "Tip 2"
			},
		}
		with open(self.filename, 'w') as f:
			json.dump(expected_levels, f)

		loader = LevelLoader(self.config, self.filename)
		loader.load()
		level = loader.get_level(1)
		self.assertEqual(level.level_number, 1)
		self.assertEqual(level.username, 'TEST1')
		self.assertEqual(level.password, 'Some Random Password 2')
		self.assertEqual(level.description, 'Description 2')
		self.assertEqual(level.solution, 'Solution 2')
		self.assertEqual(level.tip, 'Tip 2')

		self.assertEqual(len(loader.levels), 2)

	def test_save_default_level(self):
		expected_levels = {
			'0': {
				"username": "TEST0",
				"password": "Some Random Password",
				"description": "Description",
				"solution": "Solution",
				"tip": "Tip"
			}
		}

		loader = LevelLoader(self.config, self.filename)
		loader.load()
		level = loader.get_level(0)

		level.password = "Some Random Password"
		level.description = "Description"
		level.solution = "Solution"
		level.tip = "Tip"

		loader.save_level(level)

		with open(self.filename, 'r') as f:
			levels_data = json.load(f)
		self.assertEqual(levels_data, expected_levels)

		self.assertEqual(len(loader.levels), 1)

	def test_save_existing_level(self):
		saved_levels = {
			'0': {
				"username": "TEST0",
				"password": "Some Random Password",
				"description": "Description",
				"solution": "Solution",
				"tip": "Tip"
			},
			'1': {
				"username": "TEST1",
				"password": "Some Random Password 2",
				"description": "Description 2",
				"solution": "Solution 2",
				"tip": "Tip 2"
			},
		}

		with open(self.filename, 'w') as f:
			json.dump(saved_levels, f)

		expected_levels = {
			'0': {
				"username": "TEST0",
				"password": "Some Random Password 3",
				"description": "Description 3",
				"solution": "Solution 3",
				"tip": "Tip 3"
			},
			'1': {
				"username": "TEST1",
				"password": "Some Random Password 2",
				"description": "Description 2",
				"solution": "Solution 2",
				"tip": "Tip 2"
			},
		}

		loader = LevelLoader(self.config, self.filename)
		loader.load()
		level = loader.get_level(0)
		level.password = "Some Random Password 3"
		level.description = "Description 3"
		level.solution = "Solution 3"
		level.tip = "Tip 3"

		loader.save_level(level)

		with open(self.filename, 'r') as f:
			levels_data = json.load(f)
		self.assertEqual(levels_data, expected_levels)

		self.assertEqual(len(loader.levels), 2)
