import ai
import constants
from tetris import Game, GameBoard, Moves

pass_though_moves = [Moves.QUIT, Moves.SOFT_DROP]

class AiTrainGame(Game):
    def __init__(self, board: GameBoard) -> None:
        super().__init__(board, -1)
        
 
    def display(self, frame: int, game: GameBoard) -> None: return
    
    def get_moves(self, frame: int, game: GameBoard) -> list[Moves]:
        return ai.outputs_to_moves(
            ai.network.compute(
                ai.game_to_inputs(self)
            )
        )
         
def main() -> None:
    
    try:
        ai.network.load("ml_projects/tetris/tetris-network")
    except FileNotFoundError:
        print("Starting new training run")
    else:
        print("Starting from existing training run")
        
    board = GameBoard(constants.BOARD_WIDTH, constants.BOARD_HEIGHT)
    game = AiTrainGame(board)
    
    ai.network.dump("ml_projects/tetris/tetris-network")

if __name__ == "__main__":
    main()