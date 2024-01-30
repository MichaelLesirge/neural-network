import pygame

import constants
from tetris import Game, GameBoard, Moves

pass_though_moves = [Moves.QUIT, Moves.SOFT_DROP]

class AiTrainGame(Game):
    def __init__(self, board: GameBoard) -> None:
        super().__init__(board, -1)
        
 
    def display(self, frame: int, game: GameBoard) -> None: return
    
    def get_moves(self, frame: int, game: GameBoard) -> list[Moves]:
        pass
         
def main() -> None:
    pygame.init()
    
    board = GameBoard(constants.BOARD_WIDTH, constants.BOARD_HEIGHT)
    game = Game(board)
    game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()