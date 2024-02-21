import pygame
from tetris import Tetris, Move, Render
import constants

# Game Size
BOARD_SQUARES_ACROSS = constants.BOARD_WIDTH
BOARD_SQUARES_DOWN = constants.BOARD_HEIGHT

# Window size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = SCREEN_WIDTH / 1.618

TETRIS_SQUARE_SIZE = 25

GAME_WIDTH, GAME_HEIGHT = BOARD_SQUARES_ACROSS * TETRIS_SQUARE_SIZE, BOARD_SQUARES_DOWN * TETRIS_SQUARE_SIZE
GAME_X, GAME_Y = (SCREEN_WIDTH // 2 - GAME_WIDTH // 2, SCREEN_HEIGHT // 2 - GAME_HEIGHT // 2)

SIDE_BAR_GAP = TETRIS_SQUARE_SIZE
SIDE_BAR_WIDTH = TETRIS_SQUARE_SIZE * 7

# Other Window Data
WINDOW_NAME = "Tetris"
FONT = "Monospace"

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

def draw_outline(screen: pygame.surface, cord: tuple[int, int], width_height: tuple[int, int], line_width = 3, outline_color = MAIN_COLOR) -> None:    
    x, y = cord
    width, height = width_height

    pygame.draw.rect(screen, outline_color, pygame.Rect(x - line_width, y - line_width, width + line_width * 2, height + line_width * 2), width = line_width)    

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
        
    title_font = pygame.font.SysFont(FONT, TETRIS_SQUARE_SIZE * 2, True, False)
    title = title_font.render(WINDOW_NAME, True, MAIN_COLOR)
    paused_text = title_font.render("PAUSED", True, MAIN_COLOR)
    
    font = pygame.font.SysFont(FONT, TETRIS_SQUARE_SIZE, False, False)
        
    pressing_down_arrow = False
    left_down_clock = right_down_clock = None
    
    going = True
    
    paused = False
    
    while going:
        
        screen.fill(BACKGROUND_COLOR)
        
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 0))
         
        moves = []
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           moves = [Move.QUIT]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    paused = not paused
                if event.key == pygame.K_q:         moves = [Move.QUIT]
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
                
        if done or (paused and Move.QUIT in moves): going = False
        
        board_surface = board.render_as_pygame(
            block_size=TETRIS_SQUARE_SIZE,
            
            background_color=BACKGROUND_COLOR,
            line_color=SECONDARY_COLOR,
            
            ghost_block=SHOW_GHOST_PEACES
        )
        
        screen.blit(board_surface, (GAME_X, GAME_Y))
        draw_outline(screen, (GAME_X, GAME_Y), (board_surface.get_width(), board_surface.get_height()))
        
        data = {"Score": info["score"], "Level": info["level"], "Lines": info["lines"]}
        for i, (name, value) in enumerate(data.items()):
            box_width = SIDE_BAR_WIDTH
            box_height = TETRIS_SQUARE_SIZE * 3
            box_x = GAME_X - SIDE_BAR_GAP - box_width
            box_y = GAME_Y + (box_height + SIDE_BAR_GAP) * i
            
            draw_outline(screen, (box_x, box_y), (box_width, box_height))
            
            text = font.render(f"{name}: {value}", True, MAIN_COLOR)
            
            text_x = box_x + box_width // 2 - text.get_width() // 2
            text_y = box_y + box_height // 2 - text.get_height() // 2
            
            screen.blit(text, (text_x, text_y))
        
        box_x = GAME_X + GAME_WIDTH + SIDE_BAR_GAP
        box_y = GAME_Y
        box_width = SIDE_BAR_WIDTH
        box_height = PIECE_QUEUE_SIZE * TETRIS_SQUARE_SIZE * 6
        draw_outline(screen, (box_x, box_y), (box_width, box_height))
        piece_queue = info["piece_queue"]
        for i, type in enumerate(piece_queue):
            
            type_image = pygame.Surface((type.get_width() * TETRIS_SQUARE_SIZE, type.get_height() * TETRIS_SQUARE_SIZE))

            def draw_tetromino_block(row: int, col: int):
                image = type.image
                if image.get_width() != TETRIS_SQUARE_SIZE: image = pygame.transform.scale(image, (TETRIS_SQUARE_SIZE, TETRIS_SQUARE_SIZE))
                type_image.blit(image, pygame.Rect(col * TETRIS_SQUARE_SIZE, row * TETRIS_SQUARE_SIZE, TETRIS_SQUARE_SIZE, TETRIS_SQUARE_SIZE))
                
            for row in range(type.get_height()):
                for col in range(type.get_width()):
                    if type.get_default_shape()[row][col]: draw_tetromino_block(row, col)
            
            
            type_image_x = box_x + box_width // 2 - type_image.get_width() // 2
            type_image_y = box_y + TETRIS_SQUARE_SIZE * 6 * i + TETRIS_SQUARE_SIZE
            
            screen.blit(type_image, (type_image_x, type_image_y))
            
        if paused: screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
                    
        pygame.display.flip()

        clock.tick(FPS)


    pygame.quit()
        
if __name__ == "__main__":
    main()