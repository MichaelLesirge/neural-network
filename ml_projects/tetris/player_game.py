import pygame
from tetris import Tetris, Move, Render
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
SIDE_BAR_WIDTH = TETRIS_SQUARE_SIZE * 7

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
    
    # pygame.key.set_repeat(170, 50)
    
    board = Tetris(
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
            state, reward, done, info = board.step(moves)
                
        if done: going = False
        
        board_surface = board.render_as_pygame(
            block_size=TETRIS_SQUARE_SIZE,
            
            background_color=BACKGROUND_COLOR,
            line_color=SECONDARY_COLOR,
            
            ghost_block=SHOW_GHOST_PEACES
        )
        
        blit_with_outline(screen, board_surface, (GAME_X, GAME_Y))
        
        display_info = ["score", "level", "lines"]
        left_side_bar = render_info_panel(
            {key.upper(): font.render(str(info[key]), True, MAIN_COLOR) for key in display_info},
            font=font, width=SIDE_BAR_WIDTH, margin=5, section_margin=2
        )
        
        blit_with_outline(screen, left_side_bar, (GAME_X - SIDE_BAR_WIDTH - SIDE_BAR_GAP, GAME_Y))
            
        if paused: screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
                    
        pygame.display.flip()

        clock.tick(FPS)
        
    pygame.quit()

def render_section(title: str, content: pygame.Surface, font: pygame.font.Font, width: int, margin: int) -> pygame.Surface:
    title_render = font.render(title, True, MAIN_COLOR)
    
    title_area_height = margin + title_render.get_height() + margin
    content_area_height = margin + content.get_height() + margin
    
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
    
def render_info_panel(data: dict[str, pygame.Surface], font: pygame.font.Font, width: int, margin: int, section_margin: int, height = None):
    panel = pygame.Surface((
        width,
        margin + sum(
            section_margin + font.get_height() + section_margin +
            section_margin + section.get_height() + section_margin +
            margin
            for section in data.values()) + margin
    ))
        
    panel.fill(SECONDARY_COLOR)
    
    section_y = margin
    section_width = width - margin * 2
    
    for i, (title, content) in enumerate(data.items()):
        section = render_section(title, content, font, section_width, section_margin)
        
        panel.blit(section, (margin, section_y))
        section_y += section.get_height() + margin
        
    return panel
            

if __name__ == "__main__":
    main()