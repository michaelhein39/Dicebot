from player import Player
import random

# Child class of player.py
# Plays dice game based on more intelligent probability strategies
class SmartStatistician(Player):
    # Default constructor called during compilation
    
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
        otherDice = totalDice - numOwnDice
        if prevNum != 6 and prevQuantity > (otherDice / 3 + currentRoll.get(prevNum, 0)):
            return 1
        elif prevNum == 6 and prevQuantity > (otherDice / 6 + currentRoll.get(prevNum, 0)):
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