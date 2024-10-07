from typing import Self, Callable

import pygame

from ._common import ColorValue, Size, FileArg
    
def _create_square(color: ColorValue = None) -> pygame.Surface:
    surface = pygame.Surface((1, 1))
    if color is not None: surface.fill(color)
    return surface

class Tiles:
    def __init__(self, null_tile_value: int = 0, fallback_tile_color: ColorValue = "white") -> None:

        self.fallback_tile = _create_square(fallback_tile_color)
        self.null_tile_value = null_tile_value
        self.tetromino_tiles: dict[int, pygame.Surface] = {}


    def add_image_tile(self, tile_id: int, tile_filenames: FileArg) -> None:
        self.tetromino_tiles[tile_id] = pygame.image.load(tile_filenames)

    def add_color_tile(self, tile_id: int, color: ColorValue) -> None:
        self.tetromino_tiles[tile_id] = _create_square(color)
 
    def map(self, func: Callable[[pygame.Surface], pygame.Surface]) -> Self:
        return self.__class__(
            tetromino_tiles = {key: func(tile) for key, tile in self.tetromino_tiles.items()},
            missing_tetromino_tile = func(self.fallback_tile),
            null_tile_value = self.null_tile_value
        )

    def get_tile(self, tile_id: int, *, size: Size = None) -> pygame.Surface | None:
        if tile_id == self.null_tile_value:
            return None

        tile = self.tetromino_tiles.get(tile_id, self.fallback_tile)

        if size is not None:
            tile = pygame.transform.scale(tile, size)
        
        return tile