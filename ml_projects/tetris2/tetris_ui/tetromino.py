import pygame


class TetrominoTiles:
    def __init__(
        self,
        tetrominoe_tiles: dict[int, pygame.Surface],
        missing_tetrominoes_tile: pygame.Surface = None,
        empty_tile_key: int = 0,
    ) -> None:

        self.tetrominoes_tiles = {**tetrominoe_tiles, empty_tile_key: None}

        if missing_tetrominoes_tile is None:
            missing_tetrominoes_tile = pygame.Surface((1, 1))
            missing_tetrominoes_tile.fill("white")

        self.missing_tetrominoes = missing_tetrominoes_tile

    @classmethod
    def from_image_files(
        cls,
        tetrominoe_tiles: dict[str, pygame.Surface],
        missing_tetrominoes: str,
        empty_tile_key: int,
    ):
        return cls(
            {key: pygame.image.load(image) for key, image in tetrominoe_tiles.items()},
            empty_tile_key,
            pygame.image.load(missing_tetrominoes),
        )

    def get_tetromino_tile(self, tetromino_key: int) -> pygame.Surface | None:
        return self.tetrominoes_tiles.get(tetromino_key, self.missing_tetrominoes)

    def get_tetroino_tiles(
        self, tetromino_key_grid: list[list[int]]
    ) -> list[list[pygame.Surface | None]]:
        return [
            [self.get_tetromino_tile(tetromino_key) for tetromino_key in row]
            for row in tetromino_key_grid
        ]
