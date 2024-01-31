import enum
import abc

from .game_board import GameBoard

class Moves(enum.Enum):
    SPIN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    SOFT_DROP = enum.auto()
    HARD_DROP = enum.auto()
    
    QUIT = enum.auto()

class Game(abc.ABC):
    def __init__(self, board: GameBoard, drop_delay: int = -1) -> None:
        self._board = board
        self._drop_delay = drop_delay
            
    @abc.abstractmethod
    def display(self, frame: int, game: GameBoard) -> None: pass

    @abc.abstractmethod
    def get_moves(self, frame: int, game: GameBoard) -> list[Moves]: pass

    def on_drop(self, frame: int, game: GameBoard) -> None: pass
    
    def reset(self) -> None: 
        self._board.reset()
    
    def run(self) -> int:
        going = True
                
        frame = 0
 
        while going:
            
            frame += 1
             
            moves = self.get_moves(frame, self._board)
            
            if Moves.QUIT in moves:
                going = False
            
            soft_drop = False
            
            for move in moves:
                if move == Moves.SPIN:
                    self._board.rotate()
                if move == Moves.LEFT:
                    self._board.change_x(-1)
                if move == Moves.RIGHT:
                    self._board.change_x(1)
                if move == Moves.HARD_DROP:
                    self._board.hard_drop()
                if move == Moves.SOFT_DROP:
                    soft_drop = True
                                
            if (self._drop_delay < 1 or
                frame % self._drop_delay == 0 or (soft_drop)):
                self._board.soft_drop()
                self.on_drop(frame, self._board)
                
            if self._board.done:
                going = False
                        
            self.display(frame, self._board)

        return self._board.score