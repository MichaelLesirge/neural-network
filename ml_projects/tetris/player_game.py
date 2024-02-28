import json, time, pathlib

import pygame
import numpy as np

from tetris import Tetris, Move, TetrominoShape
import constants
from dqn_agent import DQNAgent

# Game Size
BOARD_SQUARES_ACROSS = constants.BOARD_WIDTH
BOARD_SQUARES_DOWN = constants.BOARD_HEIGHT

# Window sizes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = SCREEN_WIDTH / 1.618

TETRIS_SQUARE_SIZE = 25

GAME_WIDTH, GAME_HEIGHT = BOARD_SQUARES_ACROSS * TETRIS_SQUARE_SIZE, BOARD_SQUARES_DOWN * TETRIS_SQUARE_SIZE
GAME_X, GAME_Y = (SCREEN_WIDTH // 2 - GAME_WIDTH // 2, SCREEN_HEIGHT // 2 - GAME_HEIGHT // 2)


SIDE_PANEL_GAP = TETRIS_SQUARE_SIZE
SIDE_PANEL_WIDTH = TETRIS_SQUARE_SIZE * 7

SIDE_LEFT_X = GAME_X - SIDE_PANEL_WIDTH - SIDE_PANEL_GAP
SIDE_RIGHT_X = GAME_X + GAME_WIDTH + SIDE_PANEL_GAP

SIDE_PANEL_MARGIN = TETRIS_SQUARE_SIZE

OUTLINE_WIDTH = 3

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

# Path
PATH = pathlib.Path(__file__).parent
MEDIA_PATH = PATH / "assets"

SHAPE_IMAGES: dict[TetrominoShape, pygame.Surface] = {
    shape: pygame.image.load(MEDIA_PATH / "normal-tetromino" / f"{shape.get_name()}.png") for shape in TetrominoShape.ALL_SHAPES
}
SHAPE_GHOST_IMAGES: dict[TetrominoShape, pygame.Surface] = {
    shape: pygame.image.load(MEDIA_PATH / "ghost-tetromino" / f"{shape.get_name()}.png") for shape in TetrominoShape.ALL_SHAPES
}

HIGH_SCORE_STORAGE_PATH = PATH / "highScore.json"

BLANK_SURFACE = pygame.Surface((0, 0))

# Game rules
PIECE_QUEUE_SIZE = 3
SHOW_GHOST_PEACES = True

def blit_with_outline(screen: pygame.Surface, source: pygame.Surface, dest: tuple[int, int]) -> None:
    line_width = OUTLINE_WIDTH
    outline_color = MAIN_COLOR
    x, y = dest
    width, height = source.get_width(), source.get_height()

    pygame.draw.rect(screen, outline_color, pygame.Rect(x - line_width, y - line_width, width + line_width * 2, height + line_width * 2), width = line_width)  
    screen.blit(source, dest)

def main() -> None:
    
    pygame.init()
    pygame.mixer.init()
     
    pygame.mixer.music.load(MEDIA_PATH / "tetris.mp3") 
    pygame.mixer.music.play(-1, 0, 1000 * 10)

    game = Tetris(
        width=BOARD_SQUARES_ACROSS, height=BOARD_SQUARES_DOWN, shape_queue_size=constants.SHAPE_QUEUE_SIZE,
        FPS=FPS,
        enable_wall_kick=True, enable_hold=True
    )
    
    try: 
        agent = DQNAgent(constants.AGENT_NAME, game.state_as_array().size, epsilon=0)
    except FileNotFoundError:
        agent = None

    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
        
    button_size = TETRIS_SQUARE_SIZE * 2
    
    pause_button = ToggleButton(screen, (262 - button_size / 2 - 5, 483),
                                pygame.image.load(MEDIA_PATH / "play.png"),
                                pygame.image.load(MEDIA_PATH / "pause.png"),
                                button_size)

    mute_button = ToggleButton(screen, (262 + button_size / 2 + 5, 483),
                                pygame.image.load(MEDIA_PATH / "play_sound.png"),
                                pygame.image.load(MEDIA_PATH / "mute_sound.png"),
                                button_size)
        
    clock = pygame.time.Clock()
        
    title_font = pygame.font.SysFont("Monospace", 50, True, False)
    paused_text = title_font.render("PAUSED", True, MAIN_COLOR)
    
    font = pygame.font.SysFont("Berlin Sans FB", 22, False, False)
        
    pressing_down_arrow = False
    left_down_clock = right_down_clock = None
    
    has_quit_game = False
    game_going = True
    
    used_ai_control = using_ai_control = False
        
    while game_going and (not has_quit_game):
        fps = FPS
                
        screen.fill(BACKGROUND_COLOR)
        
        prefix = ("(AI)" if using_ai_control else "")
        title = title_font.render(WINDOW_NAME + prefix, True, MAIN_COLOR) 
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 0))
         
        moves = []
        
        left_click = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           has_quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:         game_going = False
                if event.key == pygame.K_UP:        moves.append(Move.SPIN)
                if event.key == pygame.K_SPACE:     moves.append(Move.HARD_DROP)
                if event.key == pygame.K_c:         moves.append(Move.HOLD)
                if event.key == pygame.K_p:    pause_button.toggle_state()
                if event.key == pygame.K_m:         mute_button.toggle_state()
                if event.key == pygame.K_a:         using_ai_control = not using_ai_control
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                left_click = True 
                
        mouse_pos = pygame.mouse.get_pos()
        for button in ToggleButton.all_buttons:
            button.update(mouse_pos, mouse_down = left_click)
        
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
        
        if using_ai_control:
            
            if Move.SOFT_DROP in moves: fps *= 20
            
            moves.clear()
            
            used_ai_control = True
            
            if agent is not None:
                next_states = game.get_next_states()
                
                best_action = agent.take_action(next_states)
                
                moves.append(best_action)

        
        if (not pause_button.get_state()) or (game.frame < 1):    
            state, reward, done, info = game.step(moves)
                
        if done: game_going = False
         
        should_pause = (pause_button.get_state() or mute_button.get_state())
        is_playing = pygame.mixer.music.get_busy()
        if should_pause and is_playing: pygame.mixer.music.pause()
        if not (should_pause or is_playing): pygame.mixer.music.unpause()
        
        tetris_board_surface = render_game(
            game,
            block_size=TETRIS_SQUARE_SIZE,
            ghost_block=SHOW_GHOST_PEACES
        )
        
        blit_with_outline(screen, tetris_board_surface, (GAME_X, GAME_Y))
                 
        minutes, seconds = divmod(info["frame"] / FPS, 60)
        
        display_info = {
            **info,
            "fps": round(clock.get_fps(), 3),
            "time": f"{minutes:.0f}:{seconds:0>2.0f}",
            "reward": round(reward, 3),
            "ai_reward": round(agent.predict_value(state)[0], 3) if agent else None,
        }
        
        info_side_panel = render_info_panel(
            {key: display_info[key] for key in ["score", "level", "lines", "time"]},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_PANEL_MARGIN
        )
        
        blit_with_outline(screen, info_side_panel, (SIDE_LEFT_X, GAME_Y))
        
        ai_info_side_panel = render_info_panel(
            {key: display_info[key] for key in ["reward", "ai_reward"]},
            font=font, width=SIDE_PANEL_WIDTH - (SIDE_PANEL_MARGIN * 2), margin=(0, SIDE_PANEL_MARGIN)
        )
        if used_ai_control: blit_with_outline(screen, ai_info_side_panel, (SIDE_LEFT_X - SIDE_PANEL_WIDTH + SIDE_PANEL_MARGIN, GAME_Y))

        next_side_panel = render_info_panel(
            {"next": render_shapes(info["piece_queue"], TETRIS_SQUARE_SIZE)},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_PANEL_MARGIN
        )

        blit_with_outline(screen, next_side_panel, (SIDE_RIGHT_X, GAME_Y))
        
        held_side_bar = render_info_panel(
            {"held": render_shapes([info["held"]], TETRIS_SQUARE_SIZE)},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_PANEL_MARGIN
        )
        
        blit_with_outline(screen, held_side_bar, (SIDE_RIGHT_X, GAME_Y + GAME_HEIGHT - held_side_bar.get_height()))
        
        control_side_bar = render_info_panel(
            {"control": render_shapes([None], TETRIS_SQUARE_SIZE)},
            font=font, width=SIDE_PANEL_WIDTH, margin=SIDE_PANEL_MARGIN
        )
        blit_with_outline(screen, control_side_bar, (SIDE_LEFT_X, GAME_Y + GAME_HEIGHT - control_side_bar.get_height()))
        pause_button.draw()
        mute_button.draw()
             
        if pause_button.get_state(): screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
                    
        pygame.display.flip()

        clock.tick(fps)
    
    if not has_quit_game:
        waiting_for_key = True
        
        try:
            with open(MEDIA_PATH.parent / HIGH_SCORE_STORAGE_PATH, "r") as file:
                high_score = json.load(file)
        except FileNotFoundError:
            high_score = {}
        
        if info["score"] > high_score.get("score", 0):
            high_score["score"] = info["score"]
            high_score["ai"] = used_ai_control
            high_score["ctime"] = time.ctime()
            high_score["time"] = time.time()
            
            with open(MEDIA_PATH.parent / HIGH_SCORE_STORAGE_PATH, "w") as file:
                json.dump(high_score, file)
            

        game_over_bar = render_info_panel(
            {"Game Over": BLANK_SURFACE, "score": info["score"], "best": high_score["score"], "Again?": "Space Key"},
            font=font, width=(8 * TETRIS_SQUARE_SIZE), margin=SIDE_PANEL_MARGIN
        )
        
        frame = 0
        wait_seconds = 1
        draw_on_frame = (FPS * wait_seconds)
        
        pygame.mixer.music.fadeout(wait_seconds * 1000)
         
        while waiting_for_key and (not has_quit_game):
            frame += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: has_quit_game = True
                elif frame > draw_on_frame and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: waiting_for_key = False
            if frame > draw_on_frame:
                blit_with_outline(screen, game_over_bar, (GAME_X + GAME_WIDTH // 2 - game_over_bar.get_width() // 2, GAME_Y + GAME_HEIGHT // 2 - game_over_bar.get_height() // 2))
                pygame.display.flip()
            clock.tick(FPS)

    if has_quit_game: pygame.quit()
    else: main()
    

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
    if shape is None: return BLANK_SURFACE 
    
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
    
def render_info_panel(data: dict[str, pygame.Surface], font: pygame.font.Font, width: int, margin: int | tuple[int, int]):
    data = {key.upper().replace("_", " "): (value if isinstance(value, pygame.Surface) else font.render(str(value), True, MAIN_COLOR)) for key, value in data.items()}
        
    try: x_margin, y_margin = margin
    except TypeError: x_margin = y_margin = margin
    
    height = y_margin + sum(font.get_height() + section.get_height() + y_margin for section in data.values())
    panel = pygame.Surface((width, height))
        
    panel.fill(SECONDARY_COLOR)
    
    section_y = y_margin
    section_width = width - x_margin * 2
    
    for title, content in data.items():
        section = render_section(title, content, font, section_width)
        panel.blit(section, (x_margin, section_y))
        section_y += section.get_height() + y_margin
        
    return panel

class ToggleButton:
    all_buttons: list["ToggleButton"] = []
    
    def __init__(self, screen: pygame.Surface, position: tuple[int, int], enable: pygame.Surface, disable: pygame.Surface, size: int) -> None:
        self.x, self.y = position
        self.size = size
        
        self.radius_squared = (self.size / 2) ** 2
                
        self.screen = screen
        
        self.enable = pygame.transform.scale(enable, (self.size, self.size))
        self.disable = pygame.transform.scale(disable, (self.size, self.size))
        
        self.state = self.is_clicked = self.is_hovered = False
        
        ToggleButton.all_buttons.append(self)
    
    def is_over(self, pos: tuple[int, int]) -> bool:
        return pygame.Vector2(pos).distance_squared_to((self.x, self.y)) <= self.radius_squared
                
    def update(self, mouse_pos: tuple[int, int], mouse_down: bool = False) -> None:
        
        self.is_hovered = self.is_over(mouse_pos)
        self.is_clicked = self.is_hovered and mouse_down
         
        if self.is_clicked: self.toggle_state()
        
    def draw(self) -> None:
        image = self.enable if self.state else self.disable

        image = pygame.transform.scale_by(image, 1 + (-0.2 if self.is_clicked else 0) + (0.1 if self.is_hovered else 0))
        
        self.screen.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))
        # blit_with_outline(self.screen, image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))
        # pygame.draw.circle(self.screen, "red", (self.x, self.y), 10)
    
    def toggle_state(self) -> None:
        self.state = not self.state
        
    def get_state(self) -> bool: return self.state

if __name__ == "__main__":
    print("""\033[32m
[][][][][] [][][][] [][][][][] [][][][]  [][][]   [][][]  
    []     []           []     []     []   []   []      [] 
    []     []           []     []     []   []   []       
    []     [][][]       []     [][][][]    []     [][][]  
    []     []           []     []   []     []           [] 
    []     []           []     []    []    []   []      [] 
    []     [][][][]     []     []     [] [][][]   [][][]          
          \033[0m""")
    
    print(f"\033[1m{'Button':<12} Action\033[0m")
    for key, control in {
        "up arrow": "rotate",
        "left arrow": "left",
        "right arrow": "right",
        "down arrow": "soft drop",
        "space": "hard drop",
        "c": "hold",
        "esc": "quit",
        "p": "pause",
        "m": "mute",
        "a": "enable ai",
    }.items():
        print(f"{key.title():<12} {control.upper()}\033[0m")
    
    main()