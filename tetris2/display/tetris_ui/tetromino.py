from typing import Self, Callable

import pygame

from ._common import ColorValue, Size, FileArg

def _load_image(filename: str, fallback_image: pygame.Surface) -> pygame.Surface:
    try:
        return pygame.image.load(filename)
    except FileNotFoundError:
        return fallback_image
    
def _create_square(color: ColorValue = None) -> pygame.Surface:
    surface = pygame.Surface((1, 1))
    if color is not None: surface.fill(color)
    return surface

class TetrominoTiles:
    def __init__(
        self,
        tetromino_tiles: dict[int, pygame.Surface],
        missing_tetrominoes_tile: pygame.Surface = None,
        null_tile_value: int = 0
    ) -> None:

        self.tetrominoes_tiles = tetromino_tiles

        if missing_tetrominoes_tile is None:
            missing_tetrominoes_tile = _create_square()

        self.missing_tetromino_tile = missing_tetrominoes_tile

        self.null_tile_value = null_tile_value

    @classmethod
    def from_image_files(
        cls,
        tetromino_tile_filenames: dict[str, FileArg],
        missing_tetromino_filename: FileArg = None,
        null_tile_value: int = 0,
    ):
        
        missing_tetrominoes_tile = _load_image(missing_tetromino_filename, _create_square())

        return cls(
            {key: _load_image(image, missing_tetrominoes_tile) for key, image in tetromino_tile_filenames.items()},
            missing_tetrominoes_tile,
            null_tile_value,
        )

    @classmethod
    def from_colors(
        cls,
        tetromino_tile_filenames: dict[str, ColorValue],
        missing_tetromino_color: ColorValue = None,
        null_tile_value: int = 0,
    ):

        return cls(
            {key: _create_square(color) for key, color in tetromino_tile_filenames.items()},
            _create_square(missing_tetromino_color),
            null_tile_value,
        )
    
    def apply(self, func: Callable[[pygame.Surface], pygame.Surface]):
        return self.__class__(
            tetromino_tiles = {key: func(tile) for key, tile in self.tetrominoes_tiles.items()},
            missing_tetrominoes_tile = func(self.missing_tetromino_tile),
            null_tile_value = self.null_tile_value
        )

    def get_tetromino_tile(self, tetromino_key: int, *, size: Size = None) -> pygame.Surface | None:
        if tetromino_key == self.null_tile_value:
            return None

        tile = self.tetrominoes_tiles.get(tetromino_key, self.missing_tetromino_tile)

        if size is not None:
            tile = pygame.transform.scale(tile, size)
        
        return tile

    def get_tetromino_tiles(
        self, tetromino_key_grid: list[list[int]], size: Size = None
    ) -> list[list[pygame.Surface | None]]:
        return [
            [self.get_tetromino_tile(tetromino_key, size=size) for tetromino_key in row]
            for row in tetromino_key_grid
        ]
