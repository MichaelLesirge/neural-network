from typing import Generator, Self

import numpy as np

CoordinatePair = tuple[int, int]
WidthHeightPair = tuple[int, int]

def find_corners(grid: np.ndarray, null_value=0) -> tuple[CoordinatePair, CoordinatePair]:
    empty_positions = np.where(grid != null_value)
    if len(empty_positions[0]) == 0:
        return
    y_start = min(empty_positions[0])
    y_end = max(empty_positions[0]) + 1
    x_start = min(empty_positions[1])
    x_end = max(empty_positions[1]) + 1
    return ((x_start, y_start), (x_end, y_end))


class Grid:
    def __init__(self, grid: np.ndarray, null_value=0) -> None:
        self.grid = grid
        self.null_value = null_value

    @classmethod
    def empty(cls, shape: WidthHeightPair, null_value=0, dtype=int) -> Self:
        width, height = shape
        new = cls(np.empty((height, width), dtype=dtype), null_value)
        new.clear()
        return new

    @classmethod
    def empty_like(cls, prototype: Self) -> Self:
        new = cls(np.empty_like(prototype.get_grid_array()), prototype.get_null_value())
        new.clear()
        return new

    def clear(self) -> None:
        self.grid.fill(self.null_value)

    def get_grid_array(self) -> np.ndarray:
        return self.grid

    def get_null_value(self) -> np.ndarray:
        return self.null_value

    def insert(self, position: CoordinatePair, subgrid: np.ndarray) -> None:
        """Put subgrid at specified position in main grid, EMPTY values will not be set"""

        x, y = position

        corners = find_corners(subgrid, self.null_value)

        if corners is None:
            return

        ((x_start, y_start), (x_end, y_end)) = corners

        subgrid = subgrid[y_start:y_end, x_start:x_end]
        x, y = x + x_start, y + y_start
        width, height = x_end - x_start, y_end - y_start


        view = self.grid[y : y + height, x : x + width]
        mask = subgrid != self.null_value

        view[mask] = subgrid[mask]

    def insert_if_empty(self, position: CoordinatePair, subgrid: np.ndarray) -> bool:
        """if subgrid does not overlap, insert it and return true"""
        x, y = position

        corners = find_corners(subgrid, self.null_value)

        if corners is None:
            return True

        ((x_start, y_start), (x_end, y_end)) = corners

        subgrid = subgrid[y_start:y_end, x_start:x_end]
        x, y = x + x_start, y + y_start
        width, height = x_end - x_start, y_end - y_start

        view = self.grid[y : y + height, x : x + width]

        if view.shape != subgrid.shape:
            return False

        mask = subgrid != self.null_value

        # Check to see if there is any overlap
        if np.logical_and(view[mask], subgrid[mask]).any():
            return False

        # Set values in grid by setting view
        view[mask] = subgrid[mask]
        return True

    def insert_empty(
        self, position: CoordinatePair, subgrid_mask: np.ndarray[bool]
    ) -> None:
        """Clear all values at specified position where subgrid_mask is True"""
        x, y = position
        height, width = subgrid_mask.shape

        view = self.grid[y : y + height, x : x + width]
        view[subgrid_mask.astype(bool)] = 0

    def does_overlap(self, position: CoordinatePair, subgrid: np.ndarray) -> bool:
        """check if subgrid overlaps with anything in grid at specified position"""
        x, y = position

        corners = find_corners(subgrid, self.null_value)

        if corners is None:
            return False

        ((x_start, y_start), (x_end, y_end)) = corners

        subgrid = subgrid[y_start:y_end, x_start:x_end]
        x, y = x + x_start, y + y_start
        width, height = x_end - x_start, y_end - y_start

        view = self.grid[y : y + height, x : x + width]

        if view.shape != subgrid.shape:
            return True

        mask = subgrid != self.null_value

        # Check to see if there is any overlap
        return np.logical_and(view[mask], subgrid[mask]).any()

    def find_full_lines(self) -> list[int]:
        return [i for i, row in enumerate(self.grid) if all(row)]

    def remove_full_lines(self, lines: list[int]) -> None:
        for line in lines:
            self.grid[1:line + 1, :] = self.grid[:line, :]
            self.grid[0, :] = 0

    def get_number_of_surrounded_holes(self) -> int:
        holes = 0

        for col in range(self.grid.shape[1]):
            has_seen_block = False
            for row in range(self.grid.shape[0]):
                if (not has_seen_block and self.grid[row, col]): has_seen_block = True
                holes += has_seen_block and self.grid[row, col] == 0 and (col < 1 or self.grid[row, col - 1] != 0) and (col >= self.grid.shape[1] - 1 or self.grid[row, col + 1] != 0)
        
        return holes
                    
    def get_number_of_holes(self) -> int:
        holes = 0

        for col in self.grid.T:
            has_seen_block = False
            for value in col:
                if (not has_seen_block and value): has_seen_block = True
                holes += (has_seen_block) and value == 0
        
        return holes
    
    def get_column_heights(self) -> np.ndarray[int]:
        mask = self.grid != 0
        return self.grid.shape[0] - np.where(mask.any(axis=0), mask.argmax(axis=0), self.grid.shape[0])
    
    def get_heights_bumpiness(self) -> int:
        heights = self.get_column_heights()
        total_bumpiness = 0
        for i, height in enumerate(heights[:-1]):
            height_difference = height - heights[i + 1]
            total_bumpiness += abs(height_difference)
        return total_bumpiness

    def get_grid_string(
        self, full_tile_str="[]", empty_tile_str="  "
    ) -> str:
        
        start_pad = "["
        end_pad = "]"

        return "\n".join(
            start_pad + (
                "".join(
                    (
                        full_tile_str
                        if (item != self.null_value)
                        else empty_tile_str
                    )
                    for item in row
                )
            ) + end_pad
            for row in self.grid 
        )

    def get_height(self) -> int:
        return self.grid.shape[0]

    def get_width(self) -> int:
        return self.grid.shape[1]

    def copy(self):
        return self.__class__(self.grid.copy(), self.null_value)

    def __iter__(self) -> Generator[tuple[int, CoordinatePair], None, None]:
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                yield (self.grid[row, col], (row, col))

    def __str__(self) -> str:
        return self.get_grid_string()
