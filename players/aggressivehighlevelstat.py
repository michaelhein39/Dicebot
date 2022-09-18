from player import Player
import random

# Child class of player.py
# Plays dice game based on more intelligent probability strategies
class AggressiveHighLevelStat(Player):
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

        if prevQuantity > totalDice or (prevQuantity == totalDice and prevNum == 6):
            return 1

        if totalDice >= 3:
            if prevNum != 6 and prevQuantity > totalDice / 3:
                return 1
            elif prevNum == 6 and prevQuantity > totalDice / 6:
                return 1
        elif totalDice < 3:
            diceNum = 0
            for num in currentRoll.keys():
                diceNum = num
            if prevQuantity == 1:
                if prevNum in currentRoll or diceNum == 6:
                    return 0
                else:
                    if diceNum > prevNum:
                        return 0
                    if random.randint(1, 3) == 1: return 1
                    else: return 0
            elif prevQuantity == 2:
                if prevNum not in currentRoll and diceNum != 6:
                    return 1
                if diceNum == 6:
                    if random.randint(1,3) == 1: return 1
                    else: return 0
                elif diceNum != 6:
                    return 1
        return 0


    # Returns highest probable quantity, and typically whichever 
    # dice number the player has most of
    def getMove(
        self,
        prevMoves: list[tuple[tuple[Player, str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int,
        numPlayers: int,
        updatedPlayerTracker: dict
    ) -> tuple[int, int]:
        maxDiceNum = 0
        count = 0
        for diceNum in currentRoll.keys():
            if currentRoll[diceNum] >= count and diceNum != 6:
                count = currentRoll[diceNum]
                maxDiceNum = diceNum
        if maxDiceNum == 0:
            maxDiceNum = 6
            count = 1
        
        otherDice = totalDice - numOwnDice
        optimalQuantity = otherDice // 3 + count

        if prevMoves:
            _, prevQuantity, prevNum = prevMoves[-1]
            if totalDice < 3:
                if prevQuantity == 1:
                    if maxDiceNum == 6:
                        return (2, prevNum)
                    elif maxDiceNum > prevNum:
                        return (prevQuantity, maxDiceNum)
                    else:
                        if prevNum == 6: return (2, maxDiceNum)
                        else: return (2, prevNum)
                elif prevQuantity == 2:
                    return (2, 6)
            else:
                if optimalQuantity > prevQuantity:
                    return (optimalQuantity, maxDiceNum)
                elif optimalQuantity == prevQuantity:
                    returnQuantity = optimalQuantity if maxDiceNum > prevNum else optimalQuantity+1
                    return (returnQuantity, maxDiceNum)
                elif optimalQuantity < prevQuantity:
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    return (prevQuantity+1, returnNum)
        else:
            if totalDice < 3:
                rand = random.randint(1, 6)
                if rand == 5:
                    return (1, 5)
                elif rand == 6:
                    return (1, 6)
                else:
                    return (1, maxDiceNum)
            else:
                return (optimalQuantity, maxDiceNum)