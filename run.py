from sys import exit, argv
import random

from dice_game import DiceGame
import parse

if __name__ == "__main__":
    # Read in game variables
    temp = parse.parse(argv[1])
    numGames = temp[0]
    numDice = temp[1]
    verbose = temp[2]
    collect = temp[3]
    players = temp[4]

    # Initialize scores to 0
    scores = {}
    for player in players:
        scores[player[1]] = 0

    for _ in range(numGames):
        try:
            random.shuffle(players)
            if collect:
                winner = DiceGame(numDice, verbose, collect, players, argv[2]).simulate()
            else:
                winner = DiceGame(numDice, verbose, collect, players).simulate()
            scores[winner] += 1
        except ValueError as ve:
            print(ve)
            exit()
        except AssertionError as ae:
            print(ae)
            exit()
    
    # Turns scores into win percentages 
    winRates = {}
    for name, score in scores.items():
        winRates[name] = (score / numGames) * 100

    # Sorts from highest win percentage to lowest
    winRates = dict(sorted(winRates.items(), key = lambda kv: kv[1], reverse = True))

    # Prints win rates rounded to two decimal places
    print('Win rates:')
    for name, rate in winRates.items():
        print(name, '\t', '%0.2f' % rate, '%')