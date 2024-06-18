import pygame

def _load_image(filename: str, fallback_image: pygame.Surface) -> pygame.Surface:
    try:
        return pygame.image.load(filename)
    except FileNotFoundError:
        return fallback_image
    
def _create_white_square() -> pygame.Surface:
    surface = pygame.Surface((1, 1))
    surface.fill("white")
    return surface

class TetrominoTiles:
    def __init__(
        self,
        tetrominoe_tiles: dict[int, pygame.Surface],
        missing_tetrominoes_tile: pygame.Surface = None,
        empty_tile_key: int = 0,
    ) -> None:

        self.tetrominoes_tiles = tetrominoe_tiles

        if missing_tetrominoes_tile is None:
            missing_tetrominoes_tile = _create_white_square()

        self.missing_tetrominoes = missing_tetrominoes_tile

        self.empty_tile_key = empty_tile_key

    @classmethod
    def from_image_files(
        cls,
        tetrominoe_tile_filenames: dict[str, pygame.Surface],
        missing_tetrominoe_filename: str = None,
        empty_tile_key: int = 0,
    ):
        
        missing_tetrominoes_tile = _load_image(missing_tetrominoe_filename, _create_white_square())

        return cls(
            {key: _load_image(image, missing_tetrominoes_tile) for key, image in tetrominoe_tile_filenames.items()},
            missing_tetrominoes_tile,
            empty_tile_key,
        )

    def get_tetromino_tile(self, tetromino_key: int, size: int = None) -> pygame.Surface | None:
        if tetromino_key == self.empty_tile_key:
            return None

        tile = self.tetrominoes_tiles.get(tetromino_key, self.missing_tetrominoes)

        if size is not None:
            tile = pygame.transform.scale(tile, (size, size))

        return tile

    def get_tetroino_tiles(
        self, tetromino_key_grid: list[list[int]], size: int = None
    ) -> list[list[pygame.Surface | None]]:
        return [
            [self.get_tetromino_tile(tetromino_key, size) for tetromino_key in row]
            for row in tetromino_key_grid
        ]
