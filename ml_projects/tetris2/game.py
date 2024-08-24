from tetris import TetrisGameManager
from player import Player

# TetrisGameManager: Model
# Player: View 
# Game: Presenter

class Game:
    def __init__(self, tetris: TetrisGameManager, player: Player) -> None:
        self.tetris = tetris
        self.player = player

    def run(self) -> None:
        while True:
            actions = self.player.get_actions()
            self.tetris.step(actions)
            