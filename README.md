## The Dice Game

Each player starts with the same number of dice.

The game proceeds in rounds, with everyone rolling and immediately hiding their dice at the start of each round (so that a player may only see their own dice).

Players have the option to make a *move* or *call bluff* on the previous move.

A move is given by stating a quantity and a die number (1-6). If a player chooses to move, they must give a quantity that is greater than or equal to the previous quantity given. If the current player moves and gives the same quantity as the previous player, the current player must give a die number that is greater than the previously given die number. (If the current player moves and gives a quantity that is strictly greater than the previous quantity given, then they may give *any* die number.)

For example, if I call 2 "4"s and you are next to move, you can call 3, 4, 5, (etc.) of *any* die number, or you can call 2 "5"s or  2 "6"s.

Or, if you do not think that there are 2 "4s" among all the dice in play, then you can *call bluff*. In that case, everyone in the game shows their rolls. If there are 2 or more "4"s as previously called, then the player who called bluff is wrong and they lose one die. If there are less than 2 "4"s, then the player who moved previously is wrong and they lose one die.

In this game, 6s are wild and thus can count as any die number. So if players have to show their "4"s after a bluff call, they must show all of their "4"s AND "6"s. Note though that if players must show their "6"s, they only show "6"s.

The player who called bluff always starts the next round by making a move (unless that player is out, in which case the next
player in the rotation goes). A player is out of the game if they no longer have any dice. The last player in the game
is the winner.

## Setup

Run the program with the following:
```
$ python3 run.py <path-to-config-file> <path-to-output-file>
```
A configuration file looks like the following:
```
# of games
# of starting dice per player
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