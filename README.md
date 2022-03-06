# OverTheWire SSH Level Loader

## Dependencies
* Linux
* Python 3.7 or higher
* `/usr/bin/expect` executable.

## How to use

### Initial usage

1. Clone this repo to your workspace
2. Rename the cloned folder to your wargame (e.g. Bandit)
3. Run `./start.py` once
4. Edit `config.json` accordingly to the data on the OverTheWire website for your wargame
5. Run `./start.py` again. You will load the default level for the wargame.
6. Solve the level

### Saving the level info

1. Run `./start.py -s -l <level num>`
2. Fill the correct data (leave empty and press enter to skip)
3. The level will be saved in `levels.json`

> After initial usage `levels.json` will be created with the default level

### Subsequent usage
* Run `./start.py -l <level num>` to load a specific level
* Run `./start.py` to load the current level

### Printing the level information
* Run `./start.py -i -l <level num>` to print info for a specific level
* Run `./start.py -i` to print info for the current level

## Notes

> I found out, that some levels on Bandit do not work properly when using
> the loader, so if you have any troubles with the loader, just copy the SSH
> command that is printed out and run the ssh connection the usual way
> If you manage to find this bug and find the way to solve it, you are welcome 
> to make a PR.

> If you want to experiment and modify this script, be sure to back up your `levels.json`
> as it contains all saved passwords to the levels. It would be unfortunate to lose 
> all of them at once.

> Please, respect the rules of OverTheWire and do not share your levels.json files.
> You should make sure that it is in `.gitignore` and is not leaked to your repo.

> You can manually add text for solutions and tips in `levels.json`

> If you consider json format uncomfortable for you, you can port this script to `yaml`
> Be sure to add the config and levels file to `.gitignore`!
> If you manage to make both json and yaml work together, without much complication
> feel free to make a PR.
