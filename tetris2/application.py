import time
import pathlib
from enum import Enum, auto 

import pygame

from game_state import State

from display import PygameDisplay, ConsoleDisplay, Color
from player import PygamePlayer, AlgorithmPlayer
from model import (
    TetrisGameManager,
    Grid,
    ShuffledBagQueue,
    TetrominoShape,
    LevelManager,
    ScoreManger,
    TimeManager,
    Event,
    JSONFileHighScoreStorage,
    Score,
)

class PlayerType(Enum):
    HUMAN = auto()
    ALGORITHM = auto()

player_type = PlayerType.ALGORITHM

NULL_VALUE = 0

BOARD_SHAPE = (10, 20)

ITEMS_IN_QUEUE = 3

board = Grid.empty(shape=BOARD_SHAPE, null_value=NULL_VALUE)

tetromino_shapes = [
    TetrominoShape(
        "I", Color.CYAN,
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "O", Color.YELLOW,
        [
            [1, 1],
            [1, 1],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "L", Color.ORANGE,
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "J", Color.BLUE,
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "T", Color.PURPLE,
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "Z", Color.RED,
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
    TetrominoShape(
        "S", Color.GREEN,
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
        null_value=NULL_VALUE,
    ),
]

piece_queue = ShuffledBagQueue(tetromino_shapes, visible_size=ITEMS_IN_QUEUE)

level_manager = LevelManager(
    lines_for_next_level=10,
)

score_manager = ScoreManger(
    for_line_clear=[0, 100, 300, 500, 800],
    for_events={Event.SOFT_DROP: 1, Event.HARD_DROP: 2},
)

time_manager = TimeManager(fps=60)

wall_kick_positions = [
    (0, 0),
    (1, 0),
    (-1, 0),
]

game_manager = TetrisGameManager(
    board, piece_queue, level_manager, score_manager, time_manager, wall_kick_positions
)

if player_type == PlayerType.HUMAN:
    player = PygamePlayer(PygamePlayer.DEFAULT_BINDINGS)
elif player_type == PlayerType.ALGORITHM:
    player = AlgorithmPlayer(tetromino_shapes, NULL_VALUE)

display = PygameDisplay({hash(shape): shape.get_color() for shape in tetromino_shapes})
display.add_pause_button_action(game_manager.pause, game_manager.unpause)
display.add_restart_button_action(game_manager.reset)

clock = pygame.time.Clock()

high_score_manager = JSONFileHighScoreStorage(
    pathlib.Path(__file__).parent / "high_scores.json"
)

was_game_over = False

while True:

    sidebar_info = game_manager.get_sidebar_info()

    game_state = State(
        game_manager.get_board(),
        game_manager.get_current_piece_board(),
        game_manager.get_piece_percent_placed(),
        game_manager.get_ghost_board(),
        game_manager.get_held_tetromino(),
        game_manager.get_can_use_held_tetromino(),
        game_manager.get_tetromino_queue(),
        sidebar_info,
        {**sidebar_info, "high_score": (0 if high_score_manager.get_top_score() is None else high_score_manager.get_top_score().score)},
        game_manager.is_game_over(),
        game_manager.is_game_paused(),
        game_manager.get_array_null_value(),
    )

    if game_manager.is_game_over() and not was_game_over:
        high_score_manager.save_score(
            Score(int(game_state.info.get("score", 0)), time.ctime(), player.get_name())
        )
    was_game_over = game_manager.is_game_over()

    display.update(game_state)

    actions = []
    if isinstance(player, PygamePlayer):
        actions.extend(
            player.get_actions(
                pygame.event.get(pygame.KEYDOWN) + pygame.event.get(pygame.KEYUP)
            )
        )

    if isinstance(player, AlgorithmPlayer):
        actions.extend(
            player.get_actions(game_state)
        )

    game_manager.step(actions)

    if pygame.event.get(pygame.QUIT):
        break

    clock.tick(time_manager.get_fps())
