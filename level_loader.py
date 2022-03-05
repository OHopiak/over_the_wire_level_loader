import json
import os

from config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEVELS_FILE = os.path.join(BASE_DIR, "levels.json")


class LevelLoader:
	def __init__(self, filename):
		self.filename = filename


class Level:
	levels = {}

	def __init__(self, config: Config = None, level_num=1):
		self._config = config
		self.level_number = level_num
		self.username = config.username(level_num)
		self.password = None
		self.description = None
		self.tip = None
		self.solution = None

		self.load()

	def run(self):
		if not self.password:
			print("This level is not explored yet =)")
			exit(1)
		os.execv("/bin/expect", self.get_command())

	def get_command(self):
		return [
			"expect", "-c",
			f'spawn ssh {self.username}@{self._config.server_url} -p {self._config.server_port};' +
			f' expect "assword:"; send "{self.password}\n"; interact'
		]

	@staticmethod
	def __fetch_level_data():
		if os.path.exists(LEVELS_FILE):
			with open(LEVELS_FILE, "r") as f:
				data = f.read()
				if data:
					new_levels = json.loads(data)
					if new_levels:
						Level.levels = new_levels

	# if not Level.levels:
	# 	Level.levels = {
	# 		1: Level().to_dict()
	# 	}
	# 	Level.__save_level_data()

	@staticmethod
	def __save_level_data():
		with open(LEVELS_FILE, "w+") as f:
			f.write(json.dumps(Level.levels, indent=2))

	def save(self):
		Level.levels[str(self.level_number)] = self.to_dict()
		Level.__save_level_data()

	def load(self):
		Level.__fetch_level_data()
		current = Level.levels.get(str(self.level_number))
		if not current:
			current = {}
		self.password = current.get("password")
		self.description = current.get("description", "")
		self.tip = current.get("tip", "")
		self.solution = current.get("solution", "")

	def to_dict(self):
		return {
			"username": self.username,
			"description": self.description,
			"password": self.password,
			"solution": self.solution,
			"tip": self.tip,
		}

	def print_info(self):
		print("Level #{}".format(self.level_number))
		print('    Username: "{}"'.format(self.username))
		print('    Password: "{}"'.format(self.password))
		print('    Description: "{}"'.format(self.description))
