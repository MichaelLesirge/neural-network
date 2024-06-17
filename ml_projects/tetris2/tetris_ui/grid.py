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
        focused_rect: pygame.Rect = None
    ) -> None:
        
        self.surface = surface
        self.grid_pixel_size = grid_size

        if focused_rect is None:

            focused_rect = pygame.Rect(
                (0, 0),
                (
                    self.surface.get_width() // self.grid_pixel_size,
                    self.surface.get_height() // self.grid_pixel_size,
                )
            )
        
        self.focused_rect = focused_rect
        
    # --- Factory Methods ---

    @classmethod
    def create_from_rows(cls, surface: pygame.Surface, num_of_rows: int):
        return cls(surface, surface.get_height() // num_of_rows)

    @classmethod
    def create_from_cols(cls, surface: pygame.Surface, num_of_cols: int):
        return cls(surface, surface.get_width() // num_of_cols)

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
            return (position + self.focused_rect.topleft) * self.grid_pixel_size

        return self.to_pixel_relative_position(Vector2(position))

    def to_grid_realtive_position(self, position: xyPair) -> Vector2:
        """Convert pixel locations on surface to grid coordinate"""
        if isinstance(position, (Vector2)):
            return position / self.grid_pixel_size - self.focused_rect.topleft

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
        size = Vector2(size)

        if position.x < 0:
            position.x = self.get_grid_size().x + position.x
        if position.y < 0:
            position.y = self.get_grid_size().y + position.y

        if size.x < 0:
            size.x = self.get_grid_size().x + size.x
        if size.y < 0:
            size.y = self.get_grid_size().y + size.y

        position.x += self.focused_rect.x
        position.y += self.focused_rect.y

        position.x -= size.x * alignX
        position.y -= size.y * alignY

        return self.__class__(self.surface, self.grid_pixel_size, focused_rect=pygame.Rect(position, size))

    # --- Pixel Surface Getters ---

    def get_square_pixels(self) -> int:
        """Get size of indivual square"""
        return self.grid_pixel_size

    def get_pixels_left_top(self) -> Vector2:
        return self.to_pixel_relative(self.focused_rect.topleft)

    def get_pixels_size(self) -> Vector2:
        return self.to_pixel_relative(self.focused_rect.size)

    # --- Grid Getters ---

    def get_grid_top_left(self) -> Vector2:
        """Get width and height of focused grid"""
        return Vector2(self.focused_rect.topleft)

    def get_grid_size(self) -> Vector2:
        """Get width and height of focused grid"""
        return Vector2(self.focused_rect.size)

    # --- Context Operations ---

    def fill(self, color: ColorValue) -> None:
        """Fill focused area with color"""
        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                self.get_pixels_left_top(),
                self.to_pixel_relative(self.focused_rect.size),
            ),
        )

    def outline(self, thickness: int, color: ColorValue = "white") -> None:
        
        offset = 0 if thickness < 0 else thickness

        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(
                self.get_pixels_left_top() - (offset, offset),
                self.get_pixels_size() + (offset * 2, offset * 2),
            ),
            width=abs(thickness),
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
