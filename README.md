## Setup

Run the program with the following:
```
$ python3 dice_game.py <path-to-config-file>
```
A configuration file looks like the following:
```
# games
# starting dice per player
verbose? (True/False)
collecting data? (True/False)
FirstPlayerType FirstPlayerName
SecondPlayerType SecondPlayerName
...
LastPlayerType LastPlayerName
```
An example configuration file looks like the following:
```
1
3
True
False
Human Ant
Human Mikey
```