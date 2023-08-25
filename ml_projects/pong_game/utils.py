import pygame

class RelativeRectPoint:
    __slots__ = ("_base_surface", "_x", "_y")
    
    def __init__(self, base: pygame.Surface, point: tuple[float, float], *, reverse_x = False, reverse_y = False) -> None:
        self._base_surface = base
        self._x, self._y = point
        if reverse_x: self._x = 1 - self._x
        if reverse_y: self._y = 1 - self._y
         
    @property
    def x(self) -> int: return round(self._base_surface.get_width() * self._x)
    
    @property
    def y(self) -> int: return round(self._base_surface.get_height() * self._y)
    
    @property
    def point(self) -> tuple[int, int]: return (self.x, self.y)
    
    def __getitem__(self, index) -> int: return self.point[index]

    def flip(self, flip_x = False, flip_y = False) -> "RelativeRectPoint":
        return self.__class__(self._base_surface, (self._x, self._y), reverse_x=flip_x, reverse_y=flip_y)
    
    def point_centered_for(self, surface: pygame.Surface) -> tuple[int, int]:
        return (self.x - (surface.get_width() // 2), self.y - (surface.get_height() // 2))