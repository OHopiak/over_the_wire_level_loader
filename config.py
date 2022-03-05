import json
import os.path


class Config:
	DEFAULT_CONFIG = {
		"SERVER_URL": "WARGAME.labs.overthewire.org",
		"SERVER_PORT": 2220,
		"USERNAME_FORMAT": "WARGAME{}",
		"DEFAULT_LEVEL": 1,
	}

	def __init__(self, filename):
		self.filename = filename
		self.config = self.DEFAULT_CONFIG

	def load(self):
		if not os.path.exists(self.filename):
			self.save()
			raise LoadingError(self.filename)
		with open(self.filename, 'r') as f:
			self.config = json.load(f)

	def save(self):
		with open(self.filename, 'w') as f:
			json.dump(self.config, f, indent='\t')

	@property
	def server_url(self) -> str:
		return self.config.get('SERVER_URL')

	@property
	def server_port(self) -> int:
		return self.config.get('SERVER_PORT')

	def username(self, level_num: int = 0) -> str:
		return self.config.get('USERNAME_FORMAT').format(level_num)

	@property
	def default_level(self) -> int:
		return self.config.get('DEFAULT_LEVEL')

	def set_default_level(self, default_level):
		self.config['DEFAULT_LEVEL'] = default_level



class LoadingError(RuntimeError):
	def __init__(self, filename):
		super().__init__(f"Please, fill the config with appropriate values for your wargame ({filename})")
