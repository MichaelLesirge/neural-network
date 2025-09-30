import pygame

class ScreenRelativeVector2(pygame.Vector2):

    @classmethod
    def from_pixels(cls, screen: pygame.Surface, pixels: tuple[int, int]) -> "ScreenRelativeVector2":
        return cls(pixels).elementwise() / screen.get_size()

    def to_pixels(self, screen: pygame.Surface) -> pygame.Vector2:
        return self.elementwise() * screen.get_size()

    def mirrored(self) -> "ScreenRelativeVector2":
        return self.__class__(1 - self.x, self.y)
    
    def copy(self) -> "ScreenRelativeVector2":
        return self.__class__(self.x, self.y)
