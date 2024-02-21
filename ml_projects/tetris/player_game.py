import pathlib

import pygame

from tetris import Tetris, Move, TetrominoShape
import constants

# Game Size
BOARD_SQUARES_ACROSS = constants.BOARD_WIDTH
BOARD_SQUARES_DOWN = constants.BOARD_HEIGHT

# Window sizes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = SCREEN_WIDTH / 1.618

TETRIS_SQUARE_SIZE = 25

GAME_WIDTH, GAME_HEIGHT = BOARD_SQUARES_ACROSS * TETRIS_SQUARE_SIZE, BOARD_SQUARES_DOWN * TETRIS_SQUARE_SIZE
GAME_X, GAME_Y = (SCREEN_WIDTH // 2 - GAME_WIDTH // 2, SCREEN_HEIGHT // 2 - GAME_HEIGHT // 2)

SIDE_BAR_GAP = TETRIS_SQUARE_SIZE
SIDE_PANEL_WIDTH = TETRIS_SQUARE_SIZE * 7

# Other Window Data
WINDOW_NAME = "Tetris"

# Window colors
MAIN_COLOR = "white"
BACKGROUND_COLOR = "black"
SECONDARY_COLOR = (50, 50, 50)

# Game speed
FPS = 30

KEY_REPEAT_DELAY = (170 / 1000) * FPS
KEY_REPEAT_INTERVAL = (50 / 1000) * FPS

# Images
PATH = pathlib.Path(__file__).parent

SHAPE_IMAGES: dict[TetrominoShape, pygame.Surface] = {
    shape: pygame.image.load(PATH / "normal-tetromino" / f"{shape.get_name()}.png") for shape in TetrominoShape.ALL_SHAPES
}
SHAPE_GHOST_IMAGES: dict[TetrominoShape, pygame.Surface] = {
    shape: pygame.image.load(PATH / "ghost-tetromino" / f"{shape.get_name()}.png") for shape in TetrominoShape.ALL_SHAPES
}

# Game rules
PIECE_QUEUE_SIZE = 3
SHOW_GHOST_PEACES = True

def blit_with_outline(screen: pygame.Surface, source: pygame.Surface, dest: tuple[int, int], line_width = 3, outline_color = MAIN_COLOR) -> None:    
    x, y = dest
    width, height = source.get_width(), source.get_height()

    pygame.draw.rect(screen, outline_color, pygame.Rect(x - line_width, y - line_width, width + line_width * 2, height + line_width * 2), width = line_width)  
    screen.blit(source, dest)

def main() -> None:
    pygame.init()
        
    game = Tetris(
        width=BOARD_SQUARES_ACROSS, height=BOARD_SQUARES_DOWN, FPS=FPS,
        enable_wall_kick=True, piece_queue_size=PIECE_QUEUE_SIZE
    )
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    
    clock = pygame.time.Clock()
        
    title_font = pygame.font.SysFont("Monospace", TETRIS_SQUARE_SIZE * 2, True, False)
    title = title_font.render(WINDOW_NAME, True, MAIN_COLOR)
    paused_text = title_font.render("PAUSED", True, MAIN_COLOR)
    
    font = pygame.font.SysFont("Berlin Sans FB", TETRIS_SQUARE_SIZE, False, False)
        
    pressing_down_arrow = False
    left_down_clock = right_down_clock = None
    
    going = True
    
    paused = False
    
    while going:
        
        screen.fill(BACKGROUND_COLOR)
        
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 0))
         
        moves = []
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           going = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    paused = not paused
                if event.key == pygame.K_q:         going = False
                if event.key == pygame.K_UP:        moves.append(Move.SPIN)
                if event.key == pygame.K_SPACE:     moves.append(Move.HARD_DROP)
                if event.key == pygame.K_c:         moves.append(Move.HOLD)
                if event.key == pygame.K_LEFT:
                    moves.append(Move.LEFT)
                    left_down_clock = KEY_REPEAT_DELAY
                if event.key == pygame.K_RIGHT:      
                    right_down_clock = KEY_REPEAT_DELAY
                    moves.append(Move.RIGHT)
                if event.key == pygame.K_DOWN:      pressing_down_arrow = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:      pressing_down_arrow = False
                if event.key == pygame.K_LEFT:      left_down_clock = None
                if event.key == pygame.K_RIGHT:     right_down_clock = None
        
        if left_down_clock is not None:
            left_down_clock -= 1
            if left_down_clock <= 0:
                moves.append(Move.LEFT)
                left_down_clock = KEY_REPEAT_INTERVAL

        if right_down_clock is not None:
            right_down_clock -= 1
            if right_down_clock <= 0:
                moves.append(Move.RIGHT)
                right_down_clock = KEY_REPEAT_INTERVAL
        
        if pressing_down_arrow: moves.append(Move.SOFT_DROP)   
        
        if not paused:
            state, reward, done, info = game.step(moves)
                
        if done: going = False
        
        tetris_board_surface = render_game(
            game,
            block_size=TETRIS_SQUARE_SIZE,
            ghost_block=SHOW_GHOST_PEACES
        )
        
        blit_with_outline(screen, tetris_board_surface, (GAME_X, GAME_Y))
        
        display_info = ["score", "level", "lines"]
        left_side_bar = render_info_panel(
            {key.upper(): font.render(str(info[key]), True, MAIN_COLOR) for key in display_info},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_BAR_GAP
        )
        
        blit_with_outline(screen, left_side_bar, (GAME_X - SIDE_PANEL_WIDTH - SIDE_BAR_GAP, GAME_Y))

        right_side_bar = render_info_panel(
            {"next".upper(): render_shapes(info["piece_queue"], TETRIS_SQUARE_SIZE)},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_BAR_GAP
        )

        blit_with_outline(screen, right_side_bar, (GAME_X + GAME_WIDTH + SIDE_BAR_GAP, GAME_Y))
        
        bottom_left_side_bar = render_info_panel(
            {"held".upper(): render_shapes([info["held"]], TETRIS_SQUARE_SIZE)},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_BAR_GAP
        )
        
        blit_with_outline(screen, bottom_left_side_bar, (GAME_X - SIDE_PANEL_WIDTH - SIDE_BAR_GAP, GAME_Y + GAME_HEIGHT - bottom_left_side_bar.get_height()))
        
            
        if paused: screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
                    
        pygame.display.flip()

        clock.tick(FPS)
        
    pygame.quit()

