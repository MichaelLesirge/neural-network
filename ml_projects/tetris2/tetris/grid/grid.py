from typing import Generator 

import numpy as np

CoordinatePair = tuple[int, int]
WidthHeightPair = tuple[int, int]

def trim(subgrid: np.ndarray) -> tuple[np.ndarray, (int, int, int, int)]:
    subgrid_zeros = np.where(subgrid != 0)        
    subgrid_y_start = min(subgrid_zeros[0])
    subgrid_y_end = max(subgrid_zeros[0]) + 1
    subgrid_x_start = min(subgrid_zeros[1])
    subgrid_x_end = max(subgrid_zeros[1]) + 1
    return subgrid[subgrid_y_start : subgrid_y_end, subgrid_x_start : subgrid_x_end], (subgrid_x_start, subgrid_x_end, subgrid_y_start, subgrid_y_end)

class Grid:    
    def __init__(self, size: WidthHeightPair, empty: int = 0) -> None:
        width, height = size
        self.grid = np.empty((height, width), dtype=int)
        self.empty = empty
        self.clear()

    def clear(self) -> None:
        self.grid.fill(self.empty)

    def get_grid_array(self) -> np.ndarray:
        return self.grid
    
    def insert(self, position: CoordinatePair, subgrid: np.ndarray) -> None:
        """Put subgrid at specified position in main grid, EMPTY values will not be set"""
        
        x, y = position
        
        subgrid, (subgrid_x_start, subgrid_x_end, subgrid_y_start, subgrid_y_end) = trim(subgrid)

        x, y = x + subgrid_x_start, y + subgrid_y_start
        width, height = subgrid_x_end - subgrid_x_start, subgrid_y_end - subgrid_y_start
        
        view = self.grid[y:y+height, x:x+width]
        mask = subgrid != self.empty
        view[mask] = subgrid[mask]

    def insert_if_empty(self, position: CoordinatePair, subgrid: np.ndarray) -> bool:
        """if subgrid does not overlap, insert it and return true"""
        x, y = position

        subgrid, (subgrid_x_start, subgrid_x_end, subgrid_y_start, subgrid_y_end) = trim(subgrid)

        x, y = x + subgrid_x_start, y + subgrid_y_start
        width, height = subgrid_x_end - subgrid_x_start, subgrid_y_end - subgrid_y_start
        
        view = self.grid[y:y+height, x:x+width]
        
        if view.shape != subgrid.shape:
            return False
        
        mask = subgrid != self.empty

        # Check to see if there is any overlap
        if np.logical_and(view[mask], subgrid[mask]).any():
            return False
        
        # Set values in grid by setting view
        view[mask] = subgrid[mask] 
        return True
        
    def insert_empty(self, position: CoordinatePair, subgrid_mask: np.ndarray[bool]) -> None:
        """Clear all values at specified position where subgrid_mask is True"""
        x, y = position
        height, width = subgrid_mask.shape
        
        view = self.grid[y:y+height, x:x+width]
        view[subgrid_mask.astype(bool)] = 0
        

    def does_overlap(self, position: CoordinatePair, subgrid: np.ndarray) -> bool:
        """check if subgrid overlaps with anything in grid at specified position"""
        x, y = position

        subgrid, (subgrid_x_start, subgrid_x_end, subgrid_y_start, subgrid_y_end) = trim(subgrid)

        x, y = x + subgrid_x_start, y + subgrid_y_start
        width, height = subgrid_x_end - subgrid_x_start, subgrid_y_end - subgrid_y_start
        
        view = self.grid[y:y+height, x:x+width]
        
        if view.shape != subgrid.shape:
            return True
        
        mask = subgrid != self.empty

        # Check to see if there is any overlap
        return np.logical_and(view[mask], subgrid[mask]).any()

    def get_grid_string(self,
                      row_template_str="[%s]",
                      full_tile_template_str=" %s",
                      empty_tile_str="  ") -> str:

        return "\n".join(
            row_template_str % ("".join(
                full_tile_template_str % item if (item != self.empty) else empty_tile_str
                for item in row))
            for row in self.grid
        )
    
    def get_height(self) -> int:
        return self.grid.shape[0]

    def get_width(self) -> int:
        return self.grid.shape[1]

    def __iter__(self) -> Generator[tuple[int, CoordinatePair], None, None]:
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.grid[row, col], (row, col))

    def __str__(self) -> str:
        return self.get_grid_string()