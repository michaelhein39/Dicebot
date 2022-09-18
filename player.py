# Parent class for different player types, each with different moves
# No parameters
class Player:
    # Default constructor called during compilation

    # Returns 1 to indicate bluff call, or 0 to indicate no bluff call 
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

    # Returns tuple with quantity and dice number, respectively
    def getMove(
        self, 
        prevMoves: list[tuple[tuple['Player', str], int, int]], 
        currentPlayer: str, 
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice : int,
        numPlayers: int,
        playerTracker: dict  # Dict with string names as keys and how many dice they have left as values 
    ) -> tuple[int, int]:
        pass