def draw_tetromino_block(screen: pygame.Surface, block_size: int, row: int, col: int, shape: TetrominoShape, ghost = False):
    image = (SHAPE_GHOST_IMAGES if ghost else SHAPE_IMAGES)[shape]
    if image.get_width() != block_size: image = pygame.transform.scale(image, (block_size, block_size))
    screen.blit(image, pygame.Rect(col * block_size, row * block_size, block_size, block_size))

def render_game(game: Tetris, block_size: int = 25, ghost_block = True) -> tuple[pygame.Surface, list[pygame.Surface]]:
    screen = pygame.Surface((game.width * block_size, game.height * block_size))
                        
    screen.fill(BACKGROUND_COLOR)
    
    for col in range(1, game.width):
        pygame.draw.line(screen, SECONDARY_COLOR, (block_size * col, 0), (block_size * col, block_size * game.height), width=1)

    for row in range(1, game.height):
        pygame.draw.line(screen, SECONDARY_COLOR, (0, block_size * row), (block_size * game.width, block_size * row), width=1)

    for value, (row, col) in game:
        if value: draw_tetromino_block(screen, block_size, row, col, TetrominoShape.SHAPE_ID_MAP[value])
            
    for value, (row, col) in game.current_tetromino:
        if value: draw_tetromino_block(screen, block_size, row, col, game.current_tetromino.shape)
        
    if ghost_block:   
        real_y = game.current_tetromino.y
        
        while not game.intersects():
            game.current_tetromino.y += 1
        game.current_tetromino.y -= 1
    
        for value, (row, col) in game.current_tetromino:
            if value: draw_tetromino_block(screen, block_size, row, col, game.current_tetromino.shape, ghost=True)
        
        game.current_tetromino.y = real_y
    
    return screen

def render_shape(shape: TetrominoShape, block_size: int) -> pygame.Surface:
    if shape is None: return pygame.Surface((0, 0))
    
    grid = shape.get_trimmed_grid()
    height, width = grid.shape
        
    shape_render = pygame.Surface((width * block_size, height * block_size))
    
    for row in range(height):
        for col in range(width):
            if grid[row, col]: draw_tetromino_block(shape_render, block_size, row, col, shape)
    
    return shape_render

_max_trimmed_height = max(shape.get_trimmed_grid().shape[0] for shape in TetrominoShape.ALL_SHAPES)
def render_shapes(shape_queue: list[TetrominoShape], block_size: int) -> pygame.Surface:
    rendered_shapes = [render_shape(shape, block_size) for shape in shape_queue]

    max_trimmed_height = _max_trimmed_height * block_size

    rendered_queue = pygame.Surface((
        max(shape.get_width() for shape in rendered_shapes),
        block_size + sum(max_trimmed_height + block_size for shape in rendered_shapes)
    ))
     
    y = block_size
    
    center_x = rendered_queue.get_width() // 2
    center_y = max_trimmed_height // 2
    
    for shape in rendered_shapes:
        rendered_queue.blit(shape, (center_x - shape.get_width() // 2, y + center_y - shape.get_height() // 2))
        y += max_trimmed_height + block_size
    
    return rendered_queue
    

def render_section(title: str, content: pygame.Surface, font: pygame.font.Font, width: int) -> pygame.Surface:
    title_render = font.render(title, True, MAIN_COLOR)
    
    title_area_height = title_render.get_height()
    content_area_height = content.get_height() 
    
    section = pygame.Surface((width, title_area_height + content_area_height))
    
    pygame.draw.rect(section, SECONDARY_COLOR, pygame.Rect((0, 0), (width, title_area_height)))
    pygame.draw.rect(section, BACKGROUND_COLOR, pygame.Rect((0, title_area_height), (width, content_area_height)))
    
    section.blit(title_render, (
        section.get_width() // 2 - title_render.get_width() // 2,
        title_area_height // 2 - title_render.get_height() // 2))
    
    section.blit(content, (
        section.get_width() // 2 - content.get_width() // 2,
        title_area_height + content_area_height // 2 - content.get_height() // 2))
    
    return section
    
def render_info_panel(data: dict[str, pygame.Surface], font: pygame.font.Font, width: int, margin: int):
    height = margin + sum(font.get_height() + section.get_height() + margin for section in data.values())
    panel = pygame.Surface((width, height))
        
    panel.fill(SECONDARY_COLOR)
    
    section_y = margin
    section_width = width - margin * 2
    
    for title, content in data.items():
        section = render_section(title, content, font, section_width)
        
        panel.blit(section, (margin, section_y))
        section_y += section.get_height() + margin
        
    return panel
            

if __name__ == "__main__":
    main()