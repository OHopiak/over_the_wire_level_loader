#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from config import Config
from level import Level
from level_loader import LevelLoader

BASE_DIR = Path(__file__).resolve().parent
LEVELS_FILE = os.path.join(BASE_DIR, "levels.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def get_parser(config: Config) -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description='Load the level of smash the stack quest')
	parser.add_argument("-l", dest='level', type=int,
						default=config.default_level, help=f"The level to load (default: {config.default_level})")
	parser.add_argument("-s", dest='save', action='store_true',
						help="Provide with password and additional info for level and save it")
	parser.add_argument("-i", dest='info', action='store_true')
	return parser


def save_level(config: Config, level_loader: LevelLoader, level_num: int):
	level = level_loader.get_level(level_num)
	if not level:
		level = Level(config, level_num)

	print("Saving/editing the level #{}".format(level_num))
	print("  (Press enter to ignore)")
	pass_prompt = " [ {} ]".format(level.password) if level.password else ""
	password = input(
		"Enter the password for the level{}: ".format(pass_prompt))
	if password:
		level.password = password
	desc_prompt = " [ {} ]".format(
		level.description) if level.description else ""
	desc = input("Enter the description for the level{}: ".format(desc_prompt))
	if desc:
		level.description = desc

	level_loader.save_level(level)

	set_default = input("Set level as default? (Y/n): ")
	if set_default.lower() in ['', 'y']:
		config.set_default_level(level_num)
		config.save()


def main():
	config = Config(CONFIG_FILE)
	try:
		config.load()
	except RuntimeError as e:
		print(e)
		exit(1)
	level_loader = LevelLoader(config, LEVELS_FILE)
	level_loader.load()

	args = get_parser(config).parse_args()

	if args.save:
		save_level(config, level_loader, args.level)
		return

	level = level_loader.get_level(args.level)
	level.print_info(verbose=args.info)
	if not args.info:
		level.run()


if __name__ == '__main__':
	main()
