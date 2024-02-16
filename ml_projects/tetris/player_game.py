import pygame
from tetris import Game, GameBoard, Moves, COLOR_MAP
import constants

MAIN_COLOR = "white"
BACKGROUND_COLOR = "black"
LINE_COLOR = (50, 50, 50)

SCREEN_SIZE = (400, 500)
WINDOW_NAME = "Tetris"

SYS_FONT = "Arial"

FPS = 30

GAME_X, GAME_Y = (100, 60)
BLOCK_SIZE = 20

class PlayerGame(Game):
    def __init__(self, board: GameBoard) -> None:
        super().__init__(board, drop_delay = FPS)
    
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(WINDOW_NAME)
        
        self.clock = pygame.time.Clock()
        
        self.all_moves = []

        self.pressing_down = False

    def draw_box(self, row: int, col: int, color = "white", width = 0, border_radius = -1, margin = 0):
        pygame.draw.rect(self.screen, color, pygame.Rect(
            GAME_X + col * BLOCK_SIZE + margin, GAME_Y + row * BLOCK_SIZE + margin,
            BLOCK_SIZE - margin, BLOCK_SIZE - margin
        ), width = width, border_radius = border_radius)            
 
    def display(self, frame: int, board: GameBoard):         
        self.screen.fill(BACKGROUND_COLOR)
        
        for col in range(board.width + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (GAME_X + BLOCK_SIZE * col, GAME_Y), (GAME_X + BLOCK_SIZE * col, GAME_Y + BLOCK_SIZE * board.height), width=1)

        for row in range(board.height + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (GAME_X, GAME_Y + BLOCK_SIZE * row), (GAME_X + BLOCK_SIZE * board.width, GAME_Y + BLOCK_SIZE * row), width=1)

        for value, (row, col) in board:
            if value: self.draw_box(row, col, color=COLOR_MAP[value], margin=1, border_radius=2)
            self.draw_box(row, col, color=LINE_COLOR, width = 1)
                
        for row, col in board.current_figure.type:
            if (board.current_figure.image()[row][col]):
                self.draw_box(board.current_figure.y + row, board.current_figure.x + col, color=board.current_figure.get_color(), margin=1, border_radius=2)

        text = pygame.font.SysFont(SYS_FONT, 25, True, False).render("Score: " + str(board.score), True, MAIN_COLOR)
        
        pygame.draw.rect(self.screen, MAIN_COLOR, pygame.Rect(
            GAME_X, GAME_Y, BLOCK_SIZE * board.width, BLOCK_SIZE * board.height 
        ), width=1)

        self.screen.blit(text, [5, 5])
        
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def get_moves(self, frame: int, game: GameBoard) -> list[Moves]:
        moves = []
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return [Moves.QUIT]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    return [Moves.QUIT]
                if event.key == pygame.K_UP:        moves.append(Moves.SPIN)
                if event.key == pygame.K_LEFT:      moves.append(Moves.LEFT)
                if event.key == pygame.K_RIGHT:     moves.append(Moves.RIGHT)
                if event.key == pygame.K_SPACE:     moves.append(Moves.HARD_DROP)
                if event.key == pygame.K_DOWN:      self.pressing_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:      self.pressing_down = False
        
        if self.pressing_down: moves.append(Moves.SOFT_DROP)   
        
        return moves
 
def main() -> None:
    pygame.init()
    
    pygame.key.set_repeat(1000 // 4, 1000 // 10)
    
    board = GameBoard(constants.BOARD_WIDTH, constants.BOARD_HEIGHT)
    game = PlayerGame(board)
    
    game.run()
        
    pygame.quit()
        
if __name__ == "__main__":
    main()