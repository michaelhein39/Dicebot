from human import Human
from statistician import Statistician

players = [
    Human('Nick')
    Statistician('Seavy')
    Human('Mike')
    Human('Ant')
]

for round in rounds:
    players[round % NUM_PLAYERS].get_move()