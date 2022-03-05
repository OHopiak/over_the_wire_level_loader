#!/usr/bin/env python
import argparse

from config import Config
from level_loader import Level


def get_parser(config: Config) -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description='Load the level of smash the stack quest')
	parser.add_argument("-l", dest='level', type=int,
						default=config.default_level, help=f"The level to load (default: {config.default_level})")
	parser.add_argument("-s", dest='save', action='store_true',
						help="Provide with password and additional info for level and save it")
	parser.add_argument("-i", dest='info', action='store_true')
	return parser


def save_level(config, level_num):
	level = Level(config=config, level_num=level_num)
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
	level.save()

	set_default = input("Set level as default? (Y/n): ")
	if set_default.lower() in ['', 'y']:
		config.set_default_level(level_num)
		config.save()


def main():
	config = Config('config.json')
	try:
		config.load()
	except RuntimeError as e:
		print(e)
		exit(1)
	args = get_parser(config).parse_args()
	level = Level(config=config, level_num=args.level)
	if args.info:
		level.print_info()
		exit(0)
	if args.save:
		save_level(config, args.level)
	else:
		level.print_info()
		level.run()


if __name__ == '__main__':
	main()
