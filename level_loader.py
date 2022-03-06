import json
import os

from config import Config
from level import Level


class LevelLoader:
	def __init__(self, config: Config, filename):
		self.config = config
		self.filename = filename
		self.levels = {}

	def load(self):
		if not os.path.exists(self.filename):
			self.levels[0] = Level(self.config)
			self.save()
			return
		with open(self.filename, 'r') as f:
			levels_data = json.load(f)

		for level_number_str, level_data in levels_data.items():
			level_number = int(level_number_str)

			level = Level(self.config, level_number)
			level.password = level_data.get('password')
			level.description = level_data.get('description')
			level.solution = level_data.get('solution')
			level.tip = level_data.get('tip')

			self.levels[level_number] = level

	def save(self):
		levels_data = {
			level.level_number: level.to_dict()
			for level in self.levels.values()
		}
		with open(self.filename, 'w') as f:
			json.dump(levels_data, f, indent='\t')

	def get_level(self, level_number: int) -> Level:
		return self.levels.get(level_number)

	def save_level(self, level: Level):
		self.levels[level.level_number] = level
		self.save()
