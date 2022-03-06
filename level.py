import os

from config import Config


class Level:
	levels = {}

	def __init__(self, config: Config = None, level_num=0, password='', description='', tip='', solution=''):
		self.level_number = level_num
		if config:
			self._config = config
			self.username = config.username(level_num)
		else:
			self.username = None
		if level_num == 0:
			password = self.username
		self.password = password
		self.description = description
		self.tip = tip
		self.solution = solution

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

	def to_dict(self):
		return {
			"username": self.username,
			"password": self.password,
			"description": self.description,
			"solution": self.solution,
			"tip": self.tip,
		}

	def print_info(self, verbose=False):
		print(f"Level #{self.level_number}")
		print(f'    Username: "{self.username}"')
		print(f'    Password: "{self.password}"')
		if self.description:
			print(f'    Description: "{self.description}"')
		if self.solution and verbose:
			print(f'    Description: "{self.solution}"')
		if self.tip and verbose:
			print(f'    Description: "{self.tip}"')