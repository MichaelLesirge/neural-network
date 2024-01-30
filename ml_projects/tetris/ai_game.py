import pygame

import player_game
from tetris import Game, GameBoard, Moves
import constants

pass_though_moves = [Moves.QUIT, Moves.SOFT_DROP]

class Game(player_game.PlayerGame):
    def get_moves(self, frame: int, game: GameBoard) -> list[Moves]:
        player_moves = [move for move in super().get_moves(frame, game) if move in pass_though_moves]
        
        # Fake ai
        moves = []
        if frame % 100 == 0: moves.append(Moves.LEFT)
        if frame % 200 == 0: moves.append(Moves.RIGHT)
        if frame % 150 == 0: moves.append(Moves.SPIN)
        
        return moves + player_moves
         
def main() -> None:
    pygame.init()
    
    board = GameBoard(constants.BOARD_WIDTH, constants.BOARD_HEIGHT)
    game = Game(board)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()