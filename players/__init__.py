# IMPORTANT
# If new player types are added here, you must add to the if/elif/else 
# statements near the end of the parse.py where the types provided in
# dice.cfg are matched to a class here

from players.human import Human
from players.conservativestat import ConservativeStat
from players.aggressivelowlevelstat import AggressiveLowLevelStat
from players.aggressivehighlevelstat import AggressiveHighLevelStat
from players.conditionallowlevelstat import ConditionalLowLevelStat
from players.conditionalhighlevelstat import ConditionalHighLevelStat
from players.supremebot import SupremeBot