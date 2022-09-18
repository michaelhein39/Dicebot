from player import Player
import random

# Child class of player.py
# Plays dice game based on simple probability strategies
class ConditionalLowLevelStat(Player):
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



    def aggressive(
        self,
        aggressiveQuantity: int,
        prevQuantity: int,
        prevNum: int,
        maxDiceNum: int
    ) -> tuple[int, int]:
        if aggressiveQuantity > prevQuantity:
            return (aggressiveQuantity, maxDiceNum)
        elif aggressiveQuantity == prevQuantity:
            returnQuantity = aggressiveQuantity if maxDiceNum > prevNum else aggressiveQuantity+1
            return (returnQuantity, maxDiceNum)
        elif aggressiveQuantity < prevQuantity:
            returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
            return (prevQuantity+1, returnNum)



    # Plays more conservatively when they have less dice than average
    # Plays more aggressively when they have more dice than average
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
        # Finds who has the most dice
        leaders = []
        maximum = 0
        for player in updatedPlayerTracker.keys():
            if updatedPlayerTracker[player] >= maximum:
                maximum = updatedPlayerTracker[player]
                leaders.append(player)

        # Find what dice number this player has the most of 
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
        avgOtherDice = otherDice / (numPlayers - 1)

        # Specific to dumb stat
        aggressiveQuantity = 0
        if maxDiceNum != 6:
            aggressiveQuantity = totalDice // 3 if totalDice >= 3 else 1
        else:
            aggressiveQuantity = totalDice // 6 if totalDice >= 6 else 1

        rand = random.randint(1, 6)

        if prevMoves:
            _, prevQuantity, prevNum = prevMoves[-1]
            if numOwnDice == 1:
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
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    returnQuantity = prevQuantity if returnNum > prevNum else prevQuantity+1
                    return (returnQuantity, returnNum)
            elif currentPlayer in leaders:
                return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
            elif numOwnDice < (avgOtherDice - 2):
                # Conservative 3/6 of the time
                if 1 <= rand <= 3:
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    returnQuantity = prevQuantity if returnNum > prevNum else prevQuantity+1
                    return (returnQuantity, returnNum)
                # Moderate 2/6 of the time
                elif 4 <= rand <= 5:
                    diff = aggressiveQuantity - prevQuantity
                    if diff <= 0:
                        return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
                    return (prevQuantity + random.randint(1, diff), maxDiceNum)
                # Aggressive 1/6 of the time 
                elif rand == 6:
                    return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
            elif numOwnDice < avgOtherDice:
                # Conservative 2/6 of the time
                if 1 <= rand <= 2:
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    returnQuantity = prevQuantity if returnNum > prevNum else prevQuantity+1
                    return (returnQuantity, returnNum)
                # Moderate 3/6 of the time
                elif 3 <= rand <= 5:
                    diff = aggressiveQuantity - prevQuantity
                    if diff <= 0:
                        return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
                    return (prevQuantity + random.randint(1, diff), maxDiceNum)
                # Aggressive 1/6 of the time 
                elif rand == 6:
                    return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
            elif numOwnDice == avgOtherDice:
                # Conservative 2/6 of the time
                if 1 <= rand <= 2:
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    returnQuantity = prevQuantity if returnNum > prevNum else prevQuantity+1
                    return (returnQuantity, returnNum)
                # Moderate 2/6 of the time
                elif 3 <= rand <= 4:
                    diff = aggressiveQuantity - prevQuantity
                    if diff <= 0:
                        return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
                    return (prevQuantity + random.randint(1, diff), maxDiceNum)
                # Aggressive 2/6 of the time 
                elif 5 <= rand <= 6:
                    return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
            elif numOwnDice > (avgOtherDice + 2):
                # Conservative 1/6 of the time
                if rand == 1:
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    returnQuantity = prevQuantity if returnNum > prevNum else prevQuantity+1
                    return (returnQuantity, returnNum)
                # Moderate 2/6 of the time
                elif 2 <= rand <= 3:
                    diff = aggressiveQuantity - prevQuantity
                    if diff <= 0:
                        return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
                    return (prevQuantity + random.randint(1, diff), maxDiceNum)
                # Aggressive 3/6 of the time 
                elif 4 <= rand <= 6:
                    return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
            elif numOwnDice > avgOtherDice:
                # Conservative 1/6 of the time
                if rand == 1:
                    returnNum = maxDiceNum if maxDiceNum != 6 else prevNum
                    returnQuantity = prevQuantity if returnNum > prevNum else prevQuantity+1
                    return (returnQuantity, returnNum)
                # Moderate 3/6 of the time
                elif 2 <= rand <= 4:
                    diff = aggressiveQuantity - prevQuantity
                    if diff <= 0:
                        return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)
                    return (prevQuantity + random.randint(1, diff), maxDiceNum)
                # Aggressive 2/6 of the time 
                elif 5 <= rand <= 6:
                    return self.aggressive(aggressiveQuantity, prevQuantity, prevNum, maxDiceNum)


        else:
            if numOwnDice == 1:
                if totalDice < 3:
                    if rand == 5:
                        return (1, 5)
                    elif rand == 6:
                        return (1, 6)
                    else:
                        return (1, maxDiceNum)
                else:
                    return (1, maxDiceNum)
            elif currentPlayer in leaders:
                return (aggressiveQuantity, maxDiceNum)
            elif numOwnDice < (avgOtherDice - 2):
                # Conservative 3/6 of the time
                if 1 <= rand <= 3:
                    return (1, maxDiceNum)
                # Moderate 2/6 of the time
                elif 4 <= rand <= 5:
                    return (random.randint(1, aggressiveQuantity), maxDiceNum)
                # Aggressive 1/6 of the time 
                elif rand == 6:
                    return (aggressiveQuantity, maxDiceNum)
            elif numOwnDice < avgOtherDice:
                # Conservative 2/6 of the time
                if 1 <= rand <= 2:
                    return (1, maxDiceNum)
                # Moderate 3/6 of the time
                elif 3 <= rand <= 5:
                    return (random.randint(1, aggressiveQuantity), maxDiceNum)
                # Aggressive 1/6 of the time 
                elif rand == 6:
                    return (aggressiveQuantity, maxDiceNum)
            elif numOwnDice == avgOtherDice:
                # Conservative 2/6 of the time
                if 1 <= rand <= 2:
                    return (1, maxDiceNum)
                # Moderate 2/6 of the time
                elif 3 <= rand <= 4:
                    return (random.randint(1, aggressiveQuantity), maxDiceNum)
                # Aggressive 2/6 of the time 
                elif 5 <= rand <= 6:
                    return (aggressiveQuantity, maxDiceNum)
            elif numOwnDice > (avgOtherDice + 2):
                # Conservative 1/6 of the time
                if rand == 1:
                    return (1, maxDiceNum)
                # Moderate 2/6 of the time
                elif 2 <= rand <= 3:
                    return (random.randint(1, aggressiveQuantity), maxDiceNum)
                # Aggressive 3/6 of the time 
                elif 4 <= rand <= 6:
                    return (aggressiveQuantity, maxDiceNum)
            elif numOwnDice > avgOtherDice:
                # Conservative 1/6 of the time
                if rand == 1:
                    return (1, maxDiceNum)
                # Moderate 3/6 of the time
                elif 2 <= rand <= 4:
                    return (random.randint(1, aggressiveQuantity), maxDiceNum)
                # Aggressive 2/6 of the time 
                elif 5 <= rand <= 6:
                    return (aggressiveQuantity, maxDiceNum)