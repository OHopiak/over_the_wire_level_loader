import os
from unittest import TestCase

from level_loader import LevelLoader


class TestLevelLoader(TestCase):
	filename = "test_levels.json"

	def tearDown(self):
		if os.path.exists(self.filename):
			os.remove(self.filename)

	def test_has_filename_saved(self):
		loader = LevelLoader(self.filename)
		self.assertEqual(loader.filename, self.filename)

	# def test_load_non_existing_config(self):
