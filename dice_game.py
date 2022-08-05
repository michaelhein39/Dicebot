from hashlib import new
from player import Player
from human import Human
from dumbstatistician import DumbStatistician
from smartstatistician import SmartStatistician
from sys import exit, argv
import time
import random


class DiceGame:
    def __init__(
            self, 
            numDice: int, 
            verbose: bool, 
            collect: bool, 
            players: list[tuple[Player, str]], 
            scores: dict
        ) -> None:
        self.numDice = numDice
        self.verbose = verbose
        self.collect = collect
        self.players = players
        self.scores = scores



    # Mutates diceRolls dictionary to simulate rolling every player's dice
    def rollAllDice(
        self, 
        diceRolls: dict,
        playerTracker: dict,
        toBeDeleted: list = []
        ) -> None:
        for player in playerTracker:
            if player in toBeDeleted:
                continue
            roll = {}
            for _ in range(playerTracker[player]):
                index = random.randint(1, 6)
                roll[index] = roll.get(index, 0) + 1
            diceRolls[player] = roll
        if self.verbose:
            print("The dice have been rolled!")
            time.sleep(2)
            print()



    def chooseBadInput(
        self,
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
        ) -> int:
        decDice = 0
        if self.verbose:
            print("That was a bad input!")
            print(player[1] + " loses a die and now has " + str(playerTracker[player]-1) + " left")
            time.sleep(2)
        playerTracker[player] -= 1
        totalDice -= 1
        decDice += 1
        if playerTracker[player] == 0:
            if self.verbose:
                print(player[1] + " is out of the game")
            del diceRolls[player]
            toBeDeleted += [player]
        if self.verbose:
            print()
        if self.verbose and len(diceRolls) > 1:
            print("There are " + str(totalDice) + " dice left on the table")
            time.sleep(2)
            print()
        # Empties previous moves list to prep for next round
        prevMoves.clear()
        # Re-rolls dice for everybody still in game
        if len(diceRolls) > 1:
            self.rollAllDice(diceRolls, playerTracker, toBeDeleted)
        # Returns boolean determining whether or not totalDice must be decremented
        return decDice



    def chooseMove(
        self,
        move: tuple[str, int, int],
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
        ) -> int:
        decDice = 0
        newQuantity = move[1]
        newNum = move[2]
        if prevMoves:   
            prevQuantity = prevMoves[-1][1]
            prevNum = prevMoves[-1][2]
            if newQuantity < prevQuantity or (newQuantity == prevQuantity and newNum <= prevNum):
                return self.chooseBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
        prevMoves += [(player, newQuantity, newNum)]
        if self.verbose:
            if newQuantity != 1:
                print(player[1] + " claims there are  " + str(newQuantity) + "  " + str(newNum) + "s")
            else:
                print(player[1] + " claims there is  " + str(newQuantity) + "  " + str(newNum))
            time.sleep(3)
            print()
        return decDice



    def chooseBluff(
        self,
        move: tuple[str, int, int],
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
        ) -> int:

        decDice = 0

        if not prevMoves: 
            return self.chooseBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)

        if self.verbose:
            print(player[1] + " calls bluff!")
            time.sleep(2)
            print()

        # Previous player
        prevPlayer = prevMoves[-1][0]
        # Number in question
        questioned = prevMoves[-1][2]
        # Quantity guessed by previous player
        guessOfQuestioned = prevMoves[-1][1]
        # Tracks quantity of number in question found among all rolls
        totalOfQuestioned = 0

        if self.verbose:
            if guessOfQuestioned != 1:
                print(prevPlayer[1] + " claimed there are  "
                + str(guessOfQuestioned) + "  " + str(questioned) + "s...")
            else:
                print(prevPlayer[1] + " claimed there is  "
                + str(guessOfQuestioned) + "  " + str(questioned) + "...")
            time.sleep(2)

        # Questioning the quantity of a number other than 6
        # Looking at the number in question along with wild 6s
        if questioned != 6:
            for player_ in diceRolls.keys():
                totalOfQuestioned += diceRolls[player_].get(questioned, 0)
                totalOfQuestioned += diceRolls[player_].get(6, 0)
        # Questioning how many 6s there are
        # Looking only at the number of wild 6s
        else:
            for player_ in diceRolls.keys():
                totalOfQuestioned += diceRolls[player_].get(questioned, 0)
        
        # Previous player was right
        if totalOfQuestioned >= guessOfQuestioned:
            if self.verbose:
                if totalOfQuestioned != 1:
                    print("And there are  " + str(totalOfQuestioned) + "  " + str(questioned) + "s!")
                else:
                    print("And there is  " + str(totalOfQuestioned) + "  " + str(questioned) + "!")
                time.sleep(2)
                print()
                print(player[1] + " loses a die and now has " + str(playerTracker[player]-1) + " left")
                time.sleep(2)
            playerTracker[player] -= 1
            totalDice -= 1
            decDice += 1
            if playerTracker[player] == 0:
                if self.verbose:
                    print(player[1] + " is out of the game")
                    time.sleep(1)
                del diceRolls[player]
                toBeDeleted += [player]
            if self.verbose:
                print()
            if self.verbose and len(diceRolls) > 1:
                print("There are " + str(totalDice) + " dice left on the table")
                time.sleep(2)
                print()

        # Previous player was wrong
        else:
            if self.verbose:
                if totalOfQuestioned != 1:
                    print("But there are only  " + str(totalOfQuestioned) + "  " + str(questioned) + "s!")
                else:
                    print("But there is only  " + str(totalOfQuestioned) + "  " + str(questioned) + "!")
                time.sleep(2)
                print()
                print(prevPlayer[1] + " loses a die and now has "
                + str(playerTracker[prevPlayer]-1) + " left")
                time.sleep(2)
            playerTracker[prevPlayer] -= 1
            totalDice -= 1
            decDice += 1
            if playerTracker[prevPlayer] == 0:
                if self.verbose:
                    print(prevPlayer[1] + " is out of the game")
                del diceRolls[prevPlayer]
                toBeDeleted += [prevPlayer]
            if self.verbose:
                print()
            if self.verbose and len(diceRolls) > 1:
                print("There are " + str(totalDice) + " dice left on the table")
                time.sleep(2)
                print()

        # Empties previous moves list to prep for next round
        prevMoves.clear()

        # Re-rolls dice for everybody still in game
        if len(diceRolls) > 1:
            self.rollAllDice(diceRolls, playerTracker, toBeDeleted)

        if player in diceRolls:
            # Ends iteration of players early if only one player remains
            if len(toBeDeleted) == len(playerTracker) - 1:
                return decDice

            if self.verbose:
                print(player[1] + "'s turn")
                time.sleep(1)

            # Gets tuple representing move of current player
            move = player[0].getMove(
                prevMoves[:],  # Defensive copy of previous moves
                player[1],  # String name of current player
                diceRolls[player].copy(),  # Defensive copy of player's dice roll
                self.verbose,
                totalDice
                )

            if  move[0].upper().strip() == 'MOVE':
                decDice += self.chooseMove(move, prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
            else:
                decDice += self.chooseBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)

        return decDice



    # Simulates one game
    def simulate(self) -> None:
        totalDice = len(self.players) * self.numDice

        # Signals new game to players
        if self.verbose:
            print("New game!")
            print()
            print("There are " + str(totalDice) + " dice on the table")
            if self.numDice != 1:
                print("Everybody has " + str(self.numDice) + " dice")
            else:
                print("Everybody has " + str(self.numDice) + " die")
            print()
            time.sleep(3)

        # Tracks who is in the game and how many dice they have left
        playerTracker = {}
        for player in self.players:
            playerTracker[player] = self.numDice

        # Initialize dice rolls for each player
        diceRolls = {}
        self.rollAllDice(diceRolls, playerTracker)
        
        # Tracks previous moves up until the most recent bluff call
        prevMoves = []

        # Continues game until only one player remains
        while len(playerTracker) > 1:
            # Tracks who must be deleted from game after one iteration of players
            toBeDeleted = []
            
            # Iterates through players remaining and takes in their moves
            for player in playerTracker.keys():
                # Ends iteration of players early if only one player remains
                if len(toBeDeleted) == len(playerTracker) - 1:
                    break

                if self.verbose:
                    print(player[1] + "'s turn")
                    time.sleep(1)

                # Gets tuple representing move of current player
                move = player[0].getMove(
                    prevMoves[:],  # Defensive copy of previous moves
                    player[1],  # String name of current player
                    diceRolls[player].copy(),  # Defensive copy of player's dice roll
                    self.verbose,
                    totalDice
                    )

                # Triggers the call made by player and tracks how much totalDice must be decremented 
                if  move[0].upper().strip() == 'MOVE':
                    decDice = self.chooseMove(move, prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
                elif move[0].upper().strip() == 'CALL_BLUFF':
                    decDice = self.chooseBluff(move, prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
                else:
                    decDice = self.chooseBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
                
                # Decrements total dice if necessary
                totalDice -= decDice

            # Deletes players who have no more dice
            for player in toBeDeleted:
                del playerTracker[player]

        winner = ''
        # Designates winner as last player remaining
        assert len(playerTracker) == 1, "Error: Game ended with multiple players still in dictionary"
        for player in playerTracker.keys():
            winner = player[1]

        self.scores[winner] += 1
        if self.verbose:
            print("GAME OVER")
            time.sleep(1)
            print("The winner is " + winner + "!")
            print()
            print('---------')
            print('Scores:')
            self.scores = dict(sorted(self.scores.items(), key = lambda kv: kv[1], reverse = True))
            for name, score in self.scores.items():
                print(name, '\t', score)
            print('---------')
            time.sleep(4)
            print()




if __name__ == "__main__":
    # Read in game variables
    players = []
    scores = {}
    with open(argv[1]) as file:
        numGames = int(file.readline())
        numDice = int(file.readline())

        # Verbose MUST be True if there is a Human player type
        verbose = bool(file.readline())

        # Collect should most likely be the opposite of verbose
        # unless data is being collected on a Human player type 
        collect = bool(file.readline())

        # Read in list of players with their types and names
        # Initialize scores to 0
        seen = set()
        for line in file:
            temp = line.split()
            type = temp[0].lower()  # converts to lowercase for easy string comparison
            name = " ".join(temp[1:])
            scores[name] = 0

            # Checks if players have the same name
            if name in seen:
                print('Two players cannot have the same name.\n\
                    Please fix configurations.')
                exit()
            else:
                seen.add(name)

            if type == "human":
                players.append((Human(), name))
            elif type == "dumbstatistician":
                players.append((DumbStatistician(), name))
            elif type == "smartstatistician":
                players.append((SmartStatistician(), name))
            else:
                print('One of the player types provided does not exist as a type.\n\
                    Please fix configurations.')

    for _ in range(numGames):
        try:
            DiceGame(numDice, verbose, collect, players, scores).simulate()
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
