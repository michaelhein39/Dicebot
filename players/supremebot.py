from tkinter.tix import InputOnly
from player import Player
from players.human import Human

import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self, num_layers, layers_size):
        super(Net, self).__init__()
        self.hidden_layers = nn.ModuleList([nn.Linear(4, layers_size)])
        self.hidden_layers.extend([nn.Linear(layers_size, layers_size) for i in range(1, num_layers-1)])
        self.output = nn.Linear(layers_size, 6)
        self.activation = nn.ReLU()
        
    def forward(self, x):
        z = x
        for layer in self.hidden_layers:
            z = self.activation(layer(z))
        return self.output(z)

# Child class of player.py
# Uses machine learning models to predict other players' rolls from their claims
class SupremeBot(Player):
    def __init__(self):
        self.nets = {
            "Agg-High": Net(2, 16),
            "Agg-Low": Net(2, 16),
            "Cond-High": Net(4, 16),
            "Cond-Low": Net(4, 16),
            "Conserv": Net(2, 16),
        }

        # Load weights for each model (trained in training folder)
        self.nets["Agg-High"].load_state_dict(torch.load("/Users/michaelhein/Programs/Dicebot/models/aggressive_high_lvl_stat.obj")),
        self.nets["Agg-Low"].load_state_dict(torch.load("/Users/michaelhein/Programs/Dicebot/models/aggressive_low_lvl_stat.obj")),
        self.nets["Cond-High"].load_state_dict(torch.load("/Users/michaelhein/Programs/Dicebot/models/conditional_high_lvl_stat.obj")),
        self.nets["Cond-Low"].load_state_dict(torch.load("/Users/michaelhein/Programs/Dicebot/models/conditional_low_lvl_stat.obj")),
        self.nets["Conserv"].load_state_dict(torch.load("/Users/michaelhein/Programs/Dicebot/models/conservative_stat.obj"))
    
    # Asks human to returns 1 to indicate bluff call, or 0 to indicate no bluff call
    def getBluff(
        self, 
        prevMoves: list[tuple[tuple[Player, str], int, int]],
        currentPlayer: str,
        currentRoll: dict,
        verbose: bool,
        totalDice: int,
        numOwnDice: int
    ) -> int:

        return Human().getBluff(
            prevMoves,
            currentPlayer,
            currentRoll,
            verbose,
            totalDice,
            numOwnDice
        )



    # Asks human for move and provides prediction of previous player's roll
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
        if len(prevMoves) > 0:
            previousMove = prevMoves[-1]

            inputTensor = torch.tensor([
                totalDice,
                updatedPlayerTracker[previousMove[0][1]],
                previousMove[1],
                previousMove[2]
            ]).float()

            print(inputTensor)
            
            outputTensor = self.nets[previousMove[0][1]].forward(inputTensor)
            print(f"""
====================================================================================
SUPREME BOT THINKS:
Player: {previousMove[0][1]},
Input Tensor: {inputTensor},
Output Tensor: {outputTensor}
====================================================================================
    """)

        return Human().getMove(
            prevMoves,
            currentPlayer,
            currentRoll,
            verbose,
            totalDice,
            numOwnDice,
            numPlayers,
            updatedPlayerTracker
        )
