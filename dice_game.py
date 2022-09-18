import time
import random

from player import Player

class DiceGame:
    def __init__(
        self, 
        numDice: int, 
        verbose: bool, 
        collect: bool, 
        players: list[tuple[Player, str]],
        outputFile: str = None
    ) -> None:
        self.numDice = numDice
        self.verbose = verbose
        self.collect = collect
        self.players = players
        self.outputFile = outputFile



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



    def handleLoseDie(
        self,
        player: tuple[Player, str],
        playerTracker: dict,
        totalDice: int,
        diceRolls: dict,
        toBeDeleted: list,
        prevMoves: list[tuple[Player, int, int]]
    ) -> None:
        if self.verbose:
            print(player[1] + " loses a die and now has " + str(playerTracker[player]-1) + " left")
            time.sleep(2)
        playerTracker[player] -= 1
        totalDice -= 1
        if playerTracker[player] == 0:
            if self.verbose:
                print(player[1] + " is out of the game")
            del diceRolls[player]
            toBeDeleted += [player]
        if self.verbose:
            print()
            if len(diceRolls) > 1:
                print("There are " + str(totalDice) + " dice left on the table")
                time.sleep(2)
                print()

        # Empties previous moves list to prep for next round
        prevMoves.clear()

        # Re-rolls dice for everybody still in game
        if len(diceRolls) > 1:
            self.rollAllDice(diceRolls, playerTracker, toBeDeleted)



    # Takes a die away from the player and enters next round if player gives bad input
    # Returns 1 to indicate totalDice must be decremented by 1
    def handleBadInput(
        self,
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
    ) -> int:
        if self.verbose:
            print("That was a bad input!")

        # Makes player lose a die and rolls dice for next round
        self.handleLoseDie(player, playerTracker, totalDice, diceRolls, toBeDeleted, prevMoves)

        # Returns 1 to decrement totalDice by 1 
        return 1



    # Continue round by tracking a new move 
    # Returns an int indicating how much totalDice must be decremented 
    def handleMove(
        self,
        move: tuple[int, int],
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
    ) -> int:
        newQuantity, newNum = move

        # Checks for bad input based on previous moves
        if prevMoves:
            _, prevQuantity, prevNum = prevMoves[-1]
            if newQuantity < prevQuantity or (newQuantity == prevQuantity and newNum <= prevNum):
                # Always returns 1
                return self.handleBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
        
        # Checks that move is otherwise valid
        if newQuantity < 1 or newNum < 1 or newNum > 6:
            return self.handleBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)

        # Keeps track of new move and returns 0 so totalDice is NOT decremented
        prevMoves.append((player, newQuantity, newNum))
        if self.verbose:
            if newQuantity != 1:
                print(player[1] + " claims there are  " + str(newQuantity) + "  " + str(newNum) + "s")
            else:
                print(player[1] + " claims there is  " + str(newQuantity) + "  " + str(newNum))
            time.sleep(3)
            print()
        
        # Creates csv of totalDice, name of player, # of dice player has, quantity of call,
        # dice number of call, then how many of each dice value 1-6 in order with 0s when
        # player has none of that value 
        if self.collect:
            with open(self.outputFile, "a") as file:
                file.write(str(totalDice) + ",")
                file.write(player[1] + ",")
                file.write(str(playerTracker[player]) + ",")
                file.write(str(newQuantity) + ",")
                file.write(str(newNum) + ",")
                file.write(str(diceRolls[player].get(1, 0)) + ",")
                file.write(str(diceRolls[player].get(2, 0)) + ",")
                file.write(str(diceRolls[player].get(3, 0)) + ",")
                file.write(str(diceRolls[player].get(4, 0)) + ",")
                file.write(str(diceRolls[player].get(5, 0)) + ",")
                file.write(str(diceRolls[player].get(6, 0)) + "\n")

        return 0



    # Ends round with bluff call
    # Returns 1 indicating that totalDice must be decremented by 1
    def handleBluff(
        self,
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
    ) -> int:
        # Checks if bluff is called at start of round
        if not prevMoves: 
            return self.handleBadInput(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)

        if self.verbose:
            print(player[1] + " calls bluff!")
            time.sleep(2)
            print()

        # Previous player, quantity guessed by previous player, and dice number in question
        prevPlayer, guessOfQuestioned, questioned = prevMoves[-1]

        # Tracks actual quantity of dice number in question found among all rolls
        totalOfQuestioned = 0

        if self.verbose:
            if guessOfQuestioned != 1:
                print(prevPlayer[1] + " claimed there are  "
                + str(guessOfQuestioned) + "  " + str(questioned) + "s...")
            else:
                print(prevPlayer[1] + " claimed there is  "
                + str(guessOfQuestioned) + "  " + str(questioned) + "...")
            time.sleep(2)

        # Tracks the number in question along with wild 6s if necessary
        for player_ in diceRolls.keys():
            totalOfQuestioned += diceRolls[player_].get(questioned, 0)
            if questioned != 6:
                totalOfQuestioned += diceRolls[player_].get(6, 0)
        
        # Previous player was right
        if totalOfQuestioned >= guessOfQuestioned:
            if self.verbose:
                if totalOfQuestioned != 1:
                    print("And there are  " + str(totalOfQuestioned) + "  " + str(questioned) + "s!")
                else:
                    print("And there is  " + str(totalOfQuestioned) + "  " + str(questioned) + "!")
                time.sleep(2)
                print()
            self.handleLoseDie(player, playerTracker, totalDice, diceRolls, toBeDeleted, prevMoves)

        # Previous player was wrong
        else:
            if self.verbose:
                if totalOfQuestioned != 1:
                    print("But there are only  " + str(totalOfQuestioned) + "  " + str(questioned) + "s!")
                else:
                    print("But there is only  " + str(totalOfQuestioned) + "  " + str(questioned) + "!")
                time.sleep(2)
                print()
            self.handleLoseDie(prevPlayer, playerTracker, totalDice, diceRolls, toBeDeleted, prevMoves)

        # There is one less die after every bluff call
        return 1



    # Triggers bluff call then allows player who called bluff to make the next move 
    # Returns an int indicating how much totalDice must be decremented
    def step(
        self,
        prevMoves: list[tuple[Player, int, int]],
        playerTracker: dict,
        diceRolls: dict,
        toBeDeleted: list,
        player: tuple[Player, str],
        totalDice: int
    ) -> int:
        decDice = self.handleBluff(prevMoves, playerTracker, diceRolls, toBeDeleted, player, totalDice)
        totalDice -= 1
        if player in diceRolls:
            # Ends iteration of players early if only one player remains
            if len(toBeDeleted) == len(playerTracker) - 1:
                return decDice

            if self.verbose:
                print(player[1] + "'s turn")
                time.sleep(1)
                print("Here is your current roll:")
                roll = []
                for number in diceRolls[player].keys():
                    for _ in range(diceRolls[player][number]):
                        roll += [number]
                print(roll)
                time.sleep(1)
                print()

            # Copies playerTracker, minus the players who are out
            playerTrackerCopy = {}
            for player_ in playerTracker.keys():
                if player_ in toBeDeleted:
                    continue
                # Inserts pairs into the copy with just the string name as the key
                playerTrackerCopy[player_[1]] = playerTracker[player_]

            # Gets tuple representing move of current player
            move = player[0].getMove(
                prevMoves[:],  # Defensive copy of previous moves
                player[1],  # String name of current player
                diceRolls[player].copy(),  # Defensive copy of player's dice roll
                self.verbose,
                totalDice,
                playerTracker[player],  # Num of dice player has
                len(diceRolls),  # Num of players left
                playerTrackerCopy  # Players in the game and how many dice they have 
                )
            # Checks if move is valid tuple
            if (isinstance(move, tuple) and len(move) == 2 and 
                isinstance(move[0], int) and isinstance(move[1], int)):
                # Handles move and tracks how much to decrement totalDice 
                decDice += self.handleMove(move, prevMoves, playerTracker, diceRolls, 
                toBeDeleted, player, totalDice)
            else:
                # Handles bad input and tracks how much to decrement totalDice
                decDice += self.handleBadInput(prevMoves, playerTracker, diceRolls, 
                toBeDeleted, player, totalDice)

        return decDice



    # Simulates one game
    def simulate(self) -> str:
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

                # This is needed in the special case where the first player in cycle calls 
                # bluff and the last player is out of the game, but still in playerTracker
                # as we cycle down to that last player
                if player in toBeDeleted:
                    continue

                # Prints whose turn it is and an array of their dice roll 
                if self.verbose:
                    print(player[1] + "'s turn")
                    time.sleep(1)
                    print("Here is your current roll:")
                    roll = []
                    for number in diceRolls[player].keys():
                        for _ in range(diceRolls[player][number]):
                            roll += [number]
                    print(roll)
                    time.sleep(1)
                    print()

                decDice = 0

                # Copies playerTracker, minus the players who are out
                playerTrackerCopy = {}
                for player_ in playerTracker.keys():
                    if player_ in toBeDeleted:
                        continue
                    # Inserts pairs into the copy with just the string name as the key
                    playerTrackerCopy[player_[1]] = playerTracker[player_]

                # Allows for bluff call when there are previous moves
                if prevMoves:
                    # Requires player to return 1 to call bluff or return 0 to go on and make a move
                    switch = player[0].getBluff(
                        prevMoves[:],  # Defensive copy of previous moves
                        player[1],  # String name of current player
                        diceRolls[player].copy(),  # Defensive copy of player's dice roll
                        self.verbose,
                        totalDice,
                        playerTracker[player]  # Num of dice player has
                        )

                    # Triggers bluff call
                    if switch == 1:
                        # Handles bluff call, allows player to make first move of next round,
                        # and tracks how much to decrement totalDice
                        decDice = self.step(prevMoves, playerTracker, diceRolls, 
                        toBeDeleted, player, totalDice)

                    # Triggers move
                    elif switch == 0:
                        # Gets tuple representing move of current player
                        move = player[0].getMove(
                            prevMoves[:],  # Defensive copy of previous moves
                            player[1],  # String name of current player
                            diceRolls[player].copy(),  # Defensive copy of player's dice roll
                            self.verbose,
                            totalDice,
                            playerTracker[player],  # Num of dice player has
                            len(diceRolls),  # Num of players left
                            playerTrackerCopy  # Players in the game and how many dice they have 
                            )
                        # Checks if move is valid tuple
                        if (isinstance(move, tuple) and len(move) == 2 and 
                            isinstance(move[0], int) and isinstance(move[1], int)):
                            # Handles move and tracks how much to decrement totalDice 
                            decDice = self.handleMove(move, prevMoves, playerTracker, diceRolls, 
                            toBeDeleted, player, totalDice)
                        else:
                            # Handles bad input and tracks how much to decrement totalDice
                            decDice = self.handleBadInput(prevMoves, playerTracker, diceRolls, 
                            toBeDeleted, player, totalDice)

                    # Triggers bad input 
                    else:
                        if self.verbose:
                            print("Players must return 1 to call bluff or 0 to continue and make a move")
                        # Handles bad input and tracks how much to decrement totalDice
                        decDice = self.handleBadInput(prevMoves, playerTracker, diceRolls, 
                        toBeDeleted, player, totalDice)


                # Does not allow for bluff call at beginning of a round
                else:
                    # Gets tuple representing move of current player
                    move = player[0].getMove(
                        prevMoves[:],  # Defensive copy of previous moves
                        player[1],  # String name of current player
                        diceRolls[player].copy(),  # Defensive copy of player's dice roll
                        self.verbose,
                        totalDice,
                        playerTracker[player],  # Num of dice player has
                        len(diceRolls),  # Num of players left
                        playerTrackerCopy  # Players in the game and how many dice they have 
                        )
                    # Handles move and tracks how much to decrement totalDice
                    decDice = self.handleMove(move, prevMoves, playerTracker, diceRolls, 
                    toBeDeleted, player, totalDice)


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

        # Prints winner if verbose
        if self.verbose:
            print("GAME OVER")
            time.sleep(1)
            print("The winner is " + winner + "!")
            print()
        
        return winner