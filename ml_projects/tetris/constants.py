from tetris import Move

BOARD_WIDTH, BOARD_HEIGHT = 10, 20
SHAPE_QUEUE_SIZE = 3

AGENT_NAME = "tetris-ai"

POTENTIAL_MOVES: list[Move] = [
    None, Move.SPIN, Move.RIGHT, Move.LEFT, 
]