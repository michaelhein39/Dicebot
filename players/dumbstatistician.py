from player import Player
import random

# Child class of player.py
# Plays dice game based on simple probability strategies
class DumbStatistician(Player):
    # Default constructor called during compilation


    # Calls bluff if the previous quantity called is greater than 1/3 of the total dice,
    # except when the dice number called is 6, in which case the threshold is 1/6
    def getBluff(
        self, 
        prevMoves: list[tuple[tuple[Player, str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int
    ) -> int:
        _, prevQuantity, prevNum = prevMoves[-1]
        if prevNum != 6 and prevQuantity > totalDice / 3:
            return 1
        elif prevNum == 6 and prevQuantity > totalDice / 6:
            return 1
        else:
            return 0


    # Returns tuple with the 0th index being a int indicating a move or a bluff call
    # The optional two indices that follow represent quantity and number, respectively
    def getMove(
        self, 
        prevMoves: list[tuple[tuple[Player, str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int
    ) -> tuple[int, int]:
        if prevMoves:
            _, prevQuantity, prevNum = prevMoves[-1]
            return (prevQuantity+1, prevNum)
        else:
            return (1, random.randint(1,6))