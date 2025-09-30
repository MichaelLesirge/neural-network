import pygame

class ScreenRelativeVector2(pygame.Vector2):

    def to_pixels(self, screen: pygame.Surface) -> pygame.Vector2:
        return self.elementwise() * screen.get_size()

    def mirrored(self) -> "ScreenRelativeVector2":
        return self.__class__(1 - self.x, self.y)
    
    def copy(self) -> "ScreenRelativeVector2":
        return self.__class__(self.x, self.y)
