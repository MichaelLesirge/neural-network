from player import Player
from ui import Display
from presenter import Presenter

from game_actions import Action

class View:
    def __init__(self, player: Player, display: Display) -> None:
        self.player = player
        self.display = display
    
    def init_display(self, presenter: Presenter) -> None:
        self.display.bind_buttons(presenter)

    def update_display(self) -> None:
            
    
    def get_actions(self) -> list[Action]:
        return self.player.get_actions() + self.display.get_actions()