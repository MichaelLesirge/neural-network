import pygame
from pygame import Vector2

xyPair = tuple[int, int] | Vector2
ColorValue = tuple[int, int, int] | str

State = tuple

class Align:
    START = 0
    END = 1
    CENTER = 0.5


class GridContext:
    def __init__(
        self,
        surface: pygame.Surface,
        grid_size: int,
        *,
        position: Vector2 = None,
        size: Vector2 = None
    ) -> None:
        
        self.surface = surface
        self.grid_pixel_size = grid_size

        if position is None:
            position = Vector2(0, 0)

        if size is None:
            size = Vector2(
                self.surface.get_width() // self.grid_pixel_size,
                self.surface.get_height() // self.grid_pixel_size,
            )
        
        self.position = position
        self.size = size
        
    # --- Factory Methods ---

    @classmethod
    def create_from_rows(cls, surface: pygame.Surface, num_of_rows: int):
        return cls(surface, round(surface.get_height() / num_of_rows))

    @classmethod
    def create_from_cols(cls, surface: pygame.Surface, num_of_cols: int):
        return cls(surface, round(surface.get_width() / num_of_cols))

    @classmethod
    def create_from_smallest_size(cls, surface: pygame.Surface, size: xyPair):
        cols, rows = size
        return cls(surface, round(min(surface.get_width() / cols, surface.get_height() / rows)))

    # --- Size Conversion ---

    def to_pixel_relative(self, position: xyPair) -> Vector2:
        """Convert grid coordinate to pixel location on surface"""

        if isinstance(position, (Vector2)):
            return position * self.grid_pixel_size

        return self.to_pixel_relative(Vector2(position))

    def to_grid_realtive(self, position: xyPair) -> Vector2:
        """Convert pixel locations on surface to grid coordinate"""
        if isinstance(position, (Vector2)):
            return position / self.grid_pixel_size

        return self.to_grid_realtive(Vector2(position))

    # --- Position Conversion ---

    def to_pixel_relative_position(self, position: xyPair) -> Vector2:
        """Convert grid coordinate to pixel location on surface"""

        if isinstance(position, (Vector2)):
            return (position + self.position) * self.grid_pixel_size

        return self.to_pixel_relative_position(Vector2(position))

    def to_grid_realtive_position(self, position: xyPair) -> Vector2:
        """Convert pixel locations on surface to grid coordinate"""
        if isinstance(position, (Vector2)):
            return position / self.grid_pixel_size - self.position

        return self.to_grid_realtive_position(Vector2(position))

    def with_focused_window(
        self,
        position: xyPair,
        size: xyPair,
        *,
        alignX=Align.START,
        alignY=Align.START,
    ):  
        position = Vector2(position)

        if position.x < 0:
            position.x = self.get_grid_size().x + position.x
        if position.y < 0:
            position.y = self.get_grid_size().y + position.y

        if size is None:
            size = self.get_grid_size() - position
            
        size = Vector2(size)

        if size.x < 0:
            size.x = self.get_grid_size().x + size.x
        if size.y < 0:
            size.y = self.get_grid_size().y + size.y

        position.x += self.position.x
        position.y += self.position.y

        position.x -= size.x * alignX
        position.y -= size.y * alignY

        return self.__class__(self.surface, self.grid_pixel_size, position = position, size = size)

    # --- Pixel Surface Getters ---

    def get_square_pixels(self) -> int:
        """Get size of indivual square"""
        return self.grid_pixel_size

    def get_pixels_left_top(self) -> Vector2:
        return self.to_pixel_relative(self.position)

    def get_pixels_size(self) -> Vector2:
        return self.to_pixel_relative(self.size)

    # --- Grid Getters ---

    def get_grid_top_left(self) -> Vector2:
        """Get width and height of focused grid"""
        return Vector2(self.position)

    def get_grid_size(self) -> Vector2:
        """Get width and height of focused grid"""
        return Vector2(self.size)

    # --- Context Operations ---

    def fill(self, color: ColorValue) -> None:
        """Fill focused area with color"""
        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                self.get_pixels_left_top(),
                self.to_pixel_relative(self.size),
            ),
        )

    def outline(self, pixels_thickness: int, color: ColorValue) -> None:
        
        offset = 0 if pixels_thickness < 0 else pixels_thickness

        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                self.get_pixels_left_top() - (offset, offset),
                self.get_pixels_size() + (offset * 2, offset * 2),
            ),
            width=abs(pixels_thickness),
        )

    def blit(
        self,
        source: pygame.Surface,
        destination: xyPair,
        *,
        alignX=Align.START,
        alignY=Align.START,
    ) -> None:
        """Blit source onto focused area"""

        x, y = self.to_pixel_relative_position(destination)

        x -= source.get_width() * alignX
        y -= source.get_height() * alignY

        self.surface.blit(source, (x, y))
