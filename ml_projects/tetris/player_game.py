import pygame
from tetris import Tetris, Move, Render
import constants

MAIN_COLOR = "white"
BACKGROUND_COLOR = "black"
SECONDARY_COLOR = (50, 50, 50)

BOARD_SQUARES_ACROSS = constants.BOARD_WIDTH
BOARD_SQUARES_DOWN = constants.BOARD_HEIGHT

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = SCREEN_WIDTH / 1.618

WINDOW_NAME = "Tetris"

FONT = "Arial"

FPS = 30

BLOCK_SIZE = 25

PIECE_QUEUE_SIZE = 3

def draw_outline(screen: pygame.surface, top_left: tuple[int, int], width_height: tuple[int, int]) -> None:
    line_width = 5
    outline_color = SECONDARY_COLOR
    
    x, y = top_left
    width, height = width_height

    pygame.draw.rect(screen, outline_color, pygame.Rect(x - line_width, y - line_width, width + line_width * 2, height + line_width * 2), width = line_width, border_radius=-1)
    
    
def main() -> None:
    pygame.init()
    
    pygame.key.set_repeat(170, 50)
    
    board = Tetris(
        width=BOARD_SQUARES_ACROSS, height=BOARD_SQUARES_DOWN, FPS=FPS,
        enable_wall_kick=True, piece_queue_size=PIECE_QUEUE_SIZE
    )
    
    board_surface = board.render_as_pygame(BLOCK_SIZE, blank_surface=True)
    
    game_position = (SCREEN_WIDTH // 2 - board_surface.get_width() // 2, SCREEN_HEIGHT // 2 - board_surface.get_height() // 2)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    
    clock = pygame.time.Clock()
        
    pressing_down = False
    
    going = True
    
    while going:
        
        screen.fill(BACKGROUND_COLOR)
        
        moves = []
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           moves = [Move.QUIT]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    moves.append(Move.QUIT)
                if event.key == pygame.K_UP:        moves.append(Move.SPIN)
                if event.key == pygame.K_LEFT:      moves.append(Move.LEFT)
                if event.key == pygame.K_RIGHT:     moves.append(Move.RIGHT)
                if event.key == pygame.K_SPACE:     moves.append(Move.HARD_DROP)
                if event.key == pygame.K_DOWN:      pressing_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:      pressing_down = False
        
        if pressing_down: moves.append(Move.SOFT_DROP)   
        
        state, reward, done, info = board.step(moves)
        
        if done: going = False
        
        board_surface = board.render_as_pygame(
            block_size=BLOCK_SIZE,
            
            background_color=BACKGROUND_COLOR,
            line_color=SECONDARY_COLOR,
            
            block_images=True,
            ghost_block=True
        )
        
        screen.blit(board_surface, game_position)
        draw_outline(screen, game_position, (board_surface.get_width(), board_surface.get_height()))
            
        pygame.display.flip()

        clock.tick(FPS)


    pygame.quit()
        
if __name__ == "__main__":
    main()