import pygame

import constants
import player_game
from tetris import Game, GameBoard, Moves

import ai

PASS_THOUGH_MOVES = [Moves.QUIT, Moves.SOFT_DROP]

class Game(player_game.PlayerGame):
    def get_moves(self, frame: int, game: GameBoard) -> list[Moves]:
        player_moves = [move for move in super().get_moves(frame, game) if move in PASS_THOUGH_MOVES]
        
        moves = ai.outputs_to_moves(
            ai.network.compute(
                ai.game_to_inputs(self)
            )
        )
        
        return moves + player_moves
         
def main() -> None:
    pygame.init()
    
    board = GameBoard(constants.BOARD_WIDTH, constants.BOARD_HEIGHT)
    game = Game(board)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()