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
        ai.network.load_params("ml_projects/tetris/tetris-network")
    except FileNotFoundError:
        print("Starting new training run")
    else:
        print("Starting from existing training run")
    
    print()
    
    training_rounds = 100_000
    children = 100
    keep_top = 10
    
    board = GameBoard(constants.BOARD_WIDTH, constants.BOARD_HEIGHT)
    game = AiTrainGame(board)
    
    top: dict[bytes: int] = {ai.network.get_params(): 0}
    
    try:
        for round in range(training_rounds):
            for network_param in list(top.keys()):
                for i in range(children):
                    
                    ai.network.set_params(network_param)
                    [layer.rand_shift() for layer in ai.network.layers if isinstance(layer, ai.nn.layers.Dense)]
                    
                    score = game.run()
                    
                    if len(top) < keep_top:
                        top[ai.network.get_params()] = score
                    
                    if score >= min(top.values()):
                        del top[min(top, key=top.__getitem__)]
                        top[ai.network.get_params()] = score
                    
                    game.reset()      
        
            print(f"Round #{round + 1}. Top scores: {sorted(top.values(), reverse = True)}")
            
    except KeyboardInterrupt:
        print("Quitting...")
    
    best_network = max(top, key=top.__getitem__)
    ai.network.set_params(best_network)  
    ai.network.save_params("ml_projects/tetris/tetris-network")

    print(f"Network with score of {top[best_network]} saved.")

if __name__ == "__main__":
    main()