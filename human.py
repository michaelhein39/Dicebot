from player import Player
import time

# Child class of player.py
# Plays dice game based on manual inputs 
class Human(Player):
    # Default constructor called during compilation
    
    # Returns tuple with the 0th index being a int indicating a move or a bluff call
    # The optional two indices that follow represent quantity and number, respectively
    def getMove(
        self,
        prevMoves: list[tuple[tuple['Player', str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int
        ) -> tuple[str] | tuple[str, int, int]:

        # Prints an array of player's dice roll
        print("Here is your current roll:")
        roll = []
        for number in currentRoll.keys():
            for _ in range(currentRoll[number]):
                roll += [number]
        print(roll)
        time.sleep(1)
        print()

        # Only provides previous moves and offers option to call bluff if 
        # another player has already made a move 
        if prevMoves:
            # Prints previous moves in the round if desired
            print("Do you want to see the list of previous moves? (y/n)")
            while True:
                answer = input().lower().strip()
                print()

                if answer == "y":
                    for item in prevMoves:
                        if item[1] != 1:
                            print(item[0][1] + "\t" + str(item[1]) + "  " + str(item[2]) + "s")
                        else:
                            print(item[0][1] + "\t" + str(item[1]) + "  " + str(item[2]))
                    print()
                    break

                elif answer == "n":
                    break

                else:
                    print("Please enter either the letter 'y' or 'n'")


            # Returns a bluff call if desired
            print("Do you want to call bluff on the previous player? (y/n)")
            while True:
                answer = input().lower().strip()
                print()

                if answer == "y":
                    return ("CALL_BLUFF",)

                elif answer == "n":
                    break

                else:
                    print("Please enter either the letter 'y' or 'n'")


        print("For your move, enter the quantity desired, then in another line enter the dice number desired")

        # Accepts quantity of player's move
        if prevMoves:
            prevQuantity = prevMoves[-1][1]
            prevNum = prevMoves[-1][2]
        newQuantity = 0
        newNum = 0
        while True:
            answer = input().strip()
            
            if answer.isdigit():
                answer = int(answer)
            else:
                print()
                print("Input is not a digit ... Try giving the quantity again")
                continue

            if answer > 0:
                if prevMoves:
                    if answer > prevQuantity:
                        newQuantity = answer
                        break
                    elif answer == prevQuantity:
                        if prevNum != 6:
                            newQuantity = answer
                            break
                        else:
                            print()
                            print("You must increase the quantity since the previous dice number called was 6")
                    else:
                        print()
                        print("The quantity can't be less than the previous quantity called"
                        + " ... Try giving the quantity again")
                else: 
                    newQuantity = answer
                    break
            else:
                print()
                print("The quantity must be greater than 0 ... Try giving the quantity again")


        # Accepts dice number of player's move
        while True:
            answer = input().strip()

            if answer.isdigit():
                answer = int(answer)
            else:
                print()
                print("Input is not a digit ... Try giving the number again")
                continue

            if 1 <= answer <= 6:
                if prevMoves:
                    if newQuantity > prevQuantity:
                        newNum = answer 
                        break
                    else:
                        if answer > prevNum:
                            newNum = answer
                            break
                        else:
                            print()
                            print("The number must be greater than the previous number called"
                            + " ... Try giving the number again")
                else:
                    newNum = answer
                    break
            else:
                print()
                print("The number must be in the range 1-6 ... Try giving the number again")

        print()
        return ("MOVE", newQuantity, newNum)