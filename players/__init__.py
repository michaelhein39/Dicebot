# IMPORTANT
# If new player types are added here, you must add to the if/elif/else 
# statements near the end of the parse.py where the types provided in
# dice.cfg are matched to a class here

from players.human import Human
from players.dumbstatistician import DumbStatistician
from players.smartstatistician import SmartStatistician