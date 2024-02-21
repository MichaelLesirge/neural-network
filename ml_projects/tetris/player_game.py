import pygame
from tetris import Tetris, Move, Render
import constants

MAIN_COLOR = "white"
BACKGROUND_COLOR = "black"
LINE_COLOR = (50, 50, 50)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = SCREEN_WIDTH / 1.618

WINDOW_NAME = "Tetris"

FONT = "Arial"

FPS = 30

DROP_DELAY_FRAMES = FPS // 3
SOFT_DROP_DELAY_FRAMES = FPS // 30

BLOCK_SIZE = 25
    
def main() -> None:
    pygame.init()
    
    pygame.key.set_repeat(170, 50)
    
    board = Tetris(
        width=constants.BOARD_WIDTH, height=constants.BOARD_HEIGHT,
        drop_delay_frames=DROP_DELAY_FRAMES, soft_drop_delay_frames=SOFT_DROP_DELAY_FRAMES,
        enable_wall_kick=True, enable_start_at_top=True
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
            line_color=LINE_COLOR,
            outline_color=MAIN_COLOR,
            
            block_images=True,
            ghost_block=True
        )
        
        screen.blit(board_surface, game_position)

        # print(board.render_as_str(full_block=True))
        
        text = pygame.font.SysFont(FONT, 25, True, False).render(f"Score: {info['score']}", True, MAIN_COLOR)
        screen.blit(text, [5, 5])
            
        pygame.display.flip()

        clock.tick(FPS)


    pygame.quit()
        
if __name__ == "__main__":
    main()