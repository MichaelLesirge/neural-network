import pygame
import random

class TetrominoBlockShape:
    MAX_ROTATIONS = 4
    
    def __init__(self, name: str, color: pygame.Color, shape: list[list[int]]) -> None:
        self.name = name
        self.color = color
        
        self.height = len(shape)
        self.width = len(shape[0])
        
        self.shapes = [shape]
        for i in range(TetrominoBlockShape.MAX_ROTATIONS):
            shape = TetrominoBlockShape.rotate_clockwise(shape)
            if shape == self.shapes[0]: break
            self.shapes.append(shape)

    @staticmethod
    def rotate_clockwise(matrix: list[list[int]]):
        return list(list(x) for x in zip(*matrix))[::-1]
    
    def __iter__(self) -> tuple[int, int]:
        for row in range(self.height):
            for col in range(self.width):
                yield (row, col)

SHAPES = [
    TetrominoBlockShape("I", (0, 240, 240), [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ]),
    TetrominoBlockShape("O", (240,240,0), [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]),
    TetrominoBlockShape("L", (240,160,0), [
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]),
    TetrominoBlockShape("J", (0,0,240), [
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]),
    TetrominoBlockShape("T", (160,0,240), [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]),
    TetrominoBlockShape("Z", (240,0,0), [
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0],
    ]),
    TetrominoBlockShape("S", (0,240,0), [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]),
]

pygame.init()

MAIN_COLOR = "white"
BACKGROUND_COLOR = "black"
LINE_COLOR = (100, 100, 100)

SCREEN_SIZE = (400, 500)
WINDOW_NAME = "Tetris"

SYS_FONT = "Arial"

FPS = 60

BOARD_WIDTH, BOARD_HEIGHT = 10, 20

GAME_X, GAME_Y = (100, 60)
BLOCK_SIZE = 20

class Tetromino:

    def __init__(self, x: int, y: int, type: TetrominoBlockShape, rotation: int = 0) -> None:
        self.x = x
        self.y = y

        self.type = type

        self.rotation = rotation % len(self.type.shapes)

    def get_color(self) -> pygame.Color:
        return self.type.color

    def image(self) -> list[list[int]]:
        return self.type.shapes[self.rotation]
    
    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % len(self.type.shapes)

    def __iter__(self) -> tuple[int, tuple[int, int]]:
        for row, col in self.type:
            yield (self.image()[row][col], (row, col))
            


class Tetris:
    def __init__(self, width: int, height: int) -> None:

        self.current_figure = None

        self.width, self.height = width, height

        self.grid = [[None] * self.width for i in range(self.height)]
        self.score = 0

    def new_figure(self):
        self.current_figure = Tetromino(self.width // 2, 0, random.choice(SHAPES), rotation=random.randrange(TetrominoBlockShape.MAX_ROTATIONS))

    def intersects(self):
        for row, col in self.current_figure.type:
            if self.current_figure.image()[row][col] and ( 
                row + self.current_figure.y >= self.height or
                col + self.current_figure.x >= self.width or
                col + self.current_figure.x < 0 or
                self.grid[row + self.current_figure.y][col + self.current_figure.x] is not None
            ):
                return True

    def find_full_lines(self) -> list[int]:
        lines = []
        
        for i, row in enumerate(self.grid):
            if all(row): lines.append(i)
                        
        return lines

    def remove_full_lines(self, lines: list[int]) -> None:
        for line in lines: self.grid.pop(line)
        for line in lines: self.grid.insert(0, [None] * self.width)
        

    def hard_drop(self) -> None:
        while not self.intersects():
            self.current_figure.y += 1
        self.current_figure.y -= 1
        self.freeze()

    def soft_drop(self) -> None:
        self.current_figure.y += 1
        if self.intersects():
            self.current_figure.y -= 1
            self.freeze()

    def freeze(self) -> bool:
        for value, (row, col) in self.current_figure:
            if value: self.grid[row + self.current_figure.y][col + self.current_figure.x] = self.current_figure.get_color()

        lines = self.find_full_lines()
        self.remove_full_lines(lines)
        
        self.new_figure()

        return self.intersects()
        
    def change_x(self, dx: int) -> None:
        old_x = self.current_figure.x
        self.current_figure.x += dx
        if self.intersects():
            self.current_figure.x = old_x

    def rotate(self) -> None:
        old_rotation = self.current_figure.rotation
        self.current_figure.rotate()
        if self.intersects():
            self.current_figure.rotation = old_rotation
    
    def __iter__(self) -> tuple[pygame.Color | None, tuple[int, int]]:
        for row in range(self.height):
            for col in range(self.width):
                yield (self.grid[row][col], (row, col))


def pick_move(game: Tetris, events: list[pygame.event.Event]):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_LEFT:
                game.change_x(-1)
            if event.key == pygame.K_RIGHT:
                game.change_x(1)
            if event.key == pygame.K_SPACE:
                game.hard_drop()
            if event.key == pygame.K_ESCAPE:
                game.__init__(BOARD_WIDTH, BOARD_HEIGHT)
    
def main() -> None:
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_NAME)

    clock = pygame.time.Clock()

    game = Tetris(BOARD_WIDTH, BOARD_HEIGHT)
    
    def draw_box(row: int, col: int, color = "white", width = 0, border_radius = -1, margin = 0):
        pygame.draw.rect(screen, color, pygame.Rect(
            GAME_X + col * BLOCK_SIZE + margin, GAME_Y + row * BLOCK_SIZE + margin,
            BLOCK_SIZE - margin, BLOCK_SIZE - margin
        ), width = width, border_radius = border_radius)
    
    level = 2

    pressing_down = False

    counter = 0
    
    done = False

    while not done:
        if game.current_figure is None:
            game.new_figure()

        counter += 1
        
        if counter % (FPS // level) == 0 or (pressing_down and counter % (FPS // (level+5)) == 0):
            game.soft_drop()

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pressing_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        pick_move(game, events)

        screen.fill(BACKGROUND_COLOR)
        

        for col in range(game.width + 1):
            pygame.draw.line(screen, LINE_COLOR, (GAME_X + BLOCK_SIZE * col, GAME_Y), (GAME_X + BLOCK_SIZE * col, GAME_Y + BLOCK_SIZE * game.height), width=1)

        for row in range(game.height + 1):
            pygame.draw.line(screen, LINE_COLOR, (GAME_X, GAME_Y + BLOCK_SIZE * row), (GAME_X + BLOCK_SIZE * game.width, GAME_Y + BLOCK_SIZE * row), width=1)

        for value, (row, col) in game:
            if value: draw_box(row, col, color=value, margin=1, border_radius=2)
            draw_box(row, col, color=LINE_COLOR, width = 1)
                
        for row, col in game.current_figure.type:
            if (game.current_figure.image()[row][col]):
                draw_box(game.current_figure.y + row, game.current_figure.x + col, color=game.current_figure.get_color(), margin=1, border_radius=2)

        text = pygame.font.SysFont(SYS_FONT, 25, True, False).render("Score: " + str(game.score), True, MAIN_COLOR)

        screen.blit(text, [5, 5])
        
        pygame.display.flip()
        clock.tick(FPS)

    text_game_over = pygame.font.SysFont(SYS_FONT, 65, True, False).render("Game Over", True, MAIN_COLOR)
    screen.blit(text_game_over, [20, 200])

    pygame.quit()


if __name__ == "__main__":
    main()
