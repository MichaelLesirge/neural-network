import pygame
from tetris import Tetris, Move, Render
import constants

MAIN_COLOR = "white"
BACKGROUND_COLOR = "black"
LINE_COLOR = (50, 50, 50)

SCREEN_SIZE = (400, 500)
WINDOW_NAME = "Tetris"

SYS_FONT = "Arial"

FPS = 30

DEFAULT_DROP_PER_SECONDS = 4
DROP_DELAY_FRAMES = FPS // DEFAULT_DROP_PER_SECONDS

SOFT_DROP_DELAY_FRAMES = 1

GAME_X, GAME_Y = (100, 60)
BLOCK_SIZE = 20
    
def main() -> None:
    pygame.init()
    
    pygame.key.set_repeat(1000 // 4, 1000 // 10)
    
    board = Tetris(constants.BOARD_WIDTH, constants.BOARD_HEIGHT, DROP_DELAY_FRAMES, SOFT_DROP_DELAY_FRAMES)
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_NAME)
    
    clock = pygame.time.Clock()
        
    pressing_down = False
    
    going = True
    
    while going:
        
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
        
        board.render_as_pygame(screen, BLOCK_SIZE,
                              (GAME_X, GAME_Y),
                              BACKGROUND_COLOR, LINE_COLOR, MAIN_COLOR)

        # print(board.render_as_str(full_block=True))
        
        text = pygame.font.SysFont(SYS_FONT, 25, True, False).render(f"Score: {info['score']}", True, MAIN_COLOR)
        screen.blit(text, [5, 5])
            
        pygame.display.flip()

        clock.tick(FPS)


    pygame.quit()
        
if __name__ == "__main__":
    main()