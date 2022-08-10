# Parent class for different player types, each with different moves
# No parameters
class Player:
    # Default constructor called during compilation

    def getBluff(
        self,
        prevMoves: list[tuple[tuple['Player', str], int, int]], 
        currentPlayer: str, 
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int
    ) -> int:
        pass

    # Returns tuple with the 0th index being a int indicating a move or a bluff call
    # The optional two indices that follow represent quantity and number, respectively
    def getMove(
        self, 
        prevMoves: list[tuple[tuple['Player', str], int, int]], 
        currentPlayer: str, 
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice : int
    ) -> tuple[int, int]:
        pass