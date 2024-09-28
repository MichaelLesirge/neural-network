import numpy as np

from game_actions import Action
from game_state import State

from .model import Model

from .tetris import (
    TetrisGameManager,
    Grid,
    ShuffledBagQueue,
    TetrominoShape,
    LevelManager,
    ScoreManger,
    TimeManager,
    Event,
)


class BasicModel(Model):

    def __init__(self) -> None:
        NULL_VALUE = 0

        board = Grid.empty(shape=(10, 20), null_value=NULL_VALUE)

        tetromino_shapes = [
            TetrominoShape(
                "I",
                [
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                ],
                null_value=NULL_VALUE
            ),
            TetrominoShape(
                "O",
                [
                    [1, 1],
                    [1, 1],
                ],
                null_value=NULL_VALUE
            ),
            TetrominoShape(
                "L",
                [
                    [0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0],
                ],
                null_value=NULL_VALUE
            ),
            TetrominoShape(
                "J",
                [
                    [1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0],
                ],
                null_value=NULL_VALUE
            ),
            TetrominoShape(
                "T",
                [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0],
                ],
                null_value=NULL_VALUE
            ),
            TetrominoShape(
                "Z",
                [
                    [1, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0],
                ],
                null_value=NULL_VALUE
            ),
            TetrominoShape(
                "S",
                [
                    [0, 1, 1],
                    [1, 1, 0],
                    [0, 0, 0],
                ],
                null_value=NULL_VALUE
            ),
        ]

        piece_queue = ShuffledBagQueue(tetromino_shapes, visible_size=3)

        level_manager = LevelManager(
            lines_for_next_level=10,
        )

        score_manager = ScoreManger(
            for_line_clear=[0, 40, 100, 300, 1200],
            for_events={Event.SOFT_DROP: 1, Event.HARD_DROP: 2}
        )

        time_manager = TimeManager(
            fps=60
        )

        self.game_manager = TetrisGameManager(board, piece_queue)

    def reset(self) -> None:
        self.game_manager.reset()

    def update(self, actions: list[Action]) -> State:
        self.game_manager.step(actions)

        return State(
            self.game_manager.get_board(),
            self.game_manager.get_current_piece_board(),
            self.game_manager.get_piece_percent_placed(),
            self.game_manager.get_ghost_board(),
            self.game_manager.get_held_tetromino(),
            self.game_manager.can_use_held_tetromino(),
            self.game_manager.get_tetromino_queue(),
            {},
            False,
            self.game_manager.get_array_null_value())
