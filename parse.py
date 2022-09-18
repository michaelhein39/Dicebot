from players import *

def parse(configFile: str) -> tuple[int, int, bool, bool, list]:
    with open(configFile) as file:
        numGames = int(file.readline())
        numDice = int(file.readline())

        if numDice < 1:
            print("Each player must have at least 1 die ... Please fix configurations")
            exit()

        # Verbose MUST be True if there is a Human player type
        if file.readline().strip() == 'True':
            verbose = True
        else:
            verbose = False

        # Collect should most likely be the opposite of verbose
        # unless data is being collected on a Human player type
        if file.readline().strip() == 'True':
            collect = True
        else:
            collect = False

        # Read in list of players with their types and names
        seen = set()
        players = []
        for line in file:
            temp = line.split()
            type = temp[0].lower()  # converts to lowercase for easy string comparison
            name = " ".join(temp[1:])

            # Checks if players have the same name
            if name in seen:
                print("Two players cannot have the same name ... Please fix configurations")
                exit()
            else:
                seen.add(name)

            # Matches type given to an existing player type class
            if type == "human":
                players.append((Human(), name))
            elif type == "conservativestat":
                players.append((ConservativeStat(), name))
            elif type == "aggressivelowlevelstat":
                players.append((AggressiveLowLevelStat(), name))
            elif type == "aggressivehighlevelstat":
                players.append((AggressiveHighLevelStat(), name))
            elif type == "conditionallowlevelstat":
                players.append((ConditionalLowLevelStat(), name))
            elif type == "conditionalhighlevelstat":
                players.append((ConditionalHighLevelStat(), name))
            elif type == "supremebot":
                players.append((SupremeBot(), name))
            else:
                print("One of the player types provided does not exist as a type ... "
                    + "Please fix configurations")
                exit()

    if len(seen) <= 1:
        print("There must be at least two players in the game ... Please fix configurations")
        exit()

    return (numGames, numDice, verbose, collect, players)