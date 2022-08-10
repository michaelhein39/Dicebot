from player import Player
import time

# Child class of player.py
# Plays dice game based on manual inputs 
class Human(Player):
    # Default constructor called during compilation



    # Returns 1 to call bluff or 0 to NOT call bluff
    def getBluff(
        self,
        prevMoves: list[tuple[tuple[Player, str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int
    ) -> int:
        # Prints previous moves in the round if desired
        print("Do you want to see the list of previous moves? (y/n)")
        while True:
            answer = input().lower().strip()
            print()

            if answer == "y":
                for item in prevMoves:
                    plural = item[1] != 1
                    extend = "s" if plural else ""
                    print(item[0][1] + "\t" + str(item[1]) + "  " + str(item[2]) + extend)
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
                return 1

            elif answer == "n":
                return 0

            else:
                print("Please enter either the letter 'y' or 'n'")



    # Returns tuple with the quantity and number of a move, respectively 
    def getMove(
        self,
        prevMoves: list[tuple[tuple[Player, str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int
    ) -> tuple[int, int]:
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
                print("Input is not a positive digit ... Try giving the quantity again")
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
                print("Input is not a positive digit ... Try giving the number again")
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
        return (newQuantity, newNum